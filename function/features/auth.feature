Feature: Authentication checks

  Scenario Outline: An empty credential should always fail
    Given I input a blank <user_id> or a blank <password>
    Then check_auth should fail

    Examples:
    | user_id | password |
    |   a     |    a     |
    | my_user |    a     |
    |   a     | my_pass  |
