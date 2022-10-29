import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import operator
import QuantLib as ql
import os
import pandas as pd
from datetime import datetime as dt


from equity.utils.logger.LoggerUtils import LoggerBuilder


from equity.calendar_schedule.DealCalendarSchedule import SetUpSchedule




class AnalyticBlackScholes(SetUpSchedule):
    def __init__(self,current_price:float,
                      strike:float,
                      ann_risk_free_rate:float,
                      ann_volatility:float,
                      valuation_date:dt.datetime,
                      termination_date:dt.datetime,
                      calendar:str='USA',
                      year_fraction_convention:str='Actual365',
                      frequency:str='daily',
                      option_type:str='CALL',
            
                      ann_dividend:float=0
                 ):
        """__init__ _summary_

        _extended_summary_

        Parameters
        ----------
        current_price : float
            Current underlier price
        strike : float
            Option strike 
        ann_risk_free_rate : float
            Annual risk free rate, using for discounting
        ann_volatility : float
            Annual volatility
        valuation_date : dt.datetime
            _description_
        termination_date : dt.datetime
            _description_
        calendar : str, optional
            Calendars schedule according to it we follow holidays, by default 'USA'
        year_fraction_convention : str, optional
            The way how User might calculate year fraction, by default 'Actual365'
        frequency : str, optional
            _description_, by default 'daily'
        option_type : str, optional
            Type of option payoff, by default 'CALL'.
        ann_dividend : float, optional
            Divident of underlying asset, by default 0.

        Raises
        ------
        ValueError
            _description_
        ValueError
            _description_
        """

        SetUpSchedule.__init__(self, valuation_date,
                                termination_date,
                                calendar,
                                year_fraction_convention,
                                frequency)

        # --------------
        # Region: Input check
        # ---------------
        if option_type != 'CALL' and option_type!='PUT':
            raise ValueError("'type_option' must be one of two values CALL or PUT") 
        if  ann_volatility<=0:
            raise ValueError("'ann_volatility' must be positive float number.")    
        # --------------
        # Region: Input check
        # --------------- 
          
        
                                
        # ---------
        # Region Attributes 
        # ---------
        self._option_type=option_type
        self._year_fraction_conv = self.m_year_fraction_conv.yearFraction(self.m_ql_valuation_date,
                                                                          self.m_ql_termination_date)
        self.mbl_price = self.black_scholes_price_fun()                                                                  
        # ----------------------                                                           
        # END Region: Attributes
        # ----------------------
        d1 = self.d1_fun(S0=current_price,K=strike,r=ann_risk_free_rate,sigma=ann_volatility)
        d2 = self.d2_fun(S0=current_price,K=strike,r=ann_risk_free_rate,sigma=ann_volatility)

        




    def d1_fun(self,
                S0:float,
                    K:float,
                    r:float,
                    sigma:float,
                    divid:float=0)->float:
        """d1_fun _summary_

        _extended_summary_

        Parameters
        ----------
        S0 : float
            _description_
        K : float
            _description_
        r : float
            _description_
        sigma : float
            _description_
        divid : float, optional
            _description_, by default 0

        Returns
        -------
        float
            _description_
        """
        d1 = (np.log(S0 /K) + (
                r - divid + 0.5 * sigma ** 2) * self._year_fraction) / (
                     np.sqrt(self._year_fraction) * sigma)
        return d1

    #
    def d2_fun(self,S0:float,
                    K:float,
                    r:float,
                    sigma:float,
                    divid:float=0):
                
        d2 = (np.log(S0 / K) + (
                r - divid - 0.5 * sigma ** 2) * self.year_fraction) / (
                     np.sqrt(self.year_fraction) * sigma)
        return d2

    ####################################---- Plain Vanila ----

    def black_scholes_price_fun(self,
                                S0:float,
                                K:float,
                                divid:float,
                                r:float,
                                d1:float,
                                d2:float):
        """black_scholes_price_fun _summary_

        _extended_summary_

        Parameters
        ----------
        S0 : float
            _description_
        K : float
            _description_
        divid : float
            _description_
        r : float
            _description_
        d1 : float
            _description_
        d2 : float
            _description_

        Returns
        -------
        _type_
            _description_
        """
                               
        
        if (self._type_option == 'CALL'):
            price = S0 * np.exp(-self.year_fraction * divid) * sc.stats.norm.cdf(d1, 0,
                1) - K * np.exp(
                -self.year_fraction * r) * stats.norm.cdf(d2, 0, 1)
        else:
            price = K * np.exp(-self.year_fraction * r) * stats.norm.cdf(-d2, 0,1) - S0 * np.exp(-self.year_fraction * divid) * stats.norm.cdf(-d1, 0, 1)
        return price

    def digitalOption(self):
        """
        Description
        -----------
        This function retuns price of digital option where :math:`\int`


        Returns:
            float: This function returns price of digital option
        """
        
        if (self._type_option == 'call'):
            price = np.exp(-self.year_fraction * self._r) * sc.stats.norm.cdf(
                self.d2_fun(), 0, 1)
        else:
            price = np.exp(-self.year_fraction * self._r) * sc.stats.norm.cdf(
                -self.d2_fun(), 0, 1)
        return price

    def AssetorNothing(self):
        if (self._type_option == 'call'):
            price = self._S0 * np.exp(-self.year_fraction * self._divid) * sc.stats.norm.cdf(
                self.d1_fun(), 0, 1)
        else:
            price = self._S0 * np.exp(-self.year_fraction * self._divid) * sc.stats.norm.cdf(
                -self.d1_fun(), 0, 1)
        return price


