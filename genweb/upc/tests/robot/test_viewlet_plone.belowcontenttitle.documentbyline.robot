*** Settings ***

Force Tags  wip-not_in_docs

Library  Selenium2Library

Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot
Resource  user_keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Variables ***

${URL_FOLDER}  ${PLONE_URL}/robot-test-folder
${SEARCH_VIEWLET}  darrera modificació

*** Test Cases ***

Check that the following users can not see the viewlet historial
  @{USERS} =  Set Variable  Member  Reader
  Given we're created different user types  @{USERS}
  When we have a modified directory to do the test
  Then check that the following users can not see the viewlet historial  @{USERS}

Check that the following users can see the viewlet historial
  @{USERS} =  Set Variable  Contributor  Editor  Reviewer  Site Administrator
  ...         WebMaster  Manager
  Given we're created different user types  @{USERS}
  When we have a modified directory to do the test
  Then check that the following users can see the viewlet historial  @{USERS}

*** Keywords ***

we have a modified directory to do the test
  Given we're logged in as admin
  When the test folder is activated
  And status has been passed to public  ${URL_FOLDER}
  Then Logout

check that the following users can not see the viewlet historial
  [Arguments]  @{USERS}
  : FOR  ${USER}  IN  @{USERS}
  \  Login as  ${USER}
  \  Page should contain  Us heu identificat correctament
  \  Go to  ${URL_FOLDER}
  \  Page Should Not Contain  ${SEARCH_VIEWLET}

check that the following users can see the viewlet historial
  [Arguments]  @{USERS}
  : FOR  ${USER}  IN  @{USERS}
  \  Login as  ${USER}
  \  Page should contain  Us heu identificat correctament
  \  Go to  ${URL_FOLDER}
  \  Page Should Contain  ${SEARCH_VIEWLET}
