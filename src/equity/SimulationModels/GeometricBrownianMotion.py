import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import operator
import QuantLib as ql
import os
import pandas as pd
from datetime import datetime

from equity.utils.logger.LoggerUtils import LoggerBuilder
from equity.tools.IOTools import IOTools

from equity.calendar_schedule.DealCalendarSchedule import SetUpSchedule


class RiskFactorSimulator(SetUpSchedule):

    def __init__(self, valuation_date, termination_date, calendar, year_fraction_convention, frequency,
                 type_option, current_price, strike, ann_risk_free_rate, ann_volatility,
                 ann_dividend
                 ):
        '''

        Parameters
        ----------
        valuation_date
        termination_date
        calendar
        year_fraction_convention
        frequency
        type_option
        current_price
        strike
        ann_risk_free_rate
        ann_volatility
        ann_dividend
        '''
        SetUpSchedule.__init__(self, valuation_date, termination_date, calendar, year_fraction_convention, frequency)

        # --------------
        # Region: Instatnces
        # ---------------
        self._type_option = type_option  # call or put
        self._S0 = current_price
        self._K = strike
        self._r = ann_risk_free_rate
        self._sigma = ann_volatility
        self._divid = ann_dividend
        # --------------
        # End Region: Instatnces
        # ---------------

        year_fractions_sequence = self.consequitiveDatesYearFraction()
        risk_factor_paths = self.geometricBrownianMotion(year_fractions_sequence=year_fractions_sequence)

        df_gbm_paths = self.convertNumpyToDataFrame(arr=risk_factor_paths,
                                                date_index=self.dt_l_dates)

        paths_metrics_dfs = self.getPathsMetrics(df=df_gbm_paths,
                                                 t_quantiles_name=('upper_quantile', 'bottom_quantile'),
                                                 t_quantiles_values=(0.97, 0.03))
        # --------------
        # Region: Preparing Plots
        # ---------------
        graph_representation = IOTools.plotUsingMatplot(ts_df_list=[df_gbm_paths.iloc[:, :20], paths_metrics_dfs],
                                                        ts_labels_list=["Paths", "Metrics"],
                                                        n_col=2,
                                                        n_row=1)
        # --------------
        # Region: Customize Plots
        # ---------------
        graph_representation[1][0].set_facecolor('grey')
        graph_representation[1][1].set_facecolor('pink')
        graph_representation[1][1].legend(['Upper Quantile','Bottom Quantile','Mean'])
        os.chdir("/drop_point")
        graph_representation[0].savefig("equity_paths_GBM_Model.png")
        # --------------
        # Region: Customize Plots
        # ---------------

        # --------------
        # End Region: Preparing Plots
        # ---------------

    def eulerDiscretisationSchema(self, year_fractions_sequence, path_number=1000) -> np.array:
        """
        Description
        -----------
        This function creates numpy array that represents modelled equity behaviour using Euler discretisation schema.

        Parameters
        ----------
        path_number : int, optional
            number os scenarios, by default 1000

        Returns
        -------
        numpy arr
            array representing scenarios along defined timestep calendar
        """
        dt = year_fractions_sequence
        x_ip1 = np.zeros((x_ip1, len(
            self.ml_dates)))  # create empty array #TODO to nie moze byc do scenario calendar tylko zalezec od obiektu o_gbmscenarios
        x_ip1[:, 0] = self._S0
        for t in range(1, len(x_ip1[0])):
            z = np.random.standard_normal(x_ip1)
            x_ip1[:, t] = +x_ip1[:, t - 1] * dt + self._sigma * z * np.sqrt(dt)
        return np.transopse(x_ip1)

    def milsteinDiscretisationSchema(self, year_fractions_sequence, path_number: int = 1000) -> np.array:
        """

        Description
        -----------
        This function creates numpy array that represents modelled equity behaviour using milstein discretisation schema.

        

        Parameters
        ----------
        path_number : int, optional
            number os scenarios, by default 1000

        Returns
        -------
        np.array
            array representing scenarios along defined timestep calendar
        """

        dt = year_fractions_sequence
        x_ip1 = np.zeros((x_ip1, len(
            self.ml_dates)))  # create empty array #TODO to nie moze byc do scenario calendar tylko zalezec od obiektu o_gbmscenarios
        x_ip1[:, 0] = self._S0
        for t in range(1, len(x_ip1[0])):
            z = np.random.standard_normal(x_ip1)
            x_ip1[:, t] = +x_ip1[:, t - 1] * dt + self._sigma * z * np.sqrt(dt) + 0.5 * self.sigma * (dt * z - dt)
        return np.transopse(x_ip1)

    def geometricBrownianMotion(self, year_fractions_sequence, paths_number: int = 1000) -> np.array:
        """

        Parameters
        ----------
        paths_number : int, optional
            _description_, by default 1000

        Returns
        -------
        np.array
            _description_
        """

        dt = year_fractions_sequence
        gbm_model = np.zeros((paths_number, len(
            self.ml_dates)))  # create empty array #TODO to nie moze byc do scenario calendar tylko zalezec od obiektu o_gbmscenarios
        gbm_model[:, 0] = self._S0  # current price
        for t in range(1, len(gbm_model[0])):
            z = np.random.standard_normal(paths_number)  # draw number from normal distribution N(0,sqrt(t*sigma))
            gbm_model[:, t] = gbm_model[:, t - 1] * np.exp(
                (self._sigma - 0.5 * self._sigma ** 2) * dt[t - 1] +
                self._sigma * np.sqrt(dt[t - 1]) * z)
        return np.transpose(gbm_model)

    def convertNumpyToDataFrame(self, arr: np.array, date_index: list) -> pd.DataFrame:
        """function convertNumpyToDataFrame

        Parameters
        ----------
        arr : np.array
            _description_
        date_index : list
            List of datetimes

        Returns
        -------
        pd.DataFrame
        """
        df = pd.DataFrame(arr, index=date_index)
        return df

    def getPathsMetrics(self, df, t_quantiles_name, t_quantiles_values):
        metric_dic = dict()
        for q_name, q_value in zip(t_quantiles_name, t_quantiles_values):
            metric_dic[q_name] = df.quantile(q_value, axis=1)
        metric_dic['mean'] = df.mean(axis=1)
        df_metrics = pd.DataFrame.from_dict(metric_dic, orient='columns')
        df_metrics.index = self.dt_l_dates
        return df_metrics


if __name__ == '__main__':
    os.chdir('/Users/krzysiekbienias/Documents/logger_files/')
    lb = LoggerBuilder()
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    log = lb.define_logger('Monte_Carlo_Methods' + stamp)
    lb.logging_conf()
    o_black_scholes_long_maturity = RiskFactorSimulator(valuation_date=datetime(2022, 4, 7),
                                                        termination_date=datetime(2022, 10, 7),
                                                        frequency='daily',
                                                        year_fraction_convention='Actual365',
                                                        # Daily,Monthly,Quarterly
                                                        calendar='USA',

                                                        ##################################
                                                        type_option='call',
                                                        current_price=40,
                                                        strike=38,
                                                        ann_risk_free_rate=0.03,
                                                        ann_volatility=0.23,
                                                        ann_dividend=0)

    log.info("THE END")
