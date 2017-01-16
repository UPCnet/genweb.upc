*** Settings ***

Force Tags  wip-not_in_docs

Library  Selenium2Library

Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot
Resource  date_keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Variables ***

${URL_NEWS_ITEM}  ${PLONE_URL}/ca/noticies
${IMAGE_PATH}  ${CURDIR}/img/sample.png
@{DATA}  ${URL_NEWS_ITEM}  titol-de-prova  ${IMAGE_PATH}
${MAX_NOTICE}  14

*** Test Cases ***

Create a fullnews portlet with normal render
  Given we're logged in as admin
  When the default directories have been created
  And it has been created a public news item with image  @{DATA}
  And it has been created a fullnews with normal render in homepage
  Then homepage should contain the news item with image left and text right

Create a fullnews portlet with total width
  Given we're logged in as admin
  When the default directories have been created
  And it has been created a public news item with image  @{DATA}
  And it has been created a fullnews with total width in homepage
  Then homepage should contain the news item with image above text and below

Create a fullnews portlet with total width of two columns
  Given we're logged in as admin
  When the default directories have been created
  And it has been created a x public news items with image  2  @{DATA}
  And it has been created a fullnews with total width of two columns in homepage
  Then homepage should contain the news items in two columns with image above and text below

Create a fullnews portlet with the minimum of news item
  Given we're logged in as admin
  When the default directories have been created
  And it has been created a public news item with image  @{DATA}
  And it has been created a fullnews with the minimum of news item
  Then homepage should contain x news items  1

Create a fullnews portlet with the maximum of news item
  Given we're logged in as admin
  When the default directories have been created
  And it has been created a x public news items with image  ${MAX_NOTICE}  @{DATA}
  And it has been created a fullnews with the maximum of news item
  Then homepage should contain x news items  ${MAX_NOTICE}

Create a fullnews portlet with marked date show
  Given we're logged in as admin
  When the default directories have been created
  And it has been created a public news item with image  @{DATA}
  And it has been created a fullnews with marked date show in homepage
  Then homepage should contain date of news item

Create a fullnews portlet without marked date show
  Given we're logged in as admin
  When the default directories have been created
  And it has been created a public news item with image  @{DATA}
  And it has been created a fullnews without marked date show in homepage
  Then homepage should not contain date of news item

*** Keywords ***

it has been created a public news item with image
  [Arguments]  ${URL}  ${TITLE}  ${IMAGE_PATH}
  it has been created a simple item  ${URL}  news-item  ${TITLE}
  ${EDIT_URL} =  Set Variable  ${URL}/${TITLE}
  Add image a news item  ${EDIT_URL}  ${IMAGE_PATH}
  status has been passed to public  ${EDIT_URL}

it has been created a x public news items with image
  [Arguments]  ${TOTAL}  ${URL}  ${TITLE}  ${IMAGE_PATH}
  : FOR  ${INDEX}  IN RANGE  0  ${TOTAL}
  \  it has been created a public news item with image  ${URL}  ${TITLE}-${INDEX}
  \  ...  ${IMAGE_PATH}

Add image a news item
  [Arguments]  ${URL}  ${IMAGE_PATH}
  Go to  ${URL}/edit
  Input F_Image  ${IMAGE_PATH}
  save form
  confirm action

it has been created a fullnews in homepage
  # ${VIEW_TYPE}  id_normal | id_full | id_full_2cols | default (Does not change)
  # ${COUNT}      Number from 1 to ${MAX_NOTICE} | default (Does not change)
  # ${SHOW_DATA}  boolean
  [Arguments]  ${VIEW_TYPE}  ${COUNT}  ${SHOW_DATA}
  Go to  ${PLONE_URL}/@@manage-homeportlets
  confirm action
  Click Element  xpath=//*[@id="portletselectorform"]/div/button
  Click Element  xpath=//*[@id="gwportletselector"]/li/a[text()="Notícies amb foto"]
  ${STATUS} =  Run Keyword And Return Status  Should Be Equal  ${VIEW_TYPE}  default
  Run Keyword Unless  ${STATUS}  Select From List  id=form.view_type  ${VIEW_TYPE}
  ${STATUS} =  Run Keyword And Return Status  Should Be Equal  ${COUNT}  default
  Run Keyword Unless  ${STATUS}  Select From List  id=form.count  ${COUNT}
  Run Keyword Unless  ${SHOW_DATA}  Unselect Checkbox  id=form.showdata
  save form

it has been created a fullnews with normal render in homepage
  it has been created a fullnews in homepage  id_normal  default  True

it has been created a fullnews with total width in homepage
  it has been created a fullnews in homepage  id_full  default  True

it has been created a fullnews with total width of two columns in homepage
  it has been created a fullnews in homepage  id_full_2cols  default  True

it has been created a fullnews with the minimum of news item
  it has been created a fullnews in homepage  default  1  True

it has been created a fullnews with the maximum of news item
  it has been created a fullnews in homepage  default  ${MAX_NOTICE}  True

it has been created a fullnews with marked date show in homepage
  it has been created a fullnews in homepage  default  default  True

it has been created a fullnews without marked date show in homepage
  it has been created a fullnews in homepage  default  default  False

Page Should Contain a news item portlet
  Page Should Contain  Notícies

homepage should contain the news item with image left and text right
  main page is open
  Page Should Contain Element  xpath=//ul[@class="list-portlet"]/li/h3/../img[@class="span6"]/../div[@class="content-noticies"]/p/../time

homepage should contain the news item with image above text and below
  main page is open
  Page Should Contain Element  xpath=//ul[@class="list-portlet"]/li/a/div[@class="noticies-full"]/img/../../h3/../../div[@class="content-noticies"]/p/../time

homepage should contain the news items in two columns with image above and text below
  main page is open
  Page Should Contain Element  xpath=//div[@id="pair-news"]/../div[@id="odd-news"]
  Page Should Contain Element  xpath=//div[@id="pair-news"]/div[@class="noticia-full-2cols"]/a/div[@class="noticies-full"]/img/../../h3/../../div[@class="content-noticies"]/p/../time
  Page Should Contain Element  xpath=//div[@id="odd-news"]/div[@class="noticia-full-2cols"]/a/div[@class="noticies-full"]/img/../../h3/../../div[@class="content-noticies"]/p/../time

homepage should contain x news items
  [Arguments]  ${TOTAL}
  main page is open
  ${COUNT} =  Get Matching Xpath Count  xpath=//ul[@class="list-portlet"]/li
  Should Be Equal  ${TOTAL}  ${COUNT}

homepage should contain date of news item
  main page is open
  ${DATE} =  Get Current Date in European format
  Page Should Contain Element  xpath=//time[text()="${DATE}"]

homepage should not contain date of news item
  main page is open
  ${DATE} =  Get Current Date in European format
  Page Should Not Contain Element  xpath=//time[text()="${DATE}"]
