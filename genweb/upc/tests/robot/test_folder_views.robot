*** Settings ***

Force Tags  wip-not_in_docs

Library  Selenium2Library
Library	 OperatingSystem
Library  Collections

Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open browser  ${PLONE_URL}  chrome
Test Teardown  Close all browsers

*** Variables ***

${TEST_FOLDER}  ${PLONE_URL}/robot-test-folder

@{NEWS_ITEM}  ${TEST_FOLDER}  news-item  Títol notícia  Descripció notícia
@{DOCUMENT}  ${TEST_FOLDER}  document  Títol document  Descripció document
@{IMAGE}  ${TEST_FOLDER}  image  Títol imatge  Descripció imatge
...  ${CURDIR}/img/sample.png
@{OTHER_FOLDER}  ${TEST_FOLDER}  folder  Títol carpeta  Descripció carpeta
@{OTHER_DOCUMENT}  ${TEST_FOLDER}/titol-carpeta  document  Títol altre document
...  Descripció altre document

*** Test Cases ***

Checking different folder views
  Given we're logged in as admin
  When multiple contents have been created in test folder
  Then standard view should then display the contents correctly
  And extended view should then display the contents correctly
  And album view should then display the contents correctly
  And summary view should then display the contents correctly
  And tabular view should then display the contents correctly
  And all content view should then display the contents correctly
  And contents index view should then display the contents correctly

*** Keywords ***

multiple contents have been created in test folder
  Given the test folder is activated
  When create a multiple contents

create a multiple contents
  @{DATA_CREATE} =  Set Variable  ${NEWS_ITEM}  ${DOCUMENT}  ${OTHER_FOLDER}
  ...  ${OTHER_DOCUMENT}
  : FOR  ${CONTENT}  IN  @{DATA_CREATE}
  \  ${URL}  ${TYPE}  ${TITLE}  ${DESCRIPTION} =  Set Variable  ${CONTENT}
  \  it has been created a simple item  ${URL}  ${TYPE}  ${TITLE}  ${DESCRIPTION}
  Create a image item

Create a image item
  ${URL}  ${TYPE}  ${TITLE}  ${DESCRIPTION}  ${PATH} =  Set Variable  @{IMAGE}
  Go to  ${URL}
  Click Element  id=plone-contentmenu-factories
  Click Element  id=${TYPE}
  Input Text  form-widgets-title  ${TITLE}
  Input Text  form-widgets-description  ${DESCRIPTION}
  Choose File  id=form-widgets-image-input  ${PATH}
  Save form
  Confirm action

Select view in test folder
  [Arguments]  ${TYPE_VIEW}
  Go To  ${TEST_FOLDER}
  Click Element  plone-contentmenu-display
  Click Element  plone-contentmenu-display-${TYPE_VIEW}
  Confirm action

###  Standard view  ###

standard view should then display the contents correctly
  @{VISIBLE_DATA} =  Create List	${NEWS_ITEM}  ${DOCUMENT}  ${IMAGE}  ${OTHER_FOLDER}
  @{NOT_VISIBLE_DATA} =  Create List	${OTHER_DOCUMENT}
  ${TYPE_VIEW} =  Set Variable  listing_view
  Select view in test folder  ${TYPE_VIEW}
  Check that the number of items is correct in stardard view  ${VISIBLE_DATA}
  Check that the content of the items is correct in stardard view
  ...  ${VISIBLE_DATA}  ${NOT_VISIBLE_DATA}

Check that the number of items is correct in stardard view
  [Arguments]  ${DATA}
  ${COUNT} =  Get Matching Xpath Count
  ...  //*[@id='content-core']/dl/dt/span/a/../../../dd/span
  Length Should Be  ${DATA}  ${COUNT}

Check that the content of the items is correct in stardard view
  [Arguments]  ${VISIBLE_DATA}  ${NOT_VISIBLE_DATA}
  : FOR  ${ELEMENT}  IN  @{VISIBLE_DATA}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/dl/dt/span/a[text() = '${TITLE}']
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/dl/dd/span[text() = '${DESCRIPTION}']
  : FOR  ${ELEMENT}  IN  @{NOT_VISIBLE_DATA}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/dl/dt/span/a[text() = '${TITLE}']
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/dl/dd/span[text() = '${DESCRIPTION}']

###  Extended view  ###

