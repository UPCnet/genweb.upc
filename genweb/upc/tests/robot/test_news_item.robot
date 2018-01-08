*** Settings ***

Force Tags  wip-not_in_docs

Library  Selenium2Library
Library	 OperatingSystem

Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Variables ***

${URL_FOLDER}  ${PLONE_URL}/robot-test-folder
${NEWS_ID}  titol-de-prova
${URL_NEWS}  ${URL_FOLDER}/${NEWS_ID}
${ITEM}  news-item
${IMAGE_PATH}  ${CURDIR}/img/sample.png
@{NEWS_DATA}  ${NEWS_ID}  Descripció de prova  Text de prova  ${IMAGE_PATH}
...           Peu de prova

*** Test Cases ***

Create a news item
  Given we're logged in as admin
  When it has been created a simple news item in test folder
  Then Page should contain  Element creat

Create a complete news item
  Given we're logged in as admin
  When it has been created a complete news item in test folder
  Then news item should contain the data

Marking as important news item
  Given we're logged in as admin
  When it has been created a simple news item in test folder
  And the news item has been marked as important
  Then Page should contain  Desmarca com a important

Unmarked as important news item
  Given we're logged in as admin
  When it has been created a complete news item in test folder
  And the news item has been marked as important
  And the news item has been unmarked as important
  Then Page should contain  Marca com a important

Check that important news is highlighted
  Given we're logged in as admin
  When it has been created a complete news item in test folder
  And the news item has been marked as important
  Then the news is highlighted

*** Keywords ***

it has been created a simple news item in test folder
  Given the test folder is activated
  Then it has been created a simple item  ${URL_FOLDER}  ${ITEM}  ${NEWS_ID}

it has been created a complete news item in test folder
  Given the test folder is activated
  Then it has been created a complete news item

it has been created a complete news item
  Go to  ${URL_FOLDER}
  Click Element  id=plone-contentmenu-factories
  Click Element  id=news-item
  ${TITLE}  ${DESCRIPTION}  ${TEXT}  ${IMAGE_PATH}  ${FOOT_IMAGE} =
  ...  Set Variable  @{NEWS_DATA}
  Input F_Text  title  ${TITLE}
  Input F_Text  description  ${DESCRIPTION}
  Input F_Rich  text  ${TEXT}
  ${STATUS} =  Run Keyword And Return Status  File Should Exist	 ${IMAGE_PATH}
  Run Keyword If  ${STATUS}
  ...  the image exists so we insert it  ${IMAGE_PATH}  ${FOOT_IMAGE}
  ...  ELSE
  ...  the image does not exist so we do not insert it  ${IMAGE_PATH}

news item should contain the data
  Go to  ${URL_NEWS}
  ${TITLE}  ${DESCRIPTION}  ${TEXT}  ${IMAGE_PATH}  ${FOOT_IMAGE} =
  ...  Set Variable  @{NEWS_DATA}
  Page should contain  ${TITLE}
  Page should contain  ${DESCRIPTION}
  Page should contain  ${TEXT}
  ${STATUS} =  Run Keyword And Return Status  File Should Exist	 ${IMAGE_PATH}
  Run Keyword If  ${STATUS}
  ...  the image exists so we check that it is inserted  ${TITLE}  ${FOOT_IMAGE}

the news item has been marked as important
  Change the important status of the news

the news item has been unmarked as important
  Change the important status of the news

the news is highlighted
  ${CLASS_SEARCH} =  Set Variable  item-important
  Go to  ${URL_FOLDER}/folder_contents
  ${CLASS} =  Get Element Attribute  id=folder-contents-item-${NEWS_ID}@class
  Should Contain  ${CLASS}  ${CLASS_SEARCH}

Change the important status of the news
  When Go to  ${URL_NEWS}/folder_contents
  Then Click Element  xpath=//*[@id="viewlet-above-content-title"]/div[1]/div/a
  And Confirm action

the image exists so we insert it
  [Arguments]  ${IMAGE_PATH}  ${FOOT_IMAGE}
  Input F_Image  ${IMAGE_PATH}
  Input F_Text_Image  image_caption  ${FOOT_IMAGE}
  Save form
  Confirm action

the image does not exist so we do not insert it
  [Arguments]  ${IMAGE_PATH}
  Save form
  Log  \nPodemos mejorar esta prueba insertando una imagen en ${IMAGE_PATH}  console=yes

the image exists so we check that it is inserted
  [Arguments]  ${TITLE}  ${FOOT_IMAGE}
  Page Should Contain Image  //*[@id="content-core"]/figure/a/img
  ${IMAGE_TITLE} =  Get Element Attribute  xpath=//*[@id="content-core"]/figure/a/img@title
  Should Contain  ${TITLE}  ${IMAGE_TITLE}
  Page should contain  ${FOOT_IMAGE}
