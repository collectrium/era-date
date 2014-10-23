from setuptools import setup

try:
    __long_description__ = open('README.md').read()
except:
    __long_description__ = ''

setup(
    name='eradate',
    version='0.1.2',
    license='private',
    description='Date util to work with BC dates and postgresql Date.',
    long_description=__long_description__,
    author='',
    author_email='',
    url='http://github.com/collectrium/era-date',
    install_requires=[
        # It was not tested on earlier versions of psycopg2 or sqlalchemy.
        'psycopg2>=2.5.3',
        'SQLAlchemy>=0.9.4'
    ],
    packages=['eradate'],
    zip_safe=False,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
