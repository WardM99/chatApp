Feature: get current user information

  Scenario: get current user - correct status code
    Given user "test.user" is logged in
    When info about current user is asked
    Then the status code is 200

  Scenario: get current user - correct user
    Given user "test.user" is logged in
    When info about current user is asked
    Then the current user is "test.user"