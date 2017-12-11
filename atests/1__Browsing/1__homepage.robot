*** Settings ***

Documentation    Simple functional test for homepage

Library    Selenium2Library
Library    XvfbRobot

Resource    resources.robot


*** Test Cases ***

Homepage
    [Setup]    Start Virtual Display    1024    768
    Given user is anonymous
    When user browses to application homepage
    Then Page Should Contain    laevus homepage
    [Teardown]    Close All Browsers


*** Keywords ***

User Browses To Application Homepage
    Go To    ${SERVER_URL}
