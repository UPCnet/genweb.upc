*** Settings ***

Force Tags  wip-not_in_docs

Library  Selenium2Library

Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Variables ***

${URL_FOLDER}  ${PLONE_URL}/robot-test-folder
${NEWS_ID}  prueba
@{COLLECTION_DATA}  titol-de-prova  Descripció de prova  Text de prova

*** Test Cases ***

Create a collection amb terme títol
  ${CONTENT} =  Set Variable    Test Folder
  Given we're logged in as admin
  When the test folder is activated
  And it has been created a collection  ${URL_FOLDER}  @{COLLECTION_DATA}  Title
  ...  ${CONTENT}
  Then collection should contain  ${URL_FOLDER}/@{COLLECTION_DATA}[0]
  ...  @{COLLECTION_DATA}  ${CONTENT}

*** Keywords ***

it has been created a collection
  [Arguments]  ${URL}  ${TITLE}  ${DESCRIPTION}  ${TEXT}  ${SELECT_VALUE}
  ...          ${CONTENT}
  Go to  ${URL}
  Click Element  id=plone-contentmenu-factories
  Click Element  id=collection
  Input F_Text  title  ${TITLE}
  Input F_Text  description  ${DESCRIPTION}
  Input Search Term  ${SELECT_VALUE}  ${CONTENT}
  Input F_Rich  text  ${TEXT}
  save form

collection should contain
  [Arguments]  ${URL}  ${TITLE}  ${DESCRIPTION}  ${TEXT}  ${CONTENT}
  Go to  ${URL}
  Page should contain  ${TITLE}
  Page should contain  ${DESCRIPTION}
  Page should contain  ${CONTENT}
  Page should contain  ${TEXT}

Input Search Term
  [Arguments]  ${SELECT_VALUE}  ${CONTENT}
  Select From List By Value  name=addindex  ${SELECT_VALUE}
  Input text  name=form.widgets.ICollection.query.v:records  ${CONTENT}
