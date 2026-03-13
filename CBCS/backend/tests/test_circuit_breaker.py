import pytest
from backend.core.circuit_breaker import circuit_breaker

def test_circuit_breaker_under_limit():
    user_id = "u_safe"
    circuit_breaker.reset_cost(user_id)
    circuit_breaker.track_cost(user_id, 1.50)
    
    assert circuit_breaker.should_downgrade(user_id) is False

def test_circuit_breaker_over_limit():
    user_id = "u_expensive"
    circuit_breaker.reset_cost(user_id)
    circuit_breaker.track_cost(user_id, 3.50)
    circuit_breaker.track_cost(user_id, 0.60) # Total 4.10
    
    assert circuit_breaker.should_downgrade(user_id) is True

def test_circuit_breaker_reset():
    user_id = "u_reset"
    circuit_breaker.reset_cost(user_id)
    circuit_breaker.track_cost(user_id, 5.00)
    assert circuit_breaker.should_downgrade(user_id) is True
    
    circuit_breaker.reset_cost(user_id)
    assert circuit_breaker.should_downgrade(user_id) is False
