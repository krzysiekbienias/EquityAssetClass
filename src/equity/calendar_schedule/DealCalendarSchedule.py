import os
import QuantLib as ql
import pandas as pd
from datetime import datetime
import os, sys 

from equity.utils.logger.LoggerUtils import LoggerBuilder
from equity.utils.quantlib_converter.QuantLibToolKid import QuantLibConverter



class SetUpSchedule():
    
    
    def __init__(self, valuation_date,
                 termination_date,
                 calendar,
                 year_fraction_convention,
                 frequency,
                 **kwargs):
        """

        This class enable to create scedule calandar to reflect trade attributes related to its lifecycle and important events.

        Parameters
        ----------
        valuation_date : datetime
            
        termination_date : datetime
            
        calendar : string
            
        year_fraction_convention : string
            
        frequency : _type_
            
        Examples  
        >>>   
        """
                 
                     
        self._dt_valuation_date = valuation_date
        self._dt_termination_date = termination_date
        self._s_calendar = calendar
        self._s_year_fraction_conv=year_fraction_convention
        self._s_frequency=frequency

        self.m_ql_valuation_date = self.convertDateIntoqlDate(date=self._dt_valuation_date)
        self.m_ql_termination_date = self.convertDateIntoqlDate(date=self._dt_termination_date)
        self.m_year_fraction_conv = self.setYearFractionConvention(year_fraction_conv=self._s_year_fraction_conv)



        quantliBConverter = QuantLibConverter(calendar=self._s_calendar)
        self.int_freq = quantliBConverter.setFrequency(freq_period=self._s_frequency)
        self.ql_calendar = quantliBConverter.setCalendar(country=self._s_calendar)
        self.m_schedule = self.setSchedule()  # simpler or standard
        self.ml_dates = self.getListOfDates()
        self.dt_l_dates=[datetime(d.year(),d.month(),d.dayOfMonth()).date() for d in self.ml_dates]


        self.ql_business_convention = quantliBConverter.setBusinessConvention(),
        self.ql_termination_business_convention = quantliBConverter.setTerminationBusinessConvention()
        self.ql_rule = quantliBConverter.setRuleOfDateGeneration()



    def convertDateIntoqlDate(self, date):
        """convertDateIntoqlDate 
        Description
        -----------
        Function converts date object into quantlib date object into

        Parameters
        ----------
        date : datetime
            Date is in the format year, month, day

        Returns
        -------
        ql.Date
        
        Examples
        --------
        here we put example.
        """
        

        ql_date = ql.Date(date.day, date.month, date.year)
        return ql_date

    def setYearFractionConvention(self, year_fraction_conv):
        """setYearFractionConvention 

        Function defines how we will calculate year fraction.

        Parameters
        ----------
        year_fraction_conv : string
             Available alternatives: Actual360, Actual365, ActualActual, Thirty360, Business252
             

        Returns
        -------
        ql.FractionConvention
            
        """
        if (year_fraction_conv == 'Actual360'):
            day_count = ql.Actual360()
            return day_count
        elif (year_fraction_conv == 'Actual365'):
            day_count = ql.Actual365Fixed()
            return day_count
        elif (year_fraction_conv == 'ActualActual'):
            day_count = ql.ActualActual()
            return day_count
        elif (year_fraction_conv == 'Thirty360'):
            day_count = ql.Thirty360()
            return day_count
        elif (year_fraction_conv == 'Business252'):
            day_count = ql.Business252()
            return day_count

    def setSchedule(self):
        """setSchedule _summary_

        Function defines quantLib schedule that anables schedule trade calendar.

        Returns
        -------
        ql.Schedule
            
        """

        try:
            simpler_schedule = ql.MakeSchedule(effectiveDate=self.m_ql_valuation_date,
                                               terminationDate=self.m_ql_termination_date,
                                               frequency=self.int_freq,
                                               calendar=self.ql_calendar)
            print('We have created schedule object')
            return simpler_schedule
        except:
            print('Failed create schedule object')


    def getListOfDates(self):
        return list(self.m_schedule)

    def consequitiveDatesYearFraction(self):
        lf_year_fraction=[]
        for i in range(1,len(self.ml_dates)):
            temp_yf=self.m_year_fraction_conv.yearFraction(self.ml_dates[i-1],self.ml_dates[i])
            lf_year_fraction.append(temp_yf)
        return lf_year_fraction

    def startEndYearFraction(self):
        sched=ql.MakeSchedule(effectiveDate=self.m_ql_valuation_date,
                        terminationDate=self.m_ql_termination_date,
                        frequency=ql.Once,
                        calendar=self.ql_calendar)
        return list(sched)




