import re
import datetime


class EraDate(object):
    """
    Class for work with BC dates in postgresql Date column type.

    Have parser to parse from database literal "YYYY-MM-DD BC".

    Other parsers should be written on demand.

    Have __int__ method (with comparison operators) to represent date in integer
    to compare it with other object of this class.

    Have as_db_literal method to cast object of this type to database literal.
    """
    # db_bc_pattern = r'([0-9]{4})-([0-9]{2})-([0-9]{2})([ ]?BC)?'
    # js_bc_pattern = r'(-[0-9]{2})?([0-9]{4})-([0-9]{2})-([0-9]{2})'
    db_bc_pattern = r'(-[0-9]{2})?([0-9]{4})-([0-9]{2})-([0-9]{2})([ ]?BC)?'

    def __init__(self, year, month=1, day=1):
        """
        It is possible to initialize object with only year.
        In this case default month (1) and day (1) will be used,
        because database requires year, month and day.
        """
        if year < 0:
            self.bc = True
            self.year = -year
        else:
            self.bc = False
            self.year = year

        self.month = month
        self.day = day

    @classmethod
    def parse(cls, db_string):
        """
        Parse database literal 'YYYY-MM-DD BC' or 'YYYY-MM-DD'.
        It also can parse incomplete date literal 'YYYY-MM' or 'YYYY BC' - not anymore
        """
        if db_string is None:
            return db_string

        match = re.match(cls.db_bc_pattern, db_string)
        if not match:
            raise ValueError("Invalid date string: \"{}\"".format(db_string))

        args, bc = map(int, match.groups()[1:-1]), match.groups()[0] or match.groups()[-1]
        # Validate
        datetime.date(*args)

        if bc:
            args[0] = -args[0]

        return cls(*args)

    def as_db_literal(self):
        """
        Builds string, valid to insert into database 'YYYY-MM-DD BC' or 'YYYY-MM-DD'
        """
        return_value = '{0:04}-{1:02}-{2:02}'.format(self.year, self.month, self.day)
        if self.bc:
            return_value += ' BC'

        return return_value

    def as_js_literal(self):
        """
        Builds string, valid to pass into javascript '-00YYYY-MM-DD' or 'YYYY-MM-DD'
        """
        return_value = '{0:04}-{1:02}-{2:02}'.format(self.year, self.month, self.day)
        if self.bc:
            return_value = '-00' + return_value

        return return_value

    def __str__(self):
        """
        TODO: Builds string to return to frontend. If date is BC date, then month and day
        are omitted from output string.
        At the moment returns as_db_literal()
        """
        # return_value = '{:04}'.format(self.year)
        # if self.bc:
        #     return_value += ' BC'
        # else:
        #     return_value += '-{0:01}-{1:01}'.format(self.month, self.day)
        # return return_value
        return self.as_db_literal()

    def __int__(self):
        """
        Returns int representation of object for comparison use only.
        """
        return_value = -400 * self.year if self.bc else 400 * self.year
        return_value += self.month * 31 + self.day

        return return_value

    def __repr__(self):
        return '<EraDate: {}>'.format(self.__str__())

    def __lt__(self, other):
        return self.__int__() < other.__int__()

    def __le__(self, other):
        return self.__int__() <= other.__int__()

    def __ge__(self, other):
        return not self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __eq__(self, other):
        if other is not None:
            return self.__int__() == other.__int__()
        else:
            return self.__int__() == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def as_datetime(self):
        """
        Just a placeholder, for future development.
        At the moment returns datetime.date if date is not BC, else returns None.
        """
        if not self.bc:
            return datetime.date(self.year, self.month, self.day)
        else:
            raise Exception("This is BC date, datetime does not support BC dates.")
