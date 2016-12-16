*** Keywords ***

main page is open
  Go to  ${PLONE_URL}

the login page
  Go to  ${PLONE_URL}/login_form

we're logged in as admin
  Given the login page
  Then Click Element  xpath=//*[@id="accordionLogin"]/div[2]/div[1]/a
  And Input Text  name=__ac_name  admin
  And Input Password  name=__ac_password  secret
  And Click Button  name=submit

the test folder is activated
  Given main page is open
  Then Click Element  xpath=//*[@id="portaltab-robot-test-folder"]/a
  And confirm action

confirm action
  Click Button  name=form.button.confirm
