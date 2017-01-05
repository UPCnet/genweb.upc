*** Settings ***

Force Tags  wip-not_in_docs

Library  Selenium2Library

Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
#Test Teardown  Close all browsers

*** Variables ***

${URL_FOLDER}  ${PLONE_URL}/robot-test-folder
${COLLECTION_ID}  titol_de_prova
${URL_COLLECTION}  ${URL_FOLDER}/${COLLECTION_ID}
@{COLLECTION_DATA}  ${COLLECTION_ID}  Descripció de prova  Text de prova

*** Test Cases ***

Create a collection for the title value
  ${SEARCH} =  Set Variable  Test Folder
  ${SELECT_VALUE} =  Set Variable  Title
  Given we're logged in as admin
  When the test folder is activated
  And it has been created a collection  ${URL_FOLDER}  @{COLLECTION_DATA}
  ...  ${SELECT_VALUE}  ${SEARCH}
  Then collection should contain  ${URL_COLLECTION}
  ...  @{COLLECTION_DATA}  ${SEARCH}

Create a collection for the subject value
  ${SEARCH} =  Set Variable  Test Folder
  ${TAG} =  Set Variable  etiqueta
  ${SELECT_VALUE} =  Set Variable  Subject
  Given we're logged in as admin
  When the test folder is activated
  And added a tag  ${URL_FOLDER}  ${TAG}
  And it has been created a collection  ${URL_FOLDER}  @{COLLECTION_DATA}
  ...  ${SELECT_VALUE}  ${TAG}
  Then collection should contain  ${URL_COLLECTION}
  ...  @{COLLECTION_DATA}  ${SEARCH}

*** Keywords ***

it has been created a collection
  [Arguments]  ${URL}  ${TITLE}  ${DESCRIPTION}  ${TEXT}  ${SELECT_VALUE}
  ...          ${SEARCH}
  Go to  ${URL}
  Click Element  id=plone-contentmenu-factories
  Click Element  id=collection
  Input F_Text  title  ${TITLE}
  Input F_Text  description  ${DESCRIPTION}
  Run Keyword If  '${SELECT_VALUE}' == 'Subject'
  ...  Input Search Term Subject  ${SELECT_VALUE}  ${SEARCH}
  ...  ELSE
  ...  Input Search Term  ${SELECT_VALUE}  ${SEARCH}
  Input F_Rich  text  ${TEXT}
  save form

collection should contain
  [Arguments]  ${URL}  ${TITLE}  ${DESCRIPTION}  ${TEXT}  ${SEARCH}
  Go to  ${URL}
  Page should contain  ${TITLE}
  Page should contain  ${DESCRIPTION}
  Page should contain  ${SEARCH}
  Page should contain  ${TEXT}

Input Search Term
  [Arguments]  ${SELECT_VALUE}  ${SEARCH}
  Select From List By Value  name=addindex  ${SELECT_VALUE}
  Input text  name=form.widgets.ICollection.query.v:records  ${SEARCH}

Input Search Term Subject
  [Arguments]  ${SELECT_VALUE}  ${TAG}
  Select From List By Value  name=addindex  ${SELECT_VALUE}
  Click Element  xpath=//*[@id="formfield-form-widgets-ICollection-query"]/div[2]/div/div[1]/div/dl[1]/dt/span[1]
  Select Checkbox  xpath=//*[@name="form.widgets.ICollection.query.v:records:list"][@value="${TAG}"]
