*** Settings ***

Library  Selenium2Library
Library  Collections

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

the default directories have been created
  Given Go to  ${PLONE_URL}/folder_contents
  Then Click Element  xpath=//*[@id="viewlet-above-content"]/div/a
  And Click Button  name=createn3

the test folder is activated
  Given main page is open
  Then Click Element  xpath=//*[@id="portaltab-robot-test-folder"]/a
  And confirm action

confirm action
  Click Button  name=form.button.confirm

save form
  ${STATUS} =  Run Keyword And Return Status
  ...  Page Should Contain Element	name=form.buttons.save
  Run Keyword If  ${STATUS}
  ...  Click Button  name=form.buttons.save
  ...  ELSE
  ...  Click Button  name=form.actions.save

it has been created a simple item
  [Arguments]  ${URL}  ${ITEM}  ${TITLE}
  Go to  ${URL}
  Click Element  id=plone-contentmenu-factories
  Click Element  id=${ITEM}
  Input F_Text  title  ${TITLE}
  save form

added a tag
  [Arguments]  ${URL}  @{TAGS}
  Go to  ${URL}/edit
  Click Element  //*[span[text()="Categorització"]]
  : FOR  ${TAG}  IN  @{TAGS}
  \  Input Text  id=s2id_autogen1  ${TAG}
  \  Wait Until Page Contains Element  xpath=//*[@class="select2-match"][text()="${TAG}"]  timeout=1
  \  Click Element  xpath=//*[@class="select2-match"][text()="${TAG}"]
  save form

status has been passed to public
  [Arguments]  ${URL}
  Go to  ${URL}
  Click Element  id=plone-contentmenu-workflow
  Click Element  id=workflow-transition-publish
  confirm action

different items have been created with tags
  [Arguments]  @{DATA}
  :FOR  ${DATA_PORTLET}  IN   @{DATA}
  \  ${URL} =  Get From List  ${DATA_PORTLET}  0
  \  ${ITEM} =  Get From List  ${DATA_PORTLET}  1
  \  ${TITLE_URL} =  Get From List  ${DATA_PORTLET}  2
  \  it has been created a simple item  ${URL}  ${ITEM}  ${TITLE_URL}
  \  ${LENGTH} =  Get Length   ${DATA_PORTLET}
  \  @{TAGS} =
  \  ...  Run Keyword If  ${LENGTH} > 3
  \  ...  Get Slice From List  ${DATA_PORTLET}  3
  \  Run Keyword If  ${LENGTH} > 3
  \  ...  added a tag  ${URL}/${TITLE_URL}   @{TAGS}

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
