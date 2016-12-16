*** Settings ***

Force Tags  wip-not_in_docs

Library   Selenium2Library
Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Test Cases ***

Create a news item Prueba
  Given we're logged in as admin
  When the test folder is activated
  Then it has been created a news item  ${PLONE_URL}/robot-test-folder  Prueba
  And Page should contain  Element creat

Marking as important news item
  Given we're logged in as admin
  When the test folder is activated
  And it has been created a news item  ${PLONE_URL}/robot-test-folder  Prueba
  And the news item has been marked as important  ${PLONE_URL}/robot-test-folder/prueba
  Then Page should contain  Desmarca com a important

Unmarked as important news item
  Given we're logged in as admin
  When the test folder is activated
  And it has been created a news item  ${PLONE_URL}/robot-test-folder  Prueba
  And the news item has been marked as important  ${PLONE_URL}/robot-test-folder/prueba
  And the news item has been unmarked as important  ${PLONE_URL}/robot-test-folder/prueba
  Then Page should contain  Marca com a important

*** Keywords ***

it has been created a news item
  [Arguments]  ${URL}  ${TITLE}
  Go to  ${URL}
  Click Element  id=plone-contentmenu-factories
  Click Element  id=news-item
  Input Text  name=form.widgets.IDublinCore.title  ${TITLE}
  Click Button  name=form.buttons.save

the news item has been marked as important
  [Arguments]  ${URL}
  Change the important status of the news  ${URL}

the news item has been unmarked as important
  [Arguments]  ${URL}
  Change the important status of the news  ${URL}

Change the important status of the news
  [Arguments]  ${URL}
  When Go to  ${URL}
  Then Click Element  xpath=//*[@id="viewlet-above-content-title"]/div[1]/div/a
  And confirm action