extended view should then display the contents correctly
  @{VISIBLE_DATA} =  Create List	${NEWS_ITEM}  ${DOCUMENT}  ${IMAGE}  ${OTHER_FOLDER}
  @{NOT_VISIBLE_DATA} =  Create List	${OTHER_DOCUMENT}
  ${TYPE_VIEW} =  Set Variable  folder_extended
  Select view in test folder  ${TYPE_VIEW}
  Check that the number of items is correct in extended view  ${VISIBLE_DATA}
  Check that the content of the items is correct in extended view
  ...  ${VISIBLE_DATA}  ${NOT_VISIBLE_DATA}

Check that the number of items is correct in extended view
  [Arguments]  ${DATA}
  ${COUNT} =  Get Matching Xpath Count
  ...  //*[@id='content-core']/ul/li/a/../p[2]
  Length Should Be  ${DATA}  ${COUNT}

Check that the content of the items is correct in extended view
  [Arguments]  ${VISIBLE_DATA}  ${NOT_VISIBLE_DATA}
  : FOR  ${ELEMENT}  IN  @{VISIBLE_DATA}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/ul/li/a[text() = '${TITLE}']
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/ul/li/p[text() = '${DESCRIPTION}']
  : FOR  ${ELEMENT}  IN  @{NOT_VISIBLE_DATA}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/ul/li/a[text() = '${TITLE}']
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/ul/li/p[text() = '${DESCRIPTION}']

###  Album view  ###

album view should then display the contents correctly
  @{VISIBLE_DATA} =  Create List	${IMAGE}
  @{NOT_VISIBLE_DATA} =  Create List	${NEWS_ITEM}  ${DOCUMENT}
  ...  ${OTHER_DOCUMENT}  ${OTHER_FOLDER}
  ${TYPE_VIEW} =  Set Variable  album_view
  Select view in test folder  ${TYPE_VIEW}
  Check that the number of items is correct in album view  ${VISIBLE_DATA}
  Check that the content of the items is correct in album view
  ...  ${VISIBLE_DATA}  ${NOT_VISIBLE_DATA}

Check that the number of items is correct in album view
  [Arguments]  ${DATA}
  ${COUNT} =  Get Matching Xpath Count
  ...  //*[@id='content-core']/div/div[@class='photoAlbumEntry']/a/span/img/../../span[2]
  Length Should Be  ${DATA}  ${COUNT}

Check that the content of the items is correct in album view
  [Arguments]  ${VISIBLE_DATA}  ${NOT_VISIBLE_DATA}
  : FOR  ${ELEMENT}  IN  @{VISIBLE_DATA}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/a[contains(@title, '${DESCRIPTION}')]
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/a/span/img[contains(@alt, '${TITLE}')][contains(@title, '${TITLE}')]
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/a/span[text() = '${TITLE}']
  : FOR  ${ELEMENT}  IN  @{NOT_VISIBLE_DATA}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/a[contains(@title, '${DESCRIPTION}')]
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/a/span/img[contains(@alt, '${TITLE}')][contains(@title, '${TITLE}')]
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/a/span[text() = '${TITLE}']

###  Summary view  ###

summary view should then display the contents correctly
  @{VISIBLE_DATA_IMAGE} =  Create List	${IMAGE}
  @{VISIBLE_DATA_NOT_IMAGE} =  Create List	${NEWS_ITEM}  ${DOCUMENT}  ${OTHER_FOLDER}
  @{NOT_VISIBLE_DATA} =  Create List	${OTHER_DOCUMENT}
  ${TYPE_VIEW} =  Set Variable  summary_view
  Select view in test folder  ${TYPE_VIEW}
  Check that the number of items is correct in summary view  ${VISIBLE_DATA_IMAGE}
  ...  ${VISIBLE_DATA_NOT_IMAGE}
  Check that the content of the items is correct in summary view
  ...  ${VISIBLE_DATA_IMAGE}  ${VISIBLE_DATA_NOT_IMAGE}  ${NOT_VISIBLE_DATA}

Check that the number of items is correct in summary view
  [Arguments]  ${DATA_IMAGE}  ${DATA_NOT_IMAGE}
  ${IMAGE} =  Get Matching Xpath Count
  ...  //*[@id='content-core']/article/div/a/img/../../../h2/a/../../span/../p/span/../../p[2]/../div[2][@class='visualClear']
  Length Should Be  ${DATA_IMAGE}  ${IMAGE}
  ${NOT_IMAGE} =  Get Matching Xpath Count
  ...  //*[@id='content-core']/article/h2/a/../../span/../p/span/../../p[2]/../div[1][@class='visualClear']
  Length Should Be  ${DATA_NOT_IMAGE}  ${NOT_IMAGE}

