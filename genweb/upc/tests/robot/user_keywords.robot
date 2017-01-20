*** Settings ***

Library  Selenium2Library

Resource  keywords.robot

*** Variables ***

@{CONTRIBUTOR}  Contributor  contributor  contributor
@{EDITOR}  Editor  editor  editor
@{MEMBER}  Member  member  member
@{READER}  Reader  reader  reader
@{REVIEWER}  Reviewer  reviewer  reviewer
@{SITE_ADMINISTRATOR}  Site Administrator  site_administrator  site_administrator
@{WEBMASTER}  WebMaster  webmaster  webmaster
@{MANAGER}  Manager  ${SITE_OWNER_NAME}  ${SITE_OWNER_PASSWORD}

@{ALL_USERS} =  ${CONTRIBUTOR}  ${EDITOR}  ${MEMBER}  ${READER}  ${REVIEWER}
...             ${SITE_ADMINISTRATOR}  ${WEBMASTER}  ${MANAGER}

*** Keywords ***

Login as
  [Arguments]  ${TYPE}
  ${NAME}  ${PASS} =  Get user data by type  ${TYPE}
  Login  ${NAME}  ${PASS}

we're created different user types
  # We do not create a Manager because it is already created by default
  [Arguments]  @{TYPE_USERS}
  we're logged in as admin
  Go to  ${PLONE_URL}/@@usergroup-userprefs
  Confirm action
  : FOR  ${TYPE}  IN  @{TYPE_USERS}
  \  ${NOT_MANAGER} =  Run Keyword And Return Status
  \  ...  Should Not Be Equal  Manager  ${TYPE}
  \  Run Keyword If  ${NOT_MANAGER}  Create user by type  ${TYPE}
  Logout

Create user by type
  [Arguments]  ${TYPE}
  Go to  ${PLONE_URL}/@@usergroup-userprefs
  Click Element  form.button.AddUser
  Wait Until Page Contains Element  form.email
  ${NAME}  ${PASS} =  Get user data by type  ${TYPE}
  Input Text  form.username  ${NAME}
  Input Text  form.email  ${NAME}@gmail.com
  Input Password  form.password  ${PASS}
  Input Password  form.password_ctl  ${PASS}
  Click Element  form.actions.register
  Wait Until Page Contains Element  xpath=//a[@title="${NAME}"]
  Unselect Checkbox  xpath=//a[@title="${NAME}"]/../../td/input[@value="Member"]
  Select Checkbox  xpath=//a[@title="${NAME}"]/../../td/input[@value="${TYPE}"]
  Click Element  form.button.Modify

Get type of user
  [Arguments]  @{USER}
  ${TYPE}  ${NAME}  ${PASS} =  Set Variable  @{USER}
  [Return]  ${TYPE}

Get user data by type
  [Arguments]  ${TYPE_USER}
  : FOR  ${USER}  IN  @{ALL_USERS}
  \  ${TYPE}  ${NAME}  ${PASS} =  Set Variable  @{USER}
  \  ${STATUS} =  Run Keyword And Return Status
  \  ...  Should Be Equal  ${TYPE}  ${TYPE_USER}
  \  Exit For Loop If  ${STATUS}
  [Return]  ${NAME}  ${PASS}

Get username by type
  [Arguments]  ${TYPE_USER}
  : FOR  ${USER}  IN  @{ALL_USERS}
  \  ${TYPE}  ${NAME}  ${PASS} =  Set Variable  @{USER}
  \  ${STATUS} =  Run Keyword And Return Status
  \  ...  Should Be Equal  ${TYPE}  ${TYPE_USER}
  \  Exit For Loop If  ${STATUS}
  [Return]  ${NAME}
