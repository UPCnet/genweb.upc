*** Settings ***

Force Tags  wip-not_in_docs

Library  Selenium2Library

Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
# Test Teardown  Close all browsers

*** Variables ***

${URL_FOLDER}  ${PLONE_URL}/robot-test-folder
@{NEWS_ITEM_0}  news_item  news_item_without_tag
@{NEWS_ITEM_1}  news_item  news_item_noticia  noticia
@{NEWS_ITEM_2}  news_item  news_item_noticia_lorem  noticia  lorem
@{EVENT_0}  event  event_without_tag
@{EVENT_1}  event  event_evento  evento
@{EVENT_2}  event  event_evento_lorem  evento  lorem
@{DOCUMENT_1}  document  document_lorem  lorem
@{DATA}  ${NEWS_ITEM_0}  ${NEWS_ITEM_1}  ${NEWS_ITEM_2}
...      ${EVENT_0}      ${EVENT_1}      ${EVENT_2}
...      ${DOCUMENT_1}

*** Test Cases ***

Create a news event listing of news type without selected tags
  Given we're logged in as admin
  When the test folder is activated
  And different items have been created with tags  ${URL_FOLDER}  @{DATA}
  # And it has been created a news event listing of news type without selected tags
  # Then Page should contain  ...

# Create a news event listing of event type without tags
#   Given we're logged in as admin
#   When the test folder is activated
#   And different items have been created with tags  ${URL_FOLDER}  @{DATA}
#   And it has been created a news event listing of event type without selected tags
#   Then Page should contain  ...
#
# Create a news event listing of news type with tags
#   Given we're logged in as admin
#   When the test folder is activated
#   And different items have been created with tags  ${URL_FOLDER}  @{DATA}
#   And it has been created a news event listing of news type with selected tags
#   Then Page should contain  ...
#
# Create a news event listing of event type with tags
#   Given we're logged in as admin
#   When the test folder is activated
#   And different items have been created with tags  ${URL_FOLDER}  @{DATA}
#   And it has been created a news event listing of event type with selected tags
#   Then Page should contain  ...

*** Keywords ***

it has been created a news event listing of news type without selected tags

it has been created a news event listing of event type without selected tags

it has been created a news event listing of news type with selected tags

it has been created a news event listing of event type with selected tags

Create a news event listing without saving
