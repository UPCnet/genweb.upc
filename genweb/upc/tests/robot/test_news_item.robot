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
${PORTLET}  news-item
@{NEWS_DATA}  ${NEWS_ID}  Descripció de prova  Text de prova
...           /tmp/sample.jpg  Peu de prova

*** Test Cases ***

Create a news item
  Given we're logged in as admin
  When the test folder is activated
  And it has been created a simple portlet  ${URL_FOLDER}  ${PORTLET}  ${NEWS_ID}
  Then Page should contain  Element creat

Create a complete news item

  Given we're logged in as admin
  When the test folder is activated
  And it has been created a complete news item  ${URL_FOLDER}  @{NEWS_DATA}
  Then news item should contain  ${URL_NEWS}  @{NEWS_DATA}

Marking as important news item
  Given we're logged in as admin
  When the test folder is activated
  And it has been created a simple portlet  ${URL_FOLDER}  ${PORTLET}  ${NEWS_ID}
  And the news item has been marked as important  ${URL_FOLDER}/${NEWS_ID}
  Then Page should contain  Desmarca com a important

Unmarked as important news item
  Given we're logged in as admin
  When the test folder is activated
  And it has been created a simple portlet  ${URL_FOLDER}  ${PORTLET}  ${NEWS_ID}
  And the news item has been marked as important  ${URL_FOLDER}/${NEWS_ID}
  And the news item has been unmarked as important  ${URL_FOLDER}/${NEWS_ID}
  Then Page should contain  Marca com a important

Check that important news is highlighted
  Given we're logged in as admin
  When the test folder is activated
  And it has been created a simple portlet  ${URL_FOLDER}  ${PORTLET}  ${NEWS_ID}
  And the news item has been marked as important  ${URL_FOLDER}/${NEWS_ID}
  Then the news is highlighted  ${URL_FOLDER}/folder_contents

*** Keywords ***

it has been created a complete news item
  [Arguments]  ${URL}  ${TITLE}  ${DESCRIPTION}  ${TEXT}  ${IMAGE_PATH}
  ...          ${FOOT_IMAGE}
  Go to  ${URL}
  Click Element  id=plone-contentmenu-factories
  Click Element  id=news-item
  Input F_Text  title  ${TITLE}
  Input F_Text  description  ${DESCRIPTION}
  Input F_Rich  text  ${TEXT}
  ${STATUS} =  Run Keyword And Return Status  File Should Exist	 ${IMAGE_PATH}
  Run Keyword If  ${STATUS}
  ...  the image exists so we insert it  ${IMAGE_PATH}  ${FOOT_IMAGE}
  ...  ELSE
  ...  the image does not exist so we do not insert it  ${IMAGE_PATH}

news item should contain
  [Arguments]  ${URL}  ${TITLE}  ${DESCRIPTION}  ${TEXT}  ${IMAGE_PATH}
  ...          ${FOOT_IMAGE}
  Go to  ${URL}
  Page should contain  ${TITLE}
  Page should contain  ${DESCRIPTION}
  Page should contain  ${TEXT}
  ${STATUS} =  Run Keyword And Return Status  File Should Exist	 ${IMAGE_PATH}
  Run Keyword If  ${STATUS}
  ...  the image exists so we check that it is inserted  ${TITLE}  ${FOOT_IMAGE}

the news item has been marked as important
  [Arguments]  ${URL}
  Change the important status of the news  ${URL}

the news item has been unmarked as important
  [Arguments]  ${URL}
  Change the important status of the news  ${URL}

the news is highlighted
  [Arguments]  ${URL}
  ${CLASS_SEARCH} =  Set Variable  item-important
  Go to  ${URL}
  ${CLASS} =  Get Element Attribute  id=folder-contents-item-${NEWS_ID}@class
  Should Contain  ${CLASS}  ${CLASS_SEARCH}

Change the important status of the news
  [Arguments]  ${URL}
  When Go to  ${URL}
  Then Click Element  xpath=//*[@id="viewlet-above-content-title"]/div[1]/div/a
  And confirm action

the image exists so we insert it
  [Arguments]  ${IMAGE_PATH}  ${FOOT_IMAGE}
  Input F_Image  ${IMAGE_PATH}
  Input F_Text_Image  image_caption  ${FOOT_IMAGE}
  save form
  confirm action

the image does not exist so we do not insert it
  [Arguments]  ${IMAGE_PATH}
  save form
  Log  \nPodemos mejorar esta prueba insertando una imagen en ${IMAGE_PATH}  console=yes

the image exists so we check that it is inserted
  [Arguments]  ${TITLE}  ${FOOT_IMAGE}
  Page Should Contain Image  //*[@id="content-core"]/figure/a/img
  ${IMAGE_TITLE} =  Get Element Attribute  xpath=//*[@id="content-core"]/figure/a/img@title
  Should Contain  ${TITLE}  ${IMAGE_TITLE}
  Page should contain  ${FOOT_IMAGE}