class FlexibeScheduleGivingTenors:
    def __init__(self, tradeDate: str, tenors, roll_convention, callendar, convention):
        self._tradeDate = tradeDate
        self._tenors = tenors
        self._rolling_convention = roll_convention
        self._ql_calendar = callendar
        self.s_days_conv = convention

        self.m_ql_valuation_date = self.convert_string_into_ql_object(date=self._tradeDate)
        self.mSpotDate = self.setSpotDate(lag=0)
        self.mlTenorsDates = self.tenors_to_date()
        self.mSetSchedule = ql.Schedule(self.tenors_to_date(), self._ql_calendar, self._rolling_convention)
        self.m_day_count = self.set_days_convention(give_name=self.s_days_conv)
        self.ml_dates = self.get_list_of_dates()
        self.ml_yf = self.consecutive_year_fractions()  # two consecutive dates year fraction
        self.ml_yfFromSpotDate = self.fromSpotYearFraction()
        # self.mf_yf_between_valu_date_and_maturity = self.year_fraction_between_valuation_and_maturity()

    def setSpotDate(self, lag):
        return self.m_ql_valuation_date + ql.Period(lag)

    def convert_string_into_ql_object(self, date):
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:])
        ql_date = ql.Date(day, month, year)
        return ql_date

    def tenors_to_date(self, arguments=None):
        matur_date = []
        if arguments == None:

            for i in range(len(self._tenors)):
                if self._tenors[i][1] == 'Days':
                    temp = self.m_ql_valuation_date + ql.Period(self._tenors[i][0])
                    matur_date.append(temp)
                else:

                    temp = self.m_ql_valuation_date + ql.Period(self._tenors[i][0], self._tenors[i][1])
                    matur_date.append(temp)
        else:
            for i in range(len(arguments)):
                if arguments[i][1] == 'Days':
                    temp = self.m_ql_valuation_date + ql.Period(arguments[i][0])
                    matur_date.append(temp)
                else:

                    temp = self.m_ql_valuation_date + ql.Period(arguments[i][0], arguments[i][1])
                    matur_date.append(temp)

        return matur_date

    def get_list_of_dates(self):
        return list(self.mSetSchedule)

    def set_days_convention(self, give_name):
        if (give_name == 'Actual360'):
            day_count = ql.Actual360()
            return day_count
        elif (give_name == 'Actual365'):
            day_count = ql.Actual365Fixed()
            return day_count
        elif (give_name == 'ActualActual'):
            day_count = ql.ActualActual()
            return day_count
        elif (give_name == 'Thity360'):
            day_count = ql.Thirty360()
            return day_count
        elif (give_name == 'Business252'):
            day_count = ql.Business252()
            return day_count

    def consecutive_year_fractions(self):
        day_count = self.m_day_count
        l_yf = []
        for i in range(1, len(self.ml_dates)):
            temp = day_count.yearFraction(self.ml_dates[i - 1], self.ml_dates[i])
            l_yf.append(temp)

        return l_yf

    def fromSpotYearFraction(self):
        day_count = self.m_day_count
        l_yf = []
        for i in range(0, len(self.ml_dates)):
            temp = day_count.yearFraction(self.mSpotDate, self.ml_dates[i])
            l_yf.append(temp)
        return l_yf


if __name__ == '__main__':
    os.chdir('/Users/krzysiekbienias/Documents/logger_files/')
    lb = LoggerBuilder()
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    log = lb.define_logger('Calendar_schedule' + stamp)
    lb.logging_conf()

    calendar_schedule = SetUpSchedule(valuation_date=datetime(2022, 4, 10),
                                      termination_date=datetime(2022, 7, 10),
                                      frequency='daily',
                                      year_fraction_convention='Actual365',

                                      calendar='USA')


