*** Settings ***

Force Tags  wip-not_in_docs

Library  Selenium2Library
Library  Collections

Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Variables ***

${URL_FOLDER}  ${PLONE_URL}/robot-test-folder
${URL_NEWS_ITEM}  ${PLONE_URL}/ca/noticies
${URL_EVENT}  ${PLONE_URL}/ca/esdeveniments

@{LIST_TAGS}  noticia  evento  lorem
@{NEWS_ITEM_0}  ${URL_NEWS_ITEM}  news-item  xnews_item_without_tagx
@{NEWS_ITEM_1}  ${URL_NEWS_ITEM}  news-item  xnews_item_noticiax  @{LIST_TAGS}[0]
@{NEWS_ITEM_2}  ${URL_NEWS_ITEM}  news-item  xnews_item_noticia_loremx  @{LIST_TAGS}[0]  @{LIST_TAGS}[2]
@{EVENT_0}  ${URL_EVENT}  event  xevent_without_tagx
@{EVENT_1}  ${URL_EVENT}  event  xevent_eventox  @{LIST_TAGS}[1]
@{EVENT_2}  ${URL_EVENT}  event  xevent_evento_loremx  @{LIST_TAGS}[1]  @{LIST_TAGS}[2]

@{DATA}  ${NEWS_ITEM_0}  ${NEWS_ITEM_1}  ${NEWS_ITEM_2}
...      ${EVENT_0}  ${EVENT_1}  ${EVENT_2}

*** Test Cases ***

View a list of news events with tags created
  Given we're logged in as admin
  When the default directories have been created
  And different items have been created with tags  @{DATA}
  And open new list of news events  ${PLONE_URL}
  Then page should contain the list of tags  @{LIST_TAGS}

View a list of news events without tags created
  Given we're logged in as admin
  When open new list of news events  ${PLONE_URL}
  Then page should not contain the list of tags  @{LIST_TAGS}

Create a news event listing of news type without selected tags
  Given we're logged in as admin
  When the default directories have been created
  And it has been created a news event listing without selected tags in homepage  News
  Then homepage should contain a news event listing of news type without selected tags

Create a news event listing of events type without selected tags
  Given we're logged in as admin
  When the default directories have been created
  And it has been created a news event listing without selected tags in homepage  Events
  Then homepage should contain a news event listing of events type

Create a news event listing of news type with tags
  @{LIST_TAGS_AND_DATA} =  Set Variable  ${LIST_TAGS}  ${DATA}
  Given we're logged in as admin
  When the default directories have been created
  And different items have been created with tags  @{DATA}
  And it has been created a news event listing with selected tags in homepage  News  @{LIST_TAGS}
  Then homepage should contain a news event listing of news type with selected tags  @{LIST_TAGS}
  And each news link must contain the corresponding elements  @{LIST_TAGS_AND_DATA}

Create a news event listing of events type with tags
  @{LIST_TAGS_AND_DATA} =  Set Variable  ${LIST_TAGS}  ${DATA}
  Given we're logged in as admin
  When the default directories have been created
  And different items have been created with tags  @{DATA}
  And it has been created a news event listing with selected tags in homepage  Events  @{LIST_TAGS}
  Then homepage should contain a news event listing of events type
  And today events link must contain the corresponding elements  @{DATA}

*** Keywords ***

it has been created a news event listing without selected tags in homepage
  [Arguments]  ${TYPE_TAG}
  open new list of news events in homepage
  Wait Until Page Contains Element  id=form.typetag  timeout=1
  Select From List  id=form.typetag  ${TYPE_TAG}
  save form

it has been created a news event listing with selected tags in homepage
  [Arguments]  ${TYPE_TAG}  @{LIST_TAGS}
  open new list of news events in homepage
  Wait Until Page Contains Element  id=form.typetag  timeout=1
  Select From List  id=form.typetag  ${TYPE_TAG}
  Select All From List  id=form.tags.from
  Click Button  name=from2toButton
  save form

open new list of news events
  [Arguments]  ${URL}
  Go to  ${URL}/@@manage-portlets
  Continue open new list of news events

open new list of news events in homepage
  Go to  ${PLONE_URL}/@@manage-homeportlets
  confirm action
  Continue open new list of news events

Continue open new list of news events
  Click Element  xpath=//*[@id="portletselectorform"]/div/button
  Click Element  xpath=//*[@id="gwportletselector"]/li/a[text()="Categories"]

page should contain the list of tags
  [Arguments]  @{LIST_TAGS}
  : FOR  ${TAG}  IN  @{LIST_TAGS}
  \  Page should contain list  id=form.tags.from  ${TAG}

page should not contain the list of tags
  [Arguments]  @{LIST_TAGS}
  : FOR  ${TAG}  IN  @{LIST_TAGS}
  \  Page should not contain  ${TAG}

homepage should contain a news event listing of news type without selected tags
  Go to  ${PLONE_URL}
  Page should contain element  xpath=//a[contains(text(), "Totes les notícies")]

homepage should contain a news event listing of events type
  Go to  ${PLONE_URL}
  Page should contain element  xpath=//a[contains(text(), "Propers")]
  Page should contain element  xpath=//a[contains(text(), "Avui")]
  Page should contain element  xpath=//a[contains(text(), "Passat")]
  Page should contain element  xpath=//a[contains(text(), "Dia")]
  Page should contain element  xpath=//a[contains(text(), "Mes")]
  Page should contain element  xpath=//a[contains(text(), "Setmana")]
  Page should contain element  xpath=//a/span[contains(text(),"iCal")]

homepage should contain a news event listing of news type with selected tags
  [Arguments]  @{TAGS}
  Go to  ${PLONE_URL}
  Page should contain element  xpath=//a[contains(text(), "Totes les notícies")]
  :FOR  ${TAG}  IN  @{TAGS}
  \  Page should contain  ${TAG}

each news link must contain the corresponding elements
  [Arguments]  @{LIST_TAGS_AND_DATA}
  @{TAGS} =  Set Variable  @{LIST_TAGS_AND_DATA}[0]
  @{DATA} =  Set Variable  @{LIST_TAGS_AND_DATA}[1]
  :FOR  ${TAG}  IN  @{TAGS}
  \  Go to  ${PLONE_URL}
  \  Click Element  //a[contains(text(), '${TAG}')]
  \  Page should contain titles of news elements  ${TAG}  @{DATA}

Page should contain titles of news elements
  [Arguments]  ${TAG}  @{DATA}
  : FOR  ${ELEMENT}  IN  @{DATA}
  \  ${STATUS_TYPE} =  Run Keyword And Return Status
  \  ...  List Should Contain Value  ${ELEMENT}  news-item
  \  ${STATUS_TAG} =  Run Keyword And Return Status
  \  ...  List Should Contain Value  ${ELEMENT}  ${TAG}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  Run Keyword If  ${STATUS_TYPE} and ${STATUS_TAG}
  \  ...  Page Should Contain  ${TITLE}
  \  ...  ELSE
  \  ...  Page Should Not Contain  ${TITLE}

today events link must contain the corresponding elements
  [Arguments]  @{DATA}
  Go to  ${PLONE_URL}
  Click Element  xpath=//a[contains(text(), "Avui")]
  : FOR  ${ELEMENT}  IN  @{DATA}
  \  ${STATUS_TYPE} =  Run Keyword And Return Status
  \  ...  List Should Contain Value  ${ELEMENT}  event
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  Run Keyword If  ${STATUS_TYPE}
  \  ...  Page Should Contain  ${TITLE}
  \  ...  ELSE
  \  ...  Page Should Not Contain  ${TITLE}
