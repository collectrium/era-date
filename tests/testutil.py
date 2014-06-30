# Configure the test suite from the env variables.

import os
from sqlalchemy.engine.url import URL

postgresql_db_credentials = {
    'name': os.environ.get('ERADATE_TEST_DB_NAME', 'eradate_test'),
    'host': os.environ.get('ERADATE_TEST_DB_HOST', None),
    'port': os.environ.get('ERADATE_TEST_DB_PORT', None),
    'user': os.environ.get('ERADATE_TEST_DB_USER', None),
    'password': os.environ.get('ERADATE_TEST_DB_PASSWORD', None)
}

sqlalchemy_url = URL(drivername='postgresql',
                     database=postgresql_db_credentials['name'],
                     host=postgresql_db_credentials['host'],
                     port=postgresql_db_credentials['port'],
                     username=postgresql_db_credentials['user'],
                     password=postgresql_db_credentials['password'])
