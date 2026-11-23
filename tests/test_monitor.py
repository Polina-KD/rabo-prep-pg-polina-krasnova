from pg_ops.monitor import check_connections, check_database_size, check_replication_lag


def test_connections():
    assert check_connections(10, 100) == "OK"
    assert check_connections(81, 100) == "WARNING"


def test_replication_lag():
    assert check_replication_lag(0) == "OK"
    assert check_replication_lag(20 * 1024 * 1024) == "WARNING"
    assert check_replication_lag(None) == "WARNING"


def test_database_size():
    assert check_database_size(10 * 1024 * 1024) == "OK"
    assert check_database_size(2 * 1024**3) == "WARNING"
