*** Settings ***

Library  Selenium2Library
Library  Collections

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

we have created different types of users
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

we have created different types of users without role
  # Permitted types of users: Contributor, Editor, Reviewer and Reader
  [Arguments]  @{TYPE_USERS}
  @{NOT_VALID_USERS} =  Set Variable  Member  Site Administrator  WebMaster
  ...  Manager
  we're logged in as admin
  Go to  ${PLONE_URL}/@@usergroup-userprefs
  Confirm action
  : FOR  ${TYPE}  IN  @{TYPE_USERS}
  \  ${IS_NOT_VALID_USERS} =  Run Keyword And Return Status
  \  ...  List Should Not Contain Value  ${NOT_VALID_USERS}  ${TYPE}
  \  Run Keyword If  ${IS_NOT_VALID_USERS}
  \  ...  Create user by type  ${TYPE}  HAVE_ROL_TYPE=False
  \  ...  ELSE  Log  ${TYPE} no es un tipo de usuario valido.  console=true
  Logout

Create user by type
  [Arguments]  ${TYPE}  ${HAVE_ROL_TYPE}=True
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
  Run Keyword If  ${HAVE_ROL_TYPE}
  ...  Select Checkbox  xpath=//a[@title="${NAME}"]/../../td/input[@value="${TYPE}"]
  Click Element  form.button.Modify

Add shared permission
  [Arguments]  ${URL}  ${TYPE}
  Go To  ${URL}/@@sharing
  ${USER} =  Get username by type  ${TYPE}
  Input Text  sharing-user-group-search  ${USER}
  Click Element  sharing-search-button
  Wait Until Page Contains Element  xpath=//input[@name="entries.id:records" and @value="${USER}"]
  Select Checkbox  xpath=//input[@name="entries.id:records" and @value="${USER}"]/../../td/input[@name="entries.role_${TYPE}:records"]
  Click Element  sharing-save-button

Delete shared permission
  [Arguments]  ${URL}  ${TYPE}
  Go To  ${URL}/@@sharing
  ${USER} =  Get username by type  ${TYPE}
  Wait Until Page Contains Element  xpath=//input[@name="entries.id:records" and @value="${USER}"]
  Unselect Checkbox  xpath=//input[@name="entries.id:records" and @value="${USER}"]/../../td/input[@name="entries.role_${TYPE}:records"]
  Click Element  sharing-save-button

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
