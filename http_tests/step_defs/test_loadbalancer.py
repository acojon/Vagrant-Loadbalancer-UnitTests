import pytest
import requests
import socket

from pytest_bdd import scenarios, given, when, then, parsers

# How many seconds to wait when using socket to connect to a port before
# failing.
timeout = 3

load_balancer_host = "site.fake.com"

load_balancer_ip = socket.gethostbyname(load_balancer_host)
load_balancer_url = {
    "80": "http://site.fake.com:80",
    "443": "https://site.fake.com:443"
}

# Scenerios
scenarios('../features/lb.feature')

# Fixtures
def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

@given('The Load Balancer is Online')
def load_balancer():
    """Given: The Load Balancer is Online."""


@when(parsers.re(r'I go to port "(?P<port>\d+)" on the Load Balancer'))
def lb_port(port):
    """When: I go to port ## on the Load Balancer."""


@then(parsers.re(r'a status code of 200 is returned for port "(?P<port>\d+)"'))
def port_online(port):
    """Then: a status code of 200 is returned"""
    assert isOpen(load_balancer_ip, port)

    r = requests.get(load_balancer_url[port])
    assert r.status_code == 200
