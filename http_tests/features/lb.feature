Feature:
  As a system administrator,
  when the automation is run,
  I want to see port 80 on the load balancer

  Scenario: Check if load balancer is hosting a website on port 80
    Given: The Load Balancer is Online
    When I go to port "80" on the Load Balancer
    Then a status code of 200 is returned for port "80"
