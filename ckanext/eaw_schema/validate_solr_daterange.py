'''
Evaluates whether a date-time string conforms to
the DateRangeField specification of SOLR 5.4.
See https://cwiki.apache.org/confluence/display/solr/Working+with+Dates
Notes on its interpretation:
  + Points in time, i.e. not truncated or "implicit" ranges
    have to end with character "Z", indicating UTC.
  + "hh" for hours run from 00 to 23
  + This validator checks for valid dates considering leap years and
    assumes a Gregorian Calendar.
'''

import re
from ckan.plugins.toolkit import Invalid

class SolrDaterange(object):

    regex_elem = {'year': r'(?P<year>-?(0\d{3}|[1-9]\d{3,}))',
                  'month': r'(?P<month>\d{2})',
                  'day': r'(?P<day>\d{2})',
                  'hour': r'(?P<hour>([01][0-9]|2[0-3]))',
                  'minute': r'(?P<minute>[0-5][0-9])',
                  'second': r'(?P<second>[0-5][0-9](\.\d{3})?Z?)'
                  }
    
    regex_implicit_range = re.compile(
        '^(' + regex_elem['year'] +
        '(-' + regex_elem['month'] +
        '(-' + regex_elem['day'] +
        '(T' + regex_elem['hour'] +
        '(:' + regex_elem['minute'] +
        '(:' + regex_elem['second'] +
        r')?)?)?)?)?|(?P<wildcard>\*))$'
    )

    regex_explicit_range = re.compile(
        r'^\[(?P<start>[\-TZ:\.\d]{4,}|\*)' +
        r' TO (?P<end>[\-TZ:\.\d]{4,}|\*)\]$'
    )
    
    @staticmethod
    def _solregex(regex):
        return(re.compile('^' + regex + '$'))

    @staticmethod
    def _check_month_day_validity(datedict):

        def noleap(y):
            return(y % 4 != 0 or
                   (intyear % 100 == 0 and
                    intyear % 400 != 0))
        
        if datedict['wildcard'] == '*':
            return('*')
        intyear = int(datedict['year'])
        try:
            intmonth = int(datedict['month'])
        except TypeError:
            intmonth = None
        try:
            intday = int(datedict['day'])
        except TypeError:
            intday = None
        maxdays = [31, 28 if noleap(intyear) else 29,
                   31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if not (intmonth is None or 1 <= intmonth <= 12):
            raise Invalid("{} is not a valid month.".format(datedict['month']))
        if not (intday is None or 1 <= intday <= maxdays[intmonth - 1]):
            raise Invalid("{} is not a valid day.".format(datedict['day']))
        
    @classmethod
    def _check_date_element(cls, typ, elemstr):
        '''Checks an element of the DateRange string.
        <typ> = 'second', 'minute', hour', 'day', 'month', or 'year'.
        '''
        reg = cls.regex_elem[typ]
        matchres = re.match(cls._solregex(reg), elemstr)
        if matchres is None:
            raise Invalid("{}: not a valid {}".format(elemstr, typ))
        else:
            return(matchres.groupdict()[typ])

    @classmethod
    def _check_implicit_range(cls, rangestr):
        matchres = re.match(cls.regex_implicit_range, rangestr)
        if matchres is None:
            raise Invalid("{}: not a valid DateRange - field"
                             .format(rangestr))
        else:
            return(matchres.groupdict())

    @classmethod
    def _check_time_direction(cls, start, end):
        if start == '*' or end == '*':
            return
        if [start, end] != sorted([start, end]):
            raise Invalid("You inverted the arrow of time!\n" +
                          "{} < {}".format(end, start))
    
    @classmethod
    def validate(cls, datestr):
        parsed = {}
        try:
            d = re.match(cls.regex_explicit_range, datestr).groupdict()
        except AttributeError:
            cls._check_month_day_validity(cls._check_implicit_range(datestr))
        else:
            cls._check_month_day_validity(cls._check_implicit_range(d['start']))
            cls._check_month_day_validity(cls._check_implicit_range(d['end']))
            cls._check_time_direction(d['start'], d['end']) 
        return(datestr)

