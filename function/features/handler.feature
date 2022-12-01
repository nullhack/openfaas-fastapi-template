Feature: Handler basic checks.

As a simple rule, for any input, the handler must return a dict.
So we can intergrate with other tools.

  Scenario: Basic output
    Given an input to the handler
    Then the output of the handler must be of type dict
