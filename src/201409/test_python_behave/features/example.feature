# -- FILE: features/example.feature
Feature: test text process using behave 

  Scenario: run from simple text
    Given we have some text "aaa bbb ccc         "
     When we implement prev word func with pointer at 12
     Then behave will return 'ccc'
     
  Scenario: run from file
    Given we have a file "text/test01.txt"
     When we implement prev word func with pointer at 12
     Then behave will return 'ccc'

  Scenario: run from long text
    Given we have some long text:
    """
    aaa bbb ccc         
    test second line
    """
    When we implement prev word func with pointer at 12
    Then behave will return 'ccc'