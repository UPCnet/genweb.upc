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

save form
  Click Button  name=form.buttons.save

added a tag
  [Arguments]  ${URL}  ${TAG}
  Go to  ${URL}
  Click Element  id=fieldsetlegend-0
  Input Text  id=s2id_autogen1  ${TAG}
  Wait Until Page Contains Element  xpath=//*[@class="select2-match"][text()="${TAG}"]  timeout=1
  Click Element  xpath=//*[@class="select2-match"][text()="${TAG}"]
  save form

Input F_Text
  [Arguments]  ${FIELD}  ${TEXT}
  Input text  name=form.widgets.IDublinCore.${FIELD}  ${TEXT}

Input F_Rich
  [Arguments]  ${FIELD}  ${TEXT}
  Select frame  id=form.widgets.IRichText.${FIELD}_ifr
  Input text  id=content  ${TEXT}
  Unselect frame

Input F_Image
  [Arguments]  ${PATH}
  Choose File  id=form-widgets-ILeadImage-image-input  ${PATH}

Input F_Text_Image
  [Arguments]  ${FIELD}  ${TEXT}
  Input text  name=form.widgets.ILeadImage.${FIELD}  ${TEXT}

Select F_Checkbox
  [Arguments]  ${VALUE}
  Select Checkbox  xpath=//*[@name="form.widgets.ICollection.query.v:records:list"][@value="${VALUE}"]
