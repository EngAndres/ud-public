Feature: Calculator Operations
    As an engineer
    I want to perform basic arithmetic operations
    So that I can calculate mathematical expressions

    Background:
        Given I have a Calculator
    
    Scenario: Sum two positive numbers
        Given I have the first number 3 
        And I have the second number 2
        When I perform addition
        Then the result should be 5

    Scenario: Divide two positive numbers
        Given I have the first number 8 
        And I have the second number 4
        When I perform division
        Then the result should be 2.0
