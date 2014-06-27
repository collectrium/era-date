def define_eradate_type_casts(postgresql_db_name,
                              postgresql_db_user=None,
                              postgresql_db_password=None,
                              postgresql_db_host=None,
                              postgresql_db_port=None):
    """
    Function to define type casts in database driver (psycopg2), to avoid
    cast of database type DATE to python type datetime.date, as datetime.date
    does not support BC dates.

    It does not store type casts, so it needs to be called for every python session.

    Requires database (postgresql) credentials as arguments.
    """
    import psycopg2
    from eradate_module import EraDate

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

    conn = psycopg2.connect(database=postgresql_db_name,
                            user=postgresql_db_user,
                            password=postgresql_db_password,
                            host=postgresql_db_host,
                            port=postgresql_db_port)
    register_era_date(conn)
