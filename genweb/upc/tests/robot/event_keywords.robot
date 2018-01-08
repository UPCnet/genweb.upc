*** Settings ***

Library  Selenium2Library

Resource  keywords.robot
Resource  date_keywords.robot

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
  Save form

recurrence has been added
  [Arguments]  ${URL}  ${REPEAT_EACH}  ${ENDED_AFTER}
  Go to  ${URL}/edit
  Click Element  name=riedit
  Input Text  name=ridailyinterval  ${REPEAT_EACH}
  Input Text  name=rirangebyoccurrencesvalue  ${ENDED_AFTER}
  Click Element  id=rirtemplate
  Click Button  xpath=//*[@id="rirtemplate"]/div/div[5]/input[2]
  Save form

Select Date
  [Arguments]  ${DAY}  ${MONTH}  ${YEAR}
  Select From List By Value  id=form-widgets-IEventBasic-start-year  ${YEAR}
  Select From List By Value  id=form-widgets-IEventBasic-start-month  ${MONTH}
  Select From List By Value  id=form-widgets-IEventBasic-start-day  ${DAY}
  
Input IEC_Text
  [Arguments]  ${FIELD}  ${TEXT}
  Input Text  id=form-widgets-IEventContact-${FIELD}  ${TEXT}
