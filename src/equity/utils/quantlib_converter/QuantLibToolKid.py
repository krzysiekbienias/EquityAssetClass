
import QuantLib as ql
from equity.utils.logger.LoggerUtils import LoggerBuilder




class QuantLibConverter:
    def __init__(self, calendar):

        '''

        :param calendar: name of calendar according to which holidays are find
        :type calendar: string
        '''
        self._calendar = calendar
        self.mqlCalendar = self.setCalendar(country=self._calendar)
        self.mqlBusinessConvention = self.setBusinessConvention()
        self.mqlTerminationBusinessConvention = self.setTerminationBusinessConvention()
        self.mqlDateGeneration = self.setRuleOfDateGeneration()

    def setCalendar(self,country):
        '''

        :param country: Name of the country for which we would like to follow.
        :return: quanlib calendar
        '''
        if country == 'USA':
            return ql.UnitedStates()
        if country == 'United Kingdom':
            return ql.UnitedKingdom()
        if country == 'Switzerland':
            return ql.Switzerland()
        if country == 'Poland':
            return ql.Poland()

    def setBusinessConvention(self):
        '''

        :return: function defines business convention. It is argument requited for schedule object
        :rtype: int
        '''
        result=ql.Following
        return result

    def setTerminationBusinessConvention(self):
        '''

        :return: function defines business convention. It is argument requited for schedule object
        :rtype: int
        '''
        result=ql.Following
        return result

    def setRuleOfDateGeneration(self):
        '''

        :return:
        :rtype: int
        '''
        return ql.DateGeneration.Forward

    def setFrequency(self,freq_period):

        if freq_period=='daily':
            return ql.Daily
        if freq_period=='once':
            return ql.Once
        if freq_period=='monthly':
            return ql.Monthly
        if freq_period=='quarterly':
            return ql.Quarterly
        if freq_period=='annual':
            return ql.Annual
        if freq_period=='semiannual':
            return ql.Semiannual


if __name__ == '__main__':
    quallib_conv=QuantLibConverter(calendar='United Kingdom')
    print('The End')