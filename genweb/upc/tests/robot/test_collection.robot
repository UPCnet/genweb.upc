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
${COLLECTION_ID}  titol_de_prova
${URL_COLLECTION}  ${URL_FOLDER}/${COLLECTION_ID}
@{COLLECTION_DATA}  ${COLLECTION_ID}  Descripció de prova  Text de prova

*** Test Cases ***

Create a collection for the title value
  ${SELECT_VALUE} =  Set Variable  Title
  ${SEARCH_TERM} =  Set Variable  Test Folder
  Given we're logged in as admin
  When it has been created a collection in test folder  ${SELECT_VALUE}
  ...  ${SEARCH_TERM}
  Then collection should contain the data  ${SEARCH_TERM}

Create a collection for the subject value
  ${SELECT_VALUE} =  Set Variable  Subject
  ${TAG_TERM} =  Set Variable  etiqueta
  ${SEARCH} =  Set Variable  Test Folder
  Given we're logged in as admin
  When it has been created a collection in test folder with tag  ${SELECT_VALUE}
  ...  ${TAG_TERM}
  Then collection should contain the data  ${SEARCH}

*** Keywords ***

it has been created a collection in test folder
  [Arguments]  ${SELECT_VALUE}  ${SEARCH_TERM}
  Given the test folder is activated
  Then it has been created a collection  ${SELECT_VALUE}  ${SEARCH_TERM}

it has been created a collection in test folder with tag
  [Arguments]  ${SELECT_VALUE}  ${TAG_TERM}
  Given the test folder is activated
  Then added a tag  ${URL_FOLDER}  ${TAG_TERM}
  And it has been created a collection  ${SELECT_VALUE}  ${TAG_TERM}

it has been created a collection
  [Arguments]  ${SELECT_VALUE}  ${TERM}
  Go to  ${URL_FOLDER}
  Click Element  id=plone-contentmenu-factories
  Click Element  id=collection
  ${TITLE}  ${DESCRIPTION}  ${TEXT} =  Set Variable  @{COLLECTION_DATA}
  Input F_Text  title  ${TITLE}
  Input F_Text  description  ${DESCRIPTION}
  Run Keyword If  '${SELECT_VALUE}' == 'Subject'
  ...  Input Search Term Subject  ${SELECT_VALUE}  ${TERM}
  ...  ELSE
  ...  Input Search Term  ${SELECT_VALUE}  ${TERM}
  Input F_Rich  text  ${TEXT}
  Save form

collection should contain the data
  [Arguments]  ${SEARCH}
  Go to  ${URL_COLLECTION}
  ${TITLE}  ${DESCRIPTION}  ${TEXT} =  Set Variable  @{COLLECTION_DATA}
  Page should contain  ${TITLE}
  Page should contain  ${DESCRIPTION}
  Page should contain  ${SEARCH}
  Page should contain  ${TEXT}

Input Search Term
  [Arguments]  ${SELECT_VALUE}  ${TERM}
  Select From List By Value  name=addindex  ${SELECT_VALUE}
  Input text  name=form.widgets.ICollection.query.v:records  ${TERM}

Input Search Term Subject
  [Arguments]  ${SELECT_VALUE}  ${TERM}
  Select From List By Value  name=addindex  ${SELECT_VALUE}
  Click Element  xpath=//*[@id="formfield-form-widgets-ICollection-query"]/div[2]/div/div[1]/div/dl[1]/dt/span[1]
  Select Checkbox  xpath=//*[@name="form.widgets.ICollection.query.v:records:list"][@value="${TERM}"]
