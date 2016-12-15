*** Settings ***

Force Tags  wip-not_in_docs

Library   Selenium2Library
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote

# Suite Setup  Open browser  ${PLONE_URL}  chrome
Test Setup  Open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Test Cases ***

Create a news item Prueba
  Login as admin user
  Active test folder
  Create a news item '${PLONE_URL}/robot-test-folder' 'Prueba'
  Page should contain  Element creat

Marking as important news item
  Login as admin user
  Active test folder
  Create a news item '${PLONE_URL}/robot-test-folder' 'Prueba'
  Go to  ${PLONE_URL}/robot-test-folder/prueba
  Page should contain  Marca com a important
  Click To Change Important
  Page should contain  L'element s'ha marcat com important
  Click Confirm Button
  Page should contain  Desmarca com a important

Desmarking as important news item
  Login as admin user
  Active test folder
  Create a news item '${PLONE_URL}/robot-test-folder' 'Prueba'
  Go to  ${PLONE_URL}/robot-test-folder/prueba
  Page should contain  Marca com a important
  Click To Change Important
  Page should contain  L'element s'ha marcat com important
  Click Confirm Button
  Page should contain  Desmarca com a important
  Click To Change Important
  Page should contain  L'element s'ha desmarcat com important
  Click Confirm Button
  Page should contain  Marca com a important