Check that the content of the items is correct in summary view
  [Arguments]  ${VISIBLE_DATA_IMAGE}  ${VISIBLE_DATA_NOT_IMAGE}  ${NOT_VISIBLE_DATA}
  : FOR  ${ELEMENT}  IN  @{VISIBLE_DATA_IMAGE}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/article/div/a/img[contains(@alt, '${TITLE}')][contains(@title, '${TITLE}')]
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/article/h2/a[text() = '${TITLE}']
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/article/p/span[text() = '${DESCRIPTION}']
  : FOR  ${ELEMENT}  IN  @{VISIBLE_DATA_NOT_IMAGE}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/article/div/a/img[contains(@alt, '${TITLE}')][contains(@title, '${TITLE}')]
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/article/h2/a[text() = '${TITLE}']
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/article/p/span[text() = '${DESCRIPTION}']
  : FOR  ${ELEMENT}  IN  @{NOT_VISIBLE_DATA}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/article/div/a/img[contains(@alt, '${TITLE}')][contains(@title, '${TITLE}')]
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/article/h2/a[text() = '${TITLE}']
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/article/p/span[text() = '${DESCRIPTION}']

###  Tabular view  ###

tabular view should then display the contents correctly
  @{VISIBLE_DATA} =  Create List	${NEWS_ITEM}  ${DOCUMENT}  ${IMAGE}  ${OTHER_FOLDER}
  @{NOT_VISIBLE_DATA} =  Create List	${OTHER_DOCUMENT}
  ${TYPE_VIEW} =  Set Variable  tabular_view
  Select view in test folder  ${TYPE_VIEW}
  Check that the number of items is correct in tabular view  ${VISIBLE_DATA}
  Check that the content of the items is correct in tabular view
  ...  ${VISIBLE_DATA}  ${NOT_VISIBLE_DATA}

Check that the number of items is correct in tabular view
  [Arguments]  ${DATA}
  ${COUNT} =  Get Matching Xpath Count
  ...  //*[@id='content-core']/div/table/tbody/tr/td/a[@title]
  Length Should Be  ${DATA}  ${COUNT}

Check that the content of the items is correct in tabular view
  [Arguments]  ${VISIBLE_DATA}  ${NOT_VISIBLE_DATA}
  : FOR  ${ELEMENT}  IN  @{VISIBLE_DATA}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/table/tbody/tr/td/a[text() = '${TITLE}']
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/table/tbody/tr/td/a[contains(@title, '${DESCRIPTION}')]
  : FOR  ${ELEMENT}  IN  @{NOT_VISIBLE_DATA}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/table/tbody/tr/td/a[text() = '${TITLE}']
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/table/tbody/tr/td/a[contains(@title, '${DESCRIPTION}')]

###  All contents  ###

all content view should then display the contents correctly
  @{VISIBLE_DATA_NOT_IMAGE} =  Create List	${NEWS_ITEM}  ${DOCUMENT}  ${OTHER_FOLDER}
  @{VISIBLE_DATA_IMAGE} =  Create List	${IMAGE}
  @{VISIBLE_DATA_INSIDE_FOLDER} =  Create List	${OTHER_DOCUMENT}
  ${TYPE_VIEW} =  Set Variable  full_view
  Select view in test folder  ${TYPE_VIEW}
  Check that the number of items is correct in all content view
  ...  ${VISIBLE_DATA_IMAGE}  ${VISIBLE_DATA_NOT_IMAGE}  ${VISIBLE_DATA_INSIDE_FOLDER}
  Check that the content of the items is correct in all content view
  ...  ${VISIBLE_DATA_IMAGE}  ${VISIBLE_DATA_NOT_IMAGE}  ${VISIBLE_DATA_INSIDE_FOLDER}

Check that the number of items is correct in all content view
  [Arguments]  ${DATA_IMAGE}  ${DATA_NOT_IMAGE}  ${DATA_INSIDE_FOLDER}
  ${IMAGE} =  Get Matching Xpath Count
  ...  //*[@id='content-core']/div/h2/a/../../div[@class='description']/../div/figure/a/img
  Length Should Be  ${DATA_IMAGE}  ${IMAGE}
  ${NOT_IMAGE} =  Get Matching Xpath Count
  ...  //*[@id='content-core']/div/h2/a/../../div[@class='description'][not(../div/figure)]
  Length Should Be  ${DATA_NOT_IMAGE}  ${NOT_IMAGE}
  ${INSIDE_FOLDER} =  Get Matching Xpath Count
  ...  //*[@id='content-core']/div/h2/a/../../div[@class='description']/../div/dl/dt/span[@class='summary']/a/../../../dd/span
  Length Should Be  ${DATA_INSIDE_FOLDER}  ${INSIDE_FOLDER}

