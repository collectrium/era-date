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

Notes
=====

The EraDate class doesn't have any validators yet, as at first it was created only as wrapper for postgresql
Date type.

Tests are in eradate/test_eradate.py.

You can make psycopg2 postgresql driver return eradate object from Date type column, and vice versa by this way:

    def define_eradate_type_casts():
        """
        Function to define type casts in database driver (psycopg2), to avoid
        cast of database type DATE to python type datetime.date, as datetime.date
        does not support BC dates.

        It does not store type casts, so it needs to be called for every python session.
        """
        import psycopg2

        """
        Cast PostgreSQL BC date into EraDate object
        http://initd.org/psycopg/docs/advanced.html#type-casting-from-sql-to-python
        This function dafines types cast, from returned from database literal to EraDate object.
        """
        def cast_era_date(value, cursor):
            return EraDate.parse_from_db_literal(value)

        """
        Adapt func. Function to cast object of custom python class to postgresql literal
        http://initd.org/psycopg/docs/advanced.html#adapting-new-python-types-to-sql-syntax
        """
        def adapt_era_date(obj):
            return psycopg2.extensions.AsIs(psycopg2.extensions.adapt(obj.as_db_literal()))

        def register_era_date(connection):
            cursor = connection.cursor()
            cursor.execute('SELECT NULL::date')
            psql_date_oid = cursor.description[0][1]

            NewDate = psycopg2.extensions.new_type((psql_date_oid,), 'DATE', cast_era_date)
            psycopg2.extensions.register_type(NewDate)
            psycopg2.extensions.register_adapter(EraDate, adapt_era_date)

        conn = psycopg2.connect(database=POSTGRESQL_YOUR_DBNAME,
                                user=POSTGRESQL_YOUR_USERNAME,
                                password=POSTGRESQL_YOUR_PASSWORD,
                                host=POSTGRESQL_YOUR_HOST,
                                port=POSTGRESQL_YOUR_PORT)
        register_era_date(conn)
