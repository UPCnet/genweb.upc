*** Settings ***

Force Tags  wip-not_in_docs

Library  Selenium2Library

Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot
Resource  date_keywords.robot
Resource  event_keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Variables ***

# You can change the values for @{START_DATE} and @{RECURRENCE_DATA}
${URL_FOLDER}  ${PLONE_URL}/ca/esdeveniments
${EVENT_ID}  titol-de-prova
${URL_EVENT}  ${URL_FOLDER}/${EVENT_ID}
@{START_DATE}  15  12  2026
@{EVENT_DATA}  ${EVENT_ID}  Descripció de prova  @{START_DATE}
...            Ubicació de prova  Assistent de prova  Contacte de prova
...            correu@de.prova  933030303  http://www.google.com  Text de prova
# To avoid problems, avoid placing values greater than 100
@{RECURRENCE_DATA}  2  5
${ITEMS_TO_DISPLAY}  5

*** Test Cases ***

Create event portlet with recurring event
  Given we're logged in as admin
  When it has been created a public event with recurrence in event folder
  And a event portlet has been created in homepage
  Then portlet event should contain the data and recurrence in homepage

*** Keywords ***

it has been created a public event with recurrence in event folder
  Given the default directories have been created
  When it has been created a event  ${URL_FOLDER}  @{EVENT_DATA}
  And recurrence has been added  ${URL_EVENT}  @{RECURRENCE_DATA}
  And status has been passed to public  ${URL_EVENT}

portlet event should contain the data and recurrence in homepage
  portlet event should contain in homepage
  portlet event should contain recurrence in homepage

a event portlet has been created in homepage
  Go to  ${PLONE_URL}/@@manage-homeportlets
  Confirm action
  Click Element  xpath=//*[@id="portletselectorform"]/div/button
  Click Element  xpath=//*[@id="gwportletselector"]/li/a[text()="Agenda"]
  Input Text  id=form.count  ${ITEMS_TO_DISPLAY}
  Save form

portlet event should contain in homepage
  Open homepage
  Page should contain  ${EVENT_ID}
  Page should contain a correct date  @{START_DATE}

portlet event should contain recurrence in homepage
  Open homepage
  ${DAY}  ${MONTH}  ${YEAR} =  Set Variable  @{START_DATE}
  ${REPEAT_EACH}  ${ENDED_AFTER} =  Set Variable  @{RECURRENCE_DATA}
  :FOR  ${INDEX}  IN RANGE  1  ${ITEMS_TO_DISPLAY}
  \  Page should contain a correct date  ${DAY}  ${MONTH}  ${YEAR}
  \  ${DAY}  ${MONTH}  ${YEAR} =  Add days to a date  ${DAY}  ${MONTH}  ${YEAR}
  \  ...  ${REPEAT_EACH}

Page should contain a correct date
  [Arguments]  ${DAY}  ${MONTH}  ${YEAR}
  ${DATE} =  Format a date  ${DAY}  ${MONTH}  ${YEAR}
  Page should contain element  xpath=//*[time[@datetime="${DATE}"]]
