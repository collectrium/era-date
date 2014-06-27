import unittest

from sqlalchemy import Column, Integer, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from eradate import define_eradate_type_casts, EraDate
from testutil import sqlalchemy_url, postgresql_db_credentials

class EraDateDatabaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(EraDateDatabaseTest, cls).setUpClass()
        cls.dateliteral_bc_lower = "3000-05-20 BC"
        cls.dateliteral_bc_higher = "0009-10-19 BC"
        cls.dateliteral_ad = "0085-06-03"

        define_eradate_type_casts(postgresql_db_name=postgresql_db_credentials['name'],
                                  postgresql_db_user=postgresql_db_credentials['user'],
                                  postgresql_db_password=postgresql_db_credentials['password'],
                                  postgresql_db_host=postgresql_db_credentials['host'],
                                  postgresql_db_port=postgresql_db_credentials['port'])

        cls.engine = create_engine(sqlalchemy_url)

        cls.Base = declarative_base()
        cls.tablename = 'DBEraDates'
        class DBEraDate(cls.Base):
            __tablename__ = cls.tablename

            id = Column(Integer, primary_key=True)
            date = Column(Date)

        cls.DBEraDateClass = DBEraDate
        # Ensure removal of table from previous tests
        try:
            cls.Base.metadata.tables[cls.tablename].drop(cls.engine)
        except:
            pass
        cls.Base.metadata.tables[cls.tablename].create(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        super(EraDateDatabaseTest, self).setUp()
        self.session = self.Session()

    def test_bc_dates_with_database(self):
        date_bc_lower = EraDate.parse_from_db_literal(self.dateliteral_bc_lower)
        date_bc_higher = EraDate.parse_from_db_literal(self.dateliteral_bc_higher)
        date_ad = EraDate.parse_from_db_literal(self.dateliteral_ad)

        # Check insertion without errors.
        date_object_bc_lower = self.DBEraDateClass(date=date_bc_lower)
        date_object_bc_higher = self.DBEraDateClass(date=date_bc_higher)
        date_object_ad = self.DBEraDateClass(date=date_ad)
        self.session.add_all([date_object_bc_lower, date_object_bc_higher, date_object_ad])
        self.session.commit()

        # Check presence of inserted objects in database.
        result = self.session.query(self.DBEraDateClass).all()
        self.assertEqual(len(result), 3)
        # Check correct type cast
        for index in range(len(result)):
            self.assertEqual(type(result[index].date), EraDate)

        # Check usage of filter and attribute select.
        result = self.session.query(self.DBEraDateClass.date).filter(self.DBEraDateClass.date == date_bc_higher).first()
        result = result[0]
        self.assertEqual(type(result), EraDate)
        self.assertEqual(result, date_bc_higher)
        self.assertEqual(result, EraDate.parse_from_db_literal(self.dateliteral_bc_higher))
        self.assertEqual(result.as_db_literal(), self.dateliteral_bc_higher)

        result = self.session.query(self.DBEraDateClass).filter(self.DBEraDateClass.date < date_bc_higher).all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, date_bc_lower)

        # Check usage of order_by.
        result = self.session.query(self.DBEraDateClass).order_by(self.DBEraDateClass.date).all()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].date, date_bc_lower)
        self.assertEqual(result[1].date, date_bc_higher)
        self.assertEqual(result[2].date, date_ad)

        result = self.session.query(self.DBEraDateClass).order_by(self.DBEraDateClass.date.desc()).all()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[2].date, date_bc_lower)
        self.assertEqual(result[1].date, date_bc_higher)
        self.assertEqual(result[0].date, date_ad)

        # Check deletion
        self.session.delete(result[0])
        result = self.session.query(self.DBEraDateClass).all()
        self.assertEqual(len(result), 2)

        result = self.session.query(self.DBEraDateClass).filter(self.DBEraDateClass.date == date_ad).all()
        self.assertEqual(len(result), 0)

        self.session.query(self.DBEraDateClass).delete()
        result = self.session.query(self.DBEraDateClass).all()
        self.assertEqual(len(result), 0)

    def tearDown(self):
        super(EraDateDatabaseTest, self).tearDown()
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        super(EraDateDatabaseTest, cls).tearDownClass()
        cls.Base.metadata.tables[cls.tablename].drop(cls.engine)
