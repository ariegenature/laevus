*** Settings ***

Documentation    Browsing test suite against a Laevus instance

Library    OperatingSystem
Library    Process
Suite Setup    Start Application
Suite Teardown    Stop Application


*** Keywords ***

Start Application
    ${sitepackagesdir}=    Get Environment Variable    SITEPACKAGESDIR
    Run Process    npm    install    cwd=${sitepackagesdir}${/}laevus${/}contributejs
    Run Process    npm    run    build    cwd=${sitepackagesdir}${/}laevus${/}contributejs
    ${handle}=    Start Process    laevus
    Set Suite Variable    ${HANDLE}    ${handle}

Stop Application
    Terminate Process    ${HANDLE}
