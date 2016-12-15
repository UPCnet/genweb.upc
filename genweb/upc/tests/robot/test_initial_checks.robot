*** Settings ***

Force Tags  wip-not_in_docs

Library   Selenium2Library
Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Test Cases ***

#Login
#  Given we're logged in as admin
#    Then Page should contain  Us heu identificat correctament
#
# Enable Test Folder
#   Given we're logged in as admin
#   When the test folder is activated
#   Then Page should contain  Actualment no hi ha elements dins d'aquesta carpeta.
#
Create default directories
  Given we're logged in as admin
  When the default directories have been created
  Then we verify that everything has been created correctly

*** Keywords ***

the test folder is activated
  Given main page is open
  Then Click Element  xpath=//*[@id="portaltab-robot-test-folder"]/a
  And Click Confirm Button

the default directories have been created
  Given Go to  ${PLONE_URL}/folder_contents
  Then Click Element  xpath=//*[@id="viewlet-above-content"]/div/a
  And Click Button  name=createn3

we verify that everything has been created correctly
  Within the directory Home
  #Within the directory Català
  #Within the directory Español
  #Within the directory English
  #Within the directory Templates
  #Within the directory Plantilles

Within the directory Home
  @{LIST_FOLDER_CONTENTS} =  Català  Español  English  Templates  Plantilles
  Go to  ${PLONE_URL}/folder_contents
  :FOR  ${STRING}  IN  @{LIST_FOLDER_CONTENTS}
  \  Page should contain  ${STRING}


Within the directory Català
  Go to  ${PLONE_URL}/ca/folder_contents
  Page should contain  Notícies
  Page should contain  Esdeveniments
  Page should contain  Banners
  Page should contain  Logos peu
  Page should contain  Benvingut
  Page should contain  Contancte personalitzat
  Page should contain  Fitxers compartits

Within the directory Español
  Go to  ${PLONE_URL}/es/folder_contents
  Page should contain  Noticias
  Page should contain  Eventos
  Page should contain  Banners
  Page should contain  Logos pie
  Page should contain  Bienvenido
  Page should contain  Contacto personalizado
  Page should contain  Ficheros compartidos

Within the directory English
  Go to  ${PLONE_URL}/es/folder_contents
  Page should contain  Noticias
  Page should contain  Eventos
  Page should contain  Banners
  Page should contain  Logos pie
  Page should contain  Bienvenido
  Page should contain  Contacto personalizado
  Page should contain  Ficheros compartidos
