*** Settings ***

Force Tags  wip-not_in_docs

Library  Selenium2Library

Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot
Resource  date_keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Variables ***

# You can change the values for @{START_DATE} and @{RECURRENCE_DATA}
${URL_FOLDER}  ${PLONE_URL}/robot-test-folder
${NEWS_ID}  prueba
@{START_DATE}  29  12  2016
@{EVENT_DATA}  titol-de-prova  Descripció de prova  @{START_DATE}
...            Ubicació de prova  Assistent de prova  Contacte de prova
...            correu@de.prova  933030303  http://www.google.com  Text de prova
# To avoid problems, avoid placing values greater than 999
@{RECURRENCE_DATA}  2  5

*** Test Cases ***

Create a recurring event
  Given we're logged in as admin
  When the test folder is activated
  And it has been created a event  ${URL_FOLDER}  @{EVENT_DATA}
  And recurrence has been added  @{RECURRENCE_DATA}
  Then event should contain  ${URL_FOLDER}/@{EVENT_DATA}[0]  @{EVENT_DATA}
  And event should contain recurrence  ${URL_FOLDER}/@{EVENT_DATA}[0]
  ...  @{START_DATE}  @{RECURRENCE_DATA}

*** Keywords ***

it has been created a event
  [Arguments]  ${URL}  ${TITLE}  ${DESCRIPTION}  ${DAY}  ${MONTH}  ${YEAR}
  ...          ${LOCATION}  ${ATTENDEES}  ${CONTACT_NAME}  ${CONTACT_EMAIL}
  ...          ${CONTACT_PHONE}  ${EVENT_URL}  ${TEXT}
  Go to  ${URL}
  Click Element  id=plone-contentmenu-factories
  Click Element  id=event
  Input F_Text  title  ${TITLE}
  Input F_Text  description  ${DESCRIPTION}
  Select Checkbox  id=form-widgets-IEventBasic-whole_day-0
  Select Checkbox  id=form-widgets-IEventBasic-open_end-0
  Select Date  ${DAY}  ${MONTH}  ${YEAR}
  Input Text  id=form-widgets-IEventLocation-location  ${LOCATION}
  Input Text  id=form-widgets-IEventAttendees-attendees  ${ATTENDEES}
  Input IEC_Text  contact_name  ${CONTACT_NAME}
  Input IEC_Text  contact_email  ${CONTACT_EMAIL}
  Input IEC_Text  contact_phone  ${CONTACT_PHONE}
  Input IEC_Text  event_url  ${EVENT_URL}
  Input F_Rich  text  ${TEXT}
  save form

recurrence has been added
  [Arguments]  ${REPEAT_EACH}  ${ENDED_AFTER}
  Go to  ${URL_FOLDER}/@{EVENT_DATA}[0]/edit
  Click Element  name=riedit
  Input Text  name=ridailyinterval  ${REPEAT_EACH}
  Input Text  name=rirangebyoccurrencesvalue  ${ENDED_AFTER}
  Click Element  id=rirtemplate
  Click Button  xpath=//*[@id="rirtemplate"]/div/div[5]/input[2]
  save form

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

Select Date
  [Arguments]  ${DAY}  ${MONTH}  ${YEAR}
  Select From List By Value  id=form-widgets-IEventBasic-start-day  ${DAY}
  Select From List By Value  id=form-widgets-IEventBasic-start-month  ${MONTH}
  Select From List By Value  id=form-widgets-IEventBasic-start-year  ${YEAR}

Input IEC_Text
  [Arguments]  ${FIELD}  ${TEXT}
  Input Text  id=form-widgets-IEventContact-${FIELD}  ${TEXT}

Page should contain a correct date
  [Arguments]  ${DAY}  ${MONTH}  ${YEAR}
  ${FORMAT_DATE} =  Format a date  ${DAY}  ${MONTH}  ${YEAR}
  Page should contain  ${FORMAT_DATE}

Page should contain more occurrences
  [Arguments]  ${ENDED_AFTER}
  ${MORE_OCCURRENCES} =  Evaluate  ${ENDED_AFTER} - 6
  Page should contain  There are ${MORE_OCCURRENCES} more occurrences.
