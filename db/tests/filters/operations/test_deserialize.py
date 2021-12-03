from db.filters.operations.deserialize import get_predicate_from_MA_filter_spec
from db.filters.base import And, Or, Not, Equal, Empty, In


def test_deserialize():
    ma_filter_spec = {"and": [
        {"not":
            {"empty": {"column": "col1"}}},
        {"or": [
            {"equal": {"column": "col2", "parameter": 15}},
            {"in": {"column": "col3", "parameters": [1, 2, 3]}},
        ]}]}
    expected_predicate = And([
        Not(
            Empty(column="col1")
        ),
        Or([
            Equal(column="col2", parameter=15),
            In(column="col3", parameters=[1, 2, 3]),
        ]),
    ])
    predicate = get_predicate_from_MA_filter_spec(ma_filter_spec)
    assert predicate == expected_predicate