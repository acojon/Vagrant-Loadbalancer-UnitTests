# coding=utf-8
"""features/lb.feature feature tests."""

from pytest_bdd import (
    given,
    scenarios,
    then,
    when,
    parsers,
)

import pytest
import requests
import socket

scenario_path = "../features/lb.feature"
scenarios(scenario_path)

# How many seconds to wait when using socket to connect to a port before
# failing.
timeout = 3

load_balancer_host = "site.fake.com"

load_balancer_ip = socket.gethostbyname(load_balancer_host)
load_balancer_url = {
    "80": "http://site.fake.com:80",
    "443": "https://site.fake.com:443"
}


def isOpen(ip, port):
    '''
    This function uses the socket library to connect to the referenced
    ip_address on the referenced port.  If the connection is successful, the
    function returns True.  Otherwise the function returns False.
    '''
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


@then(parsers.re(r'I do not get a response from port "(?P<port>\d+)"'))
def port_offline(port):
    """Then: I do not get a response."""
    assert not isOpen(load_balancer_ip, port)

