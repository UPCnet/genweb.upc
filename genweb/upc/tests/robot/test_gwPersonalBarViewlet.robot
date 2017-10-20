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

*** Test Cases ***

Editor, Manager, Site Administrator and WebMaster do have the tools section in the top menu
  @{USERS} =  Set Variable  Editor  Manager  Site Administrator  WebMaster
  Given we have created different types of users  @{USERS}
  Then the homepage should contain the tools section in the top menu  @{USERS}

Editor do have the tools section in the top menu the over root of each language
  ${USERS} =  Set Variable  Editor
  Given we have created different types of users without role  ${USERS}
  Then the over root of each language should contain the tools section in the top menu
  ...  ${USERS}

Editor and Contributor do have the tools section in the top menu the over root of each language
  @{USERS} =  Set Variable  Editor  Contributor
  Given we have created different types of users without role  @{USERS}
  Then the root of each language should contain the tools section in the top menu
  ...  @{USERS}

Reader and Reviewer do not have the tools section in the top menu at the root of each language
  @{USERS} =  Set Variable  Reader  Reviewer
  Given we have created different types of users without role  @{USERS}
  Then the root of each language should not contain the tools section in the top menu
  ...  @{USERS}

*** Keywords ***

the homepage should contain the tools section in the top menu
  [Arguments]  @{USERS}
  : FOR  ${USER}  IN  @{USERS}
  \  Login as  ${USER}
  \  Wait Until Page Contains Element  portal-personaltools-wrapper
  \  Page should contain menu items  Català  Español  English
  \  ...  Concedir permisos  Fitxers compartits  Personalitza plantilles  Desfés

the over root of each language should contain the tools section in the top menu
  [Arguments]  @{USERS}
  Create the default directories have been created
  : FOR  ${USER}  IN  @{USERS}
  \  Add sharing permission to user  ${PLONE_URL}  ${USER}
  \  Login as  ${USER}
  \  Go to  ${PLONE_URL}
  \  Page should contain menu items  Català  Español  English  Concedir permisos
  \  ...  Fitxers compartits  Personalitza plantilles  Desfés
  \  Logout

the root of each language should contain the tools section in the top menu
  [Arguments]  @{USERS}
  Create the default directories have been created
  : FOR  ${USER}  IN  @{USERS}
  \  Add sharing permission to user  ${PLONE_URL}/ca  ${USER}
  \  Login as  ${USER}
  \  Go to  ${PLONE_URL}/ca
  \  Page should contain menu items  Català  Fitxers compartits  Desfés
  \  Page should not contain menu items  Español  English  Concedir permisos
  \  ...  Personalitza plantilles
  \  Logout
  \  Delete sharing permission to user  ${PLONE_URL}/ca  ${USER}
  \  Add sharing permission to user  ${PLONE_URL}/es  ${USER}
  \  Login as  ${USER}
  \  Go to  ${PLONE_URL}/es
  \  Page should contain menu items  Español  Ficheros compartidos  Deshacer
  \  Page should not contain menu items  Català  English  Conceder permisos
  \  ...  Personaliza pantillas
  \  Logout
  \  Delete sharing permission to user  ${PLONE_URL}/es  ${USER}
  \  Add sharing permission to user  ${PLONE_URL}/en  ${USER}
  \  Login as  ${USER}
  \  Go to  ${PLONE_URL}/en
  \  Page should contain menu items  English  Shared files  Undo
  \  Page should not contain menu items  Català  Español  Grant access
  \  ...  Costumize templates

the root of each language should not contain the tools section in the top menu
  [Arguments]  @{USERS}
  Create the default directories have been created
  : FOR  ${USER}  IN  @{USERS}
  \  Add sharing permission to user  ${PLONE_URL}  ${USER}
  \  Login as  ${USER}
  \  Go to  ${PLONE_URL}/ca
  \  Page Should Not Contain Element  xpath=//a[@data-toggle="dropdown"][contains(text(),"Eines")]
  \  Go to  ${PLONE_URL}/es
  \  Page Should Not Contain Element  xpath=//a[@data-toggle="dropdown"][contains(text(),"Herramientas")]
  \  Go to  ${PLONE_URL}/en
  \  Page Should Not Contain Element  xpath=//a[@data-toggle="dropdown"][contains(text(),"Tools")]
  \  Logout

Page should contain menu items
  [Arguments]  @{LINKS}
  : FOR  ${LINK}  IN  @{LINKS}
  \  Page Should Contain Element  xpath=//li[@role="menuitem"]/a[contains(text(),"${LINK}")]

Page should not contain menu items
  [Arguments]  @{LINKS}
  : FOR  ${LINK}  IN  @{LINKS}
  \  Page Should Not Contain Element  xpath=//li[@role="menuitem"]/a[contains(text(),"${LINK}")]

Create the default directories have been created
  we're logged in as admin
  the default directories have been created
  Logout

Add sharing permission to user
  [Arguments]  ${URL}  ${PERMISSION}
  we're logged in as admin
  Add shared permission  ${URL}  ${PERMISSION}
  Logout

Delete sharing permission to user
  [Arguments]  ${URL}  ${PERMISSION}
  we're logged in as admin
  Delete shared permission  ${URL}  ${PERMISSION}
  Logout
