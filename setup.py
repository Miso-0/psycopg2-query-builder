from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Sql/Postgresql query builder, inspired by the Supabase client SDK functions.'
LONG_DESCRIPTION = ('QueryBuilder is a lightweight Python package designed to simplify building SQL queries when using '
                    'the Psycopg2 library to interact with PostgreSQL databases. Inspired by Supabase\'s client SDKs, '
                    'QueryBuilder aims to provide an intuitive and fluid API for constructing and executing SQL '
                    'queries.')

# Setting up
setup(
    name="psycopg2-query-builder",
    version=VERSION,
    author="Miso Menze",
    author_email="<misomenze6@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['psycopg2-binary', 'psycopg2'],
    keywords=['python', 'sql', 'postgresql', 'query', 'builder', 'database'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
