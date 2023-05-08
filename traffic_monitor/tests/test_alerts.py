import pytest
from traffic_monitor.log import Log
import traffic_monitor.monitor as monitor

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

    monitor.high_traffic = False
    monitor.zero_timestamp = logs[0].timestamp

    reqs_per_sec, high_traffic = monitor.alerts(logs, 10)
    
    assert reqs_per_sec == 22
    assert high_traffic == True

def test_alert_back_to_normal():
    """Test alerts"""

    monitor.high_traffic = True
    monitor.zero_timestamp = logs[8].timestamp

    reqs_per_sec, high_traffic = monitor.alerts(logs[8:15], 10)
    
    assert reqs_per_sec < 10
    assert high_traffic == False

def test_alert_one_log_only():
    """Test alerts"""

    monitor.high_traffic = True
    monitor.zero_timestamp = logs[0].timestamp

    reqs_per_sec, high_traffic = monitor.alerts([Log("10.0.0.3","-","apache",1549573860,"GET /report HTTP/1.0",200,1194)], 1)
    
    assert reqs_per_sec == 1
    assert high_traffic == False

def test_alert_empty_logs():
    """Test alerts"""

    monitor.high_traffic = True
    monitor.zero_timestamp = None

    reqs_per_sec, high_traffic = monitor.alerts([], 1)
    
    assert reqs_per_sec == 0
    assert high_traffic == monitor.high_traffic

def test_alert_threshold_zero():
    """Test alerts"""

    monitor.high_traffic = False
    monitor.zero_timestamp = logs[0].timestamp

    reqs_per_sec, high_traffic = monitor.alerts(logs, 0)
    
    assert reqs_per_sec > 0
    assert high_traffic == True

def test_alert_threshold_negative():
    """Test alerts"""

    monitor.high_traffic = False
    monitor.zero_timestamp = logs[0].timestamp

    reqs_per_sec, high_traffic = monitor.alerts(logs, -1)
    
    assert reqs_per_sec > -1
    assert high_traffic == True

def test_alert_raise_exception():
    """Test alerts"""

    monitor.high_traffic = False
    monitor.zero_timestamp = None

    with pytest.raises(TypeError):
        reqs_per_sec, high_traffic = monitor.alerts(logs, 1)




