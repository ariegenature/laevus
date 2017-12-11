*** Settings ***

Documentation    Acceptance tests related to contributing wild life collision observations

Library    Selenium2Library
Library    XvfbRobot

Resource    resources.robot


*** Test Cases ***

Contribution page
    [Setup]    Start Virtual Display    1024    768
    Given user is anonymous
    When user browses to contribution page
    Then Page Should Contain    Welcome to Your Vue.js App
    [Teardown]    Close All Browsers


*** Keywords ***

User Browses To contribution page
    Go To    ${SERVER_URL}/contribute
