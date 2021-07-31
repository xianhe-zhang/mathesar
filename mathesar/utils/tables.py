from mathesar.models import Table
from mathesar.imports.csv import create_table_from_csv
from mathesar.database.base import create_mathesar_engine
from db.tables import infer_table_column_types, create_mathesar_table, get_oid_from_table


def get_table_column_types(table):
    schema = table.schema
    types = infer_table_column_types(schema.name, table.name, schema._sa_engine)
    col_types = {
        col.name: t().compile(dialect=schema._sa_engine.dialect)
        for col, t in zip(table.sa_columns, types)
        if not col.is_default
        and not col.primary_key
        and not col.foreign_keys
    }
    return col_types


def create_table_from_datafile(data_files, name, schema):
    data_file = data_files[0]
    table = create_table_from_csv(data_file, name, schema)
    return table


def create_empty_table(name, schema):
    """
    Create an empty table, with only Mathesar's internal columns.

    :param name: the parsed and validated table name
    :param schema: the parsed and validated schema model
    :return: the newly created blank table
    """

    engine = create_mathesar_engine(schema.database.name)
    db_table = create_mathesar_table(name, schema.name, [], engine)
    db_table_oid = get_oid_from_table(db_table.name, db_table.schema, engine)
    table, _ = Table.objects.get_or_create(oid=db_table_oid, schema=schema)
    return table