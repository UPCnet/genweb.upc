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

Click To Change Important
  Click Element  xpath=//*[@id="viewlet-above-content-title"]/div[1]/div/a

Click Confirm Button
  Click Button  name=form.button.confirm

Create a news item
  [Arguments]  ${URL}  @{TITLE}
  Go to  ${URL}
  Click Element  id=plone-contentmenu-factories
  Click Element  id=news-item
  Input Text  name=form.widgets.IDublinCore.title  ${TITLE}
  Click Button  name=form.buttons.save

An important news item
  [Arguments]  ${URL}  @{TITLE}
  Go to  ${URL}
  Click Element  id=plone-contentmenu-factories
  Click Element  id=news-item
  Input Text  name=form.widgets.IDublinCore.title  ${TITLE}
  Click Button  name=form.buttons.save
