Feature:
  As a system administrator,
  when the automation is run,
  I want to see port 443 on the webserver hosting the website
  and I do not want to see port 80 on the webserver hosting the website

  Scenario: Check if the webserver is hosting a website on port "443"
    Given: The webserver is Online
    When I go to port "443" on the webserver
    And I go to port "80" on the webserver
    Then a status code of 200 is returned for port "443"
    But I do not get a response from port "80"