Check that the content of the items is correct in all content view
  [Arguments]  ${VISIBLE_DATA_IMAGE}  ${VISIBLE_DATA_NOT_IMAGE}
  ...  ${VISIBLE_DATA_INSIDE_FOLDER}
  : FOR  ${ELEMENT}  IN  @{VISIBLE_DATA_IMAGE}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/h2/a[text()='${TITLE}']
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div[@class='description' and text()='${DESCRIPTION}']
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/figure/a/img[contains(@alt, '${TITLE}')][contains(@title, '${TITLE}')]
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/dl/dt/span/a[text()='${TITLE}']
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/dl/dd/span[text()='${DESCRIPTION}']
  : FOR  ${ELEMENT}  IN  @{VISIBLE_DATA_NOT_IMAGE}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/h2/a[text()='${TITLE}']
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div[@class='description' and text()='${DESCRIPTION}']
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/figure/a/img[contains(@alt, '${TITLE}')][contains(@title, '${TITLE}')]
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/dl/dt/span/a[text()='${TITLE}']
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/dl/dd/span[text()='${DESCRIPTION}']
  : FOR  ${ELEMENT}  IN  @{VISIBLE_DATA_INSIDE_FOLDER}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/h2/a[text()='${TITLE}']
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div[@class='description' and text()='${DESCRIPTION}']
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/figure/a/img[contains(@alt, '${TITLE}')][contains(@title, '${TITLE}')]
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/dl/dt/span/a[text()='${TITLE}']
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/div/dl/dd/span[text()='${DESCRIPTION}']

###  Contents view  ###

contents index view should then display the contents correctly
  @{VISIBLE_DATA_OUTSIDE_FOLDER} =  Create List	${NEWS_ITEM}  ${DOCUMENT}  ${IMAGE}
  ...  ${OTHER_FOLDER}
  @{VISIBLE_DATA_INSIDE_FOLDER} =  Create List	${OTHER_DOCUMENT}
  ${TYPE_VIEW} =  Set Variable  folder_index_view
  Select view in test folder  ${TYPE_VIEW}
  Check that the number of items is correct in contents index view
  ...  ${VISIBLE_DATA_OUTSIDE_FOLDER}  ${VISIBLE_DATA_INSIDE_FOLDER}
  Check that the content of the items is correct in contents index view
  ...  ${VISIBLE_DATA_OUTSIDE_FOLDER}  ${VISIBLE_DATA_INSIDE_FOLDER}

Check that the number of items is correct in contents index view
  [Arguments]  ${VISIBLE_DATA_OUTSIDE_FOLDER}  ${VISIBLE_DATA_INSIDE_FOLDER}
  ${OUTSIDE_FOLDER} =  Get Matching Xpath Count
  ...  //*[@id='content-core']/div/ul/li/h3/a
  Length Should Be  ${VISIBLE_DATA_OUTSIDE_FOLDER}  ${OUTSIDE_FOLDER}
  ${INSIDE_FOLDER} =  Get Matching Xpath Count
  ...  //*[@id='content-core']/div/ul/li/ul/li/a
  Length Should Be  ${VISIBLE_DATA_INSIDE_FOLDER}  ${INSIDE_FOLDER}

Check that the content of the items is correct in contents index view
  [Arguments]  ${VISIBLE_DATA}  ${NOT_VISIBLE_DATA}
  : FOR  ${ELEMENT}  IN  @{VISIBLE_DATA}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/ul/li/h3/a[text()='${TITLE}']
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/ul/li/ul/li/a[text()='${TITLE}']
  : FOR  ${ELEMENT}  IN  @{NOT_VISIBLE_DATA}
  \  ${TITLE} =  Get From List  ${ELEMENT}  2
  \  ${DESCRIPTION} =  Get From List  ${ELEMENT}  3
  \  Page Should Not Contain Element
  \  ...  xpath=//*[@id='content-core']/div/ul/li/h3/a[text()='${TITLE}']
  \  Page Should Contain Element
  \  ...  xpath=//*[@id='content-core']/div/ul/li/ul/li/a[text()='${TITLE}']
