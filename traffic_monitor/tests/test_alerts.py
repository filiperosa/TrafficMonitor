import pytest
from traffic_monitor.log import Log
from traffic_monitor.log_collection import LogCollection
from traffic_monitor import alerts

# Create a list of logs
logs = [
    Log("10.0.0.2","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234),
    Log("10.0.0.4","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234),
    Log("10.0.0.4","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234),
    Log("10.0.0.2","-","apache",1549573860,"GET /api/help HTTP/1.0",200,1234),
    Log("10.0.0.5","-","apache",1549573860,"GET /api/help HTTP/1.0",200,1234),
    Log("10.0.0.5","-","apache",1549573860,"POST /report HTTP/1.0",500,1307),
    Log("10.0.0.3","-","apache",1549573860,"POST /report HTTP/1.0",200,1234),
    Log("10.0.0.3","-","apache",1549573860,"GET /api/help HTTP/1.0",200,1234),
    Log("10.0.0.3","-","apache",1549573860,"GET /report HTTP/1.0",200,1194),
    Log("10.0.0.5","-","apache",1549573860,"GET /api/help HTTP/1.0",200,1234),
    Log("10.0.0.5","-","apache",1549573860,"GET /api/help HTTP/1.0",200,1234),
    Log("10.0.0.4","-","apache",1549573861,"GET /api/user HTTP/1.0",200,1136),
    Log("10.0.0.5","-","apache",1549573861,"GET /api/user HTTP/1.0",200,1194),
    Log("10.0.0.1","-","apache",1549573861,"GET /api/user HTTP/1.0",200,1261),
    Log("10.0.0.2","-","apache",1549573861,"GET /api/help HTTP/1.0",200,1194),
    Log("10.0.0.2","-","apache",1549573861,"GET /report HTTP/1.0",200,1136),
    Log("10.0.0.5","-","apache",1549573861,"POST /report HTTP/1.0",200,1136),
    Log("10.0.0.5","-","apache",1549573861,"GET /api/user HTTP/1.0",200,1194),
    Log("10.0.0.1","-","apache",1549573861,"GET /api/user HTTP/1.0",200,1261),
    Log("10.0.0.2","-","apache",1549573861,"GET /api/help HTTP/1.0",200,1194),
    Log("10.0.0.2","-","apache",1549573861,"GET /report HTTP/1.0",200,1136),
    Log("10.0.0.5","-","apache",1549573861,"POST /report HTTP/1.0",200,1136),
]


def test_alert_high_traffic():
    """Test alerts"""

    alerts.high_traffic = False
    log_window = LogCollection(logs)
    reqs_per_sec, high_traffic = alerts.check_high_traffic(log_window, 10)
    
    assert reqs_per_sec == 22
    assert high_traffic == True

def test_alert_back_to_normal():
    """Test alerts"""

    alerts.high_traffic = True

    reqs_per_sec, high_traffic = alerts.check_high_traffic(LogCollection(logs[8:15]), 10)
    
    assert reqs_per_sec < 10
    assert high_traffic == False

def test_alert_one_log_only():
    """Test alerts"""

    alerts.high_traffic = True
    log_window = LogCollection([Log("10.0.0.3","-","apache",1549573860,"GET /report HTTP/1.0",200,1194)])
    reqs_per_sec, high_traffic = alerts.check_high_traffic(log_window, 1)
    
    assert reqs_per_sec == 1
    assert high_traffic == False

def test_alert_empty_logs():
    """Test alerts"""

    alerts.high_traffic = True

    reqs_per_sec, high_traffic = alerts.check_high_traffic(LogCollection(), 1)
    
    assert reqs_per_sec == 0
    assert high_traffic == alerts.high_traffic

def test_alert_threshold_zero():
    """Test alerts"""

    alerts.high_traffic = False
    log_window = LogCollection(logs)
    reqs_per_sec, high_traffic = alerts.check_high_traffic(log_window, 0)
    
    assert reqs_per_sec > 0
    assert high_traffic == True

def test_alert_threshold_negative():
    """Test alerts"""

    alerts.high_traffic = False
    log_window = LogCollection(logs)
    reqs_per_sec, high_traffic = alerts.check_high_traffic(log_window, -1)
    
    assert reqs_per_sec > -1
    assert high_traffic == True

def test_alert_raise_exception():
    """Test alerts"""

    alerts.high_traffic = False
    log_window = LogCollection(logs)
    with pytest.raises(TypeError):
        reqs_per_sec, high_traffic = alerts.check_high_traffic(log_window, "a")




