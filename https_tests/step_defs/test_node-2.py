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

scenario_path = "../features/webserver.feature"
scenarios(scenario_path)

# How many seconds to wait when using socket to connect to a port before
# failing.
timeout = 3

webserver_host = "node-2"

webserver_ip = socket.gethostbyname(webserver_host)
webserver_url = {
    "80": "http://node-2:80",
    "443": "https://node-2:443"
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


@given('The webserver is Online')
def webserver():
    """Given: The webserver is Online."""


@when(parsers.re(r'I go to port "(?P<port>\d+)" on the webserver'))
def lb_port(port):
    """When: I go to port ## on the webserver."""


@then(parsers.re(r'a status code of 200 is returned for port "(?P<port>\d+)"'))
def port_online(port):
    """Then: a status code of 200 is returned"""
    assert isOpen(webserver_ip, port)

    r = requests.get(webserver_url[port])
    assert r.status_code == 200


@then(parsers.re(r'I do not get a response from port "(?P<port>\d+)"'))
def port_offline(port):
    """Then: I do not get a response."""
    assert not isOpen(webserver_ip, port)

