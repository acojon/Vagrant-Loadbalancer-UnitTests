# vagrant-LoadBalancer

Running vagrant up with the default condition will spin up:

* 2 Web servers running Nginx on port 80
* 1 Server runing HAProxy to load balance traffic between the two web servers on port 80
* One server running ansible
* One server to run pytest-bdd tests on the infrastructure.

Once the environment is running, you can log onto the ansible host.  If you run the site.yaml playbook, it will update the environment to run on HTTPS.  You can also build the https environment without first building the http environment, simply update the ansible.sh script to start in HTTPSPlaybooks.

## HAProxy

Stats page url: <http://>ipaddress:8404/stats

## pytest notes

```bash
# This will generate text showing the missing code for a given test
py.test --generate-missing --feature tests/features

#This will generate all of the code for a test from the user story
pytest-bdd generate tests/features/lb.feature

# Run all the tests
pytest tests/

# Run a specific test
pytest tests/step_defs/test_loadbalancer.py

# Run a test and save the output as json
pytest tests/step_defs/test_loadbalancer.py --cucumberjson-expanded --cucumberjson=.\test.json
```

## Gherkin

I found this page very helpful: <https://cucumber.io/docs/gherkin/reference/>

### Given

Given steps are used to describe the initial context of the system - the scene of the scenario. It is typically something that happened in the past.

When Cucumber executes a Given step, it will configure the system to be in a well-defined state, such as creating and configuring objects or adding data to a test database.

***The purpose of Given steps is to put the system in a known state*** before the user (or external system) starts interacting with the system (in the When steps). Avoid talking about user interaction in Given’s. If you were creating use cases, Given’s would be your preconditions.

It’s okay to have several Given steps (use And or But for number 2 and upwards to make it more readable).

Examples:

* Mickey and Minnie have started a game
* I am logged in
* Joe has a balance of £42

### When

When steps are used to describe an event, or an action. This can be a person interacting with the system, or it can be an event triggered by another system.

It’s strongly recommended you only have a single When step per Scenario. If you feel compelled to add more, it’s usually a sign that you should split the scenario up into multiple scenarios.

Examples:

* Guess a word
* Invite a friend
* Withdraw money

Most software does something people could do manually (just not as efficiently).

Try hard to come up with examples that don’t make any assumptions about technology or user interface. Imagine it’s 1922, when there were no computers.

Implementation details should be hidden in the step definitions.

### Then

Then steps are used to describe an expected outcome, or result.

The step definition of a Then step should use an assertion to compare the actual outcome (what the system actually does) to the expected outcome (what the step says the system is supposed to do).

An outcome should be on an observable output. That is, something that comes out of the system (report, user interface, message), and not a behavior deeply buried inside the system (like a record in a database).

Examples:

* See that the guessed word was wrong
* Receive an invitation
* Card should be swallowed

While it might be tempting to implement Then steps to look in the database - resist that temptation!

You should only verify an outcome that is observable for the user (or external system), and changes to a database are usually not.

### And, But

If you have successive Given’s, When’s, or Then’s, you could write:

```Gherkin
Example: Multiple Givens
  Given one thing
  Given another thing
  Given yet another thing
  When I open my eyes
  Then I should see something
  Then I shouldn't see something else
```

Or, you could make the example more fluidly structured by replacing the successive Given’s, When’s, or Then’s with And’s and But’s:

```Gherkin
Example: Multiple Givens
  Given one thing
  And another thing
  And yet another thing
  When I open my eyes
  Then I should see something
  But I shouldn't see something else
```

### *

Gherkin also supports using an asterisk (*) in place of any of the normal step keywords. This can be helpful when you have some steps that are effectively a list of things, so you can express it more like bullet points where otherwise the natural language of And etc might not read so elegantly.

For example:

```Gherkin
Scenario: All done
  Given I am out shopping
  And I have eggs
  And I have milk
  And I have butter
  When I check my list
  Then I don't need anything
```

Could be expressed as:

```Gherkin
Scenario: All done
  Given I am out shopping
  * I have eggs
  * I have milk
  * I have butter
  When I check my list
  Then I don't need anything
```
