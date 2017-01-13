*** Settings ***

Force Tags  wip-not_in_docs

Library  Selenium2Library

Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot
Resource  event_keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Variables ***

# You can change the values for @{START_DATE} and @{RECURRENCE_DATA}
${URL_FOLDER}  ${PLONE_URL}/robot-test-folder
${EVENT_ID}  titol-de-prova
${URL_EVENT}  ${URL_FOLDER}/${EVENT_ID}
@{START_DATE}  29  12  2016
@{EVENT_DATA}  ${EVENT_ID}  Descripció de prova  @{START_DATE}
...            Ubicació de prova  Assistent de prova  Contacte de prova
...            correu@de.prova  933030303  http://www.google.com  Text de prova
# To avoid problems, avoid placing values greater than 999
@{RECURRENCE_DATA}  2  5

*** Test Cases ***

Create a recurring event
  Given we're logged in as admin
  When the test folder is activated
  And it has been created a event  ${URL_FOLDER}  @{EVENT_DATA}
  And recurrence has been added  ${URL_EVENT}  @{RECURRENCE_DATA}
  Then event should contain  ${URL_EVENT}  @{EVENT_DATA}
  And event should contain recurrence  ${URL_EVENT}  @{START_DATE}
  ...  @{RECURRENCE_DATA}

*** Keywords ***

event should contain
  [Arguments]  ${URL}  ${TITLE}  ${DESCRIPTION}  ${DAY}  ${MONTH}  ${YEAR}
  ...          ${LOCATION}  ${ATTENDEES}  ${CONTACT_NAME}  ${CONTACT_EMAIL}
  ...          ${CONTACT_PHONE}  ${EVENT_URL}  ${TEXT}
  Go to  ${URL}
  Page should contain  ${TITLE}
  Page should contain  ${DESCRIPTION}
  Page should contain a correct date  ${DAY}  ${MONTH}  ${YEAR}
  Page should contain  ${LOCATION}
  Page should contain  ${ATTENDEES}
  Page should contain  ${CONTACT_NAME}
  Page should contain Element  xpath=//*[@href="mailto:${CONTACT_EMAIL}"]
  Page should contain  ${CONTACT_PHONE}
  Page should contain  ${EVENT_URL}
  Page should contain  ${TEXT}

event should contain recurrence
  [Arguments]  ${URL}  ${DAY}  ${MONTH}  ${YEAR}  ${REPEAT_EACH}  ${ENDED_AFTER}
  Go to  ${URL}
  :FOR  ${INDEX}  IN RANGE  1  6
  \  Page should contain a correct date  ${DAY}  ${MONTH}  ${YEAR}
  \  ${DAY}  ${MONTH}  ${YEAR} =  Add days to a date  ${DAY}  ${MONTH}  ${YEAR}
  \  ...  ${REPEAT_EACH}
  Run Keyword If  ${ENDED_AFTER} > 6
  ...  Page should contain more occurrences  ${ENDED_AFTER}

Page should contain a correct date
  [Arguments]  ${DAY}  ${MONTH}  ${YEAR}
  ${FORMAT_DATE} =  Format a date  ${DAY}  ${MONTH}  ${YEAR}
  Page should contain  ${FORMAT_DATE}

Page should contain more occurrences
  [Arguments]  ${ENDED_AFTER}
  ${MORE_OCCURRENCES} =  Evaluate  ${ENDED_AFTER} - 6
  Page should contain  There are ${MORE_OCCURRENCES} more occurrences.
