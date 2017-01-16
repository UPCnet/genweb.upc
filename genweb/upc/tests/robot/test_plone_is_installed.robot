*** Settings ***

Force Tags  wip-not_in_docs

Library   Selenium2Library
Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Variables ***

${FOOTER}  Aquest web utilitza cookies pròpies per oferir una millor experiència i servei.

*** Test Cases ***

Homepage is shown
  Given homepage is open
  Then Page should contain  ${FOOTER}