#It is suitable for
class Black76(SetUpSchedule):
    def __init__(self, valuation_date, termination_date, calendar, year_fraction_convention, frequency,
                 type_option,forward, current_price, strike, ann_risk_free_rate, ann_volatility,
                 ann_dividend
                 ):
        SetUpSchedule.__init__(self, valuation_date, termination_date, calendar, year_fraction_convention, frequency)
        self._type_option = type_option  # call or put
        self._S0 = current_price
        self._K = strike
        self._r = ann_risk_free_rate
        self._sigma = ann_volatility
        self._divid = ann_dividend
        self._type_option = type_option  # call or put
        self._F = forward
        self._K = strike
        self._r = ann_risk_free_rate
        self._sigma = ann_volatility
        self._divid = ann_dividend

        self.mfd1 = self.d1Black76()
        self.mfd2 = self.d2Black76()
        self.blackprice = self.black76_price_fun()


    def d1Black76(self):
        d1 = (np.log(self._F / self._K) + (  0.5 * self._sigma ** 2) * self.ml_yf[0]) / (
                         np.sqrt(self.ml_yf) * self._sigma)
        return d1

    def d2Black76(self):
        d1 = (np.log(self._F / self._K) - (0.5 * self._sigma ** 2) * self.ml_yf[0]) / (
                np.sqrt(self.ml_yf) * self._sigma)
        return d1
    #TODO review the formula
    def black76_price_fun(self):
        if (self._type_option == 'call'):
            price = self._F * np.exp(-self.ml_yf[0] * self._divid) * sc.stats.norm.cdf(
                self.d1Black76(), 0,
                1) - self._K * np.exp(
                -self.ml_yf[0] * self._r) * stats.norm.cdf(self.d2Black76(), 0, 1)
        else:
            price = self._K * np.exp(-self.ml_yf[0] * self._r) * stats.norm.cdf(-self.d2Black76(), 0,
                                                                                1) - self._F * np.exp(
                -self.ml_yf[0] * self._divid) * stats.norm.cdf(-self.d1Black76(), 0, 1)
        return price


if __name__ == '__main__':
    os.chdir('/Users/krzysiekbienias/Documents/logger_files/')
    lb = LoggerBuilder()
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    log = lb.define_logger('Analytical_Price' + stamp)
    lb.logging_conf()



    o_black_scholes_short_maturity = AnalyticBlackScholes(valuation_date=dt.datetime(2022,4,7),
                                               termination_date=dt.datetime(2022,4,17),
                                               frequency='daily',
                                               year_fraction_convention='Actual365',  # Daily,Monthly,Quarterly
                                               calendar='USA',

                                               ##################################
                                               type_option='CALL',
                                               current_price=40,
                                               strike=38,
                                               ann_risk_free_rate=0.03,
                                               ann_volatility=0.23,
                                               ann_dividend=0)
    log.info('short maturity option {0}'.format(o_black_scholes_short_maturity.black_scholes_price_fun()))


    ######################################----3Month Option Setting----############################
    o_black_scholes_medium_maturity = AnalyticBlackScholes(valuation_date=datetime(2022, 4, 7),
                                                          termination_date=datetime(2022, 5, 7),
                                                          frequency='daily',
                                                          year_fraction_convention='Actual365',
                                                          # Daily,Monthly,Quarterly
                                                          calendar='USA',

                                                          ##################################
                                                          type_option='CALL',
                                                          current_price=40,
                                                          strike=38,
                                                          ann_risk_free_rate=0.03,
                                                          ann_volatility=0.23,
                                                          ann_dividend=0)
    log.info('medium maturity option {0}'.format(o_black_scholes_medium_maturity.black_scholes_price_fun()))

    ######################################----3Month Option Setting----############################


    ######################################----6Month Option Setting----############################
    o_black_scholes_long_maturity = AnalyticBlackScholes(valuation_date=datetime(2022, 4, 7),
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
    log.info('long maturity option {0}'.format(o_black_scholes_long_maturity.black_scholes_price_fun()))

    ######################################----3Month Option Setting----############################
    ######################################----6Month Option Setting----############################




































