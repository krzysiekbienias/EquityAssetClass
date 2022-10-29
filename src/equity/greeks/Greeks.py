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


from equity.calendar_schedule.DealCalendarSchedule import SetUpSchedule

class Greeks(SetUpSchedule):

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

        self._type_option = type_option  # call or put
        self._S0 = current_price
        self._K = strike
        self._r = ann_risk_free_rate
        self._sigma = ann_volatility
        self._divid = ann_dividend

        self.mfd1 = self.d1_fun()
        self.mfd2 = self.d2_fun()

        self.year_fraction = self.m_year_fraction_conv.yearFraction(self.m_ql_valuation_date,
                                                                    self.m_ql_termination_date)

        self.m_delta = self.delta()
        self.m_gamma = self.gamma()
        self.m_vega = self.vega()


    def d1(self)->float:
        """function d1
        Description
        -----------
        Function calculates :math:`d_{1}` ingredient needed to calculating price Scholes formula.

        Returns
        -------
        float
        """
        d1 = (np.log(self._S0 / self._K) + (
                self._r - self._divid + 0.5 * self._sigma ** 2) * self.year_fraction) / (
                     np.sqrt(self.year_fraction) * self._sigma)
        return d1

    #
    def d2(self)->float:
        """function d2

        Description
        -----------

        Function calculates :math:`d_{2}` ingredient needed to calculating price Scholes formula.

        Returns
        -------
        float
            
        """
        d2 = (np.log(self._S0 / self._K) + (
                self._r - self._divid - 0.5 * self._sigma ** 2) * self.year_fraction) / (
                     np.sqrt(self.year_fraction) * self._sigma)
        
        return d2


    def delta(self)->float:
        """delta 

        Function returns derivative with respect to underlier's price

        Returns
        -------
        float
            _description_
        """

        if (self._type_option == 'call'):
            delta = stats.norm.cdf(self.d1_fun(), 0, 1)

        else:
            delta = -stats.norm.cdf(-self.d1_fun(), 0, 1)

        return delta

    def gamma(self):  # for call and put is identical
        """gamma 

        Function returs second derivative with resppect to the time.

        Returns
        -------
        float
            
        """             
        gamma = stats.norm.pdf(self.d1_fun(), 0, 1) * np.exp(
            -self._divid * self.year_fraction) / (
                        self._S0 * self._sigma * np.sqrt(
                    self.year_fraction))

        return gamma

    def vega(self):
        vega = self._S0 * np.exp(-self._divid * self.year_fraction) * np.sqrt(
            self.year_fraction) * stats.norm.pdf(self.d1_fun(), 0, 1)

        return vega

    def theta(self):
        if (self._type_option == 'call'):
            fTheta = -self._S0 * stats.norm.pdf(self.d1_fun(), 0, 1) * self._sigma * np.exp(
                -self._divid * self.year_fraction) / 2 * np.sqrt(
                self.year_fraction) + self._divid * self._S0 * np.exp(
                -self._divid *
                self.year_fraction) * stats.norm.pdf(self.d1_fun(), 0,
                                                                            1) - self._r * self._K * np.exp(-self._r *
                                                                                                            self.year_fraction) * stats.norm.pdf(
                self.d2_fun(), 0, 1)
            return fTheta
        if (self._type_option == 'put'):
            fTheta = -self._S0 * stats.norm.pdf(self.d1_fun(), 0, 1) * self._sigma * np.exp(
                -self._divid * self.year_fraction) / 2 * np.sqrt(
                self.year_fraction) - self._divid * self._S0 * np.exp(
                -self._divid *
                self.year_fraction) * stats.norm.pdf(-self.d1_fun(), 0,
                                                                            1) - self._r * self._K * np.exp(-self._r *
                                                                                                            self.year_fraction) * stats.norm.pdf(
                -self.d2_fun(), 0, 1)
            return fTheta

if __name__ == '__main__':
    os.chdir('/Users/krzysiekbienias/Documents/logger_files/')
    lb = LoggerBuilder()
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    log = lb.define_logger('Greeks' + stamp)
    lb.logging_conf()



    greeks_short_maturity = Greeks(valuation_date=datetime(2022,4,7),
                                               termination_date=datetime(2022,4,17),
                                               frequency='daily',
                                               year_fraction_convention='Actual365',  # Daily,Monthly,Quarterly
                                               calendar='USA',

                                               ##################################
                                               type_option='call',
                                               current_price=40,
                                               strike=38,
                                               ann_risk_free_rate=0.03,
                                               ann_volatility=0.23,
                                               ann_dividend=0)

    greeks_medium_maturity = Greeks(valuation_date=datetime(2022, 4, 7),
                                   termination_date=datetime(2022, 5, 7),
                                   frequency='daily',
                                   year_fraction_convention='Actual365',  # Daily,Monthly,Quarterly
                                   calendar='USA',

                                   ##################################
                                   type_option='call',
                                   current_price=40,
                                   strike=38,
                                   ann_risk_free_rate=0.03,
                                   ann_volatility=0.23,
                                   ann_dividend=0)

    greeks_long_maturity = Greeks(valuation_date=datetime(2022, 4, 7),
                                    termination_date=datetime(2022, 10, 7),
                                    frequency='daily',
                                    year_fraction_convention='Actual365',  # Daily,Monthly,Quarterly
                                    calendar='USA',

                                    ##################################
                                    type_option='call',
                                    current_price=40,
                                    strike=38,
                                    ann_risk_free_rate=0.03,
                                    ann_volatility=0.23,
                                    ann_dividend=0)


