import pytest
from rest_framework.test import APIClient

from mathesar.imports.csv import create_table_from_csv


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_table(engine, csv_filename):
    def _create_table(table_name):
        with open(csv_filename, 'rb') as csv_file:
            create_table_from_csv(
                name=table_name,
                schema='Patents',
                database_key='mathesar_db_test_database',
                csv_file=csv_file
            )

    return _create_table
