era-date
========

Description
===========

This module was written to work with dates (including BC) from postgresql database type Date (which supports BC dates).

Potentially this module should have functional of python datetime.date module, with addition of BC dates.

At the moment all functional that presents is:
* parsing date string from postgresql database,
* generating date string for postgresql database,
* compare date objects with each other.

Examples
========

Python class
============

Instantiate eradate objects:

    from eradate.eradate import EraDate

By providing year, month and day values (year is negative for BC date):

    ad_date = EraDate(2014, 5, 20)
    bc_date = EraDate(-1500, 10, 1)

Or only year or year and month. Not provided values will be replaced with default 1:

    ad_date_incomplete = EraDate(1990)
    bc_date_incomplete = EraDate(-500, 8)

Or by providing string to parse. String format corresponds with such in postgresql Date type.
"YYYY-MM-DD" or "YYYY-MM-DD BC"

    ad_date_parsed = EraDate.parse_from_db_literal("2014-05-20")
    bc_date_parsed = EraDate.parse_from_db_literal("1500-10-01 BC")

Compare eradate objects:

    print ad_date < bc_date # True
    print ad_date == ad_date_parsed # True
    print ad_date_incomplete < bc_date_parsed # False

Get string for database (which will be in correct format):

    print ad_date.as_db_literal() # 2014-05-20
    print bc_date.as_db_literal() == "1500-10-01 BC" # true

You can access year, month and day attributes (if date is BC, year will be positive, and flag bc will be True):

    print ad_date.year, ad_date.month, ad_date.day, ad_date.bc # 2014 5 20 False
    print bc_date.year, bc_date.month, bc_date.day, bc_date.bc # 1500 10 1 True

Work with database
==================

With EraDate class and defined type casts to work with BC dates the default column type Date
from sqlalchemy can be used. For example, following model will work perfectly:

    Base = declarative_base()

    class EraDate(Base):
        __tablename__ = 'EraDates'

        id = Column(Integer, primary_key=True)
        date = Column(Date)

        def __repr__(self):
            return "<EraDate(date='{0}', id='{1}')>".format(self.date, self.id)

Date field will return EraDate object.
Inserts will work:

    EraDate_0 = EraDate(date=EraDate.parse_from_db_literal("0010-01-01 BC"))
    EraDate_1 = EraDate()
    EraDate_1.date = EraDate(-2000, 10, 25)
    session.add_all([EraDate_0, EraDate_1])
    session.commit()

Queries with filter will work:

    result = session.query(EraDate).filter(EraDate.date == EraDate(-10, 1, 1)).first()
    print result.date # <EraDate: 0010-01-01 BC>
    result = session.query(EraDate.date).filter(EraDate.date == EraDate.parse_from_db_literal("2000-10-25 BC")).all()
    print result[0] # <EraDate: 2000-10-25 BC>
    print result[0].as_db_literal() # 2000-10-25 BC

As mentioned above, EraDate can be initialized with year only, and can parse noncomplete literals:

    result = session.query(EraDate).filter(EraDate.date > EraDate(1990)).all()
    print result # []
    result = session.query(EraDate.date).filter(EraDate.date <= EraDate.parse_from_db_literal("1900 BC")).all()
    print result[0].as_db_literal() # 2000-10-25 BC

although in these cases result can be unexpected, as EraDate will use default month and day if not provided,
which means that EraDate(1990) is actually EraDate(1990, 1, 1) and 
EraDate.parse_from_db_literal("2000 BC") will return same as EraDate.parse_from_db_literal("2000-01-01 BC")

Queries with order_by will work:

    result = session.query(EraDate).order_by(EraDate.date).all()
    print [dt.as_db_literal() for dt in result] # ["2000-10-25 BC", "0010-01-01 BC"]
    result = session.query(EraDate).order_by(EraDate.date.desc()).all()
    print [dt.as_db_literal() for dt in result] # ["0010-01-01 BC", "2000-10-25 BC"]

Notes
=====

The EraDate class doesn't have any validators yet, as at first it was created only as wrapper for postgresql
Date type.

Tests can be found in tests.
To run db tests on local machine, you need to specify db credentials in environment:
ERADATE_TEST_DB_NAME, 
ERADATE_TEST_DB_HOST, 
ERADATE_TEST_DB_PORT, 
ERADATE_TEST_DB_USER, 
ERADATE_TEST_DB_PASSWORD.
