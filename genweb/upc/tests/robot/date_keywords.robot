*** Keywords ***

Add days to a date
  # To avoid problems, avoid placing too many numbers
  [Arguments]  ${DAY}  ${MONTH}  ${YEAR}  ${ADD_DAYS}
  : FOR  ${LOOP}  IN RANGE  1  999999
  \  @{TOTAL_DAYS_FOR_MONTH} =  Return day of each month  ${YEAR}
  \  ${AMONTH} =  Evaluate  ${MONTH} - 1
  \  ${MAX_DAYS} =  Set Variable  @{TOTAL_DAYS_FOR_MONTH}[${AMONTH}]
  \  ${DAY}  ${MONTH}  ${YEAR}  ${ADD_DAYS} =
  \  ...  Run Keyword If  (${DAY} + ${ADD_DAYS}) <= ${MAX_DAYS}
  \  ...  Add Days 1  ${DAY}  ${MONTH}  ${YEAR}  ${ADD_DAYS}  ${MAX_DAYS}
  \  ...  ELSE IF  (${DAY} + ${ADD_DAYS}) > ${MAX_DAYS} and (${MONTH} + 1) <= 12
  \  ...  Add Days 2  ${DAY}  ${MONTH}  ${YEAR}  ${ADD_DAYS}  ${MAX_DAYS}
  \  ...  ELSE IF  (${DAY} + ${ADD_DAYS}) > ${MAX_DAYS} and (${MONTH} + 1) > 12
  \  ...  Add Days 3  ${DAY}  ${MONTH}  ${YEAR}  ${ADD_DAYS}  ${MAX_DAYS}
  \  Exit For Loop If  ${ADD_DAYS} == 0
  [Return]  ${DAY}  ${MONTH}  ${YEAR}

Return day of each month
  [Arguments]  ${YEAR}
  @{DAYS} =
  ...  Run Keyword If  ((${YEAR} % 4 == 0) and ((${YEAR} % 100 != 0) or (${YEAR} % 400 == 0)))
	...  Set Variable  31  29  31  30  31  30  31  31  30  31  30  31
  ...  ELSE
  ...  Set Variable  31  28  31  30  31  30  31  31  30  31  30  31
  [Return]  @{DAYS}

Add Days 1
  [Arguments]  ${DAY}  ${MONTH}  ${YEAR}  ${ADD_DAYS}  ${MAX_DAYS}
  ${DAY} =  Evaluate  ${DAY} + ${ADD_DAYS}
  ${ADD_DAYS} =  Set Variable  0
  [Return]  ${DAY}  ${MONTH}  ${YEAR}  ${ADD_DAYS}

Add Days 2
  [Arguments]  ${DAY}  ${MONTH}  ${YEAR}  ${ADD_DAYS}  ${MAX_DAYS}
  ${ADD_DAYS} =  Evaluate  ${ADD_DAYS} - (${MAX_DAYS} - ${DAY}) - 1
  ${MONTH} =  Evaluate  ${MONTH} + 1
  ${DAY} =  Set Variable  1
  [Return]  ${DAY}  ${MONTH}  ${YEAR}  ${ADD_DAYS}

Add Days 3
  [Arguments]  ${DAY}  ${MONTH}  ${YEAR}  ${ADD_DAYS}  ${MAX_DAYS}
  ${ADD_DAYS} =  Evaluate  ${ADD_DAYS} - (${MAX_DAYS} - ${DAY}) - 1
  ${YEAR} =  Evaluate  ${YEAR} + 1
  ${MONTH} =  Set Variable  1
  ${DAY} =  Set Variable  1
  [Return]  ${DAY}  ${MONTH}  ${YEAR}  ${ADD_DAYS}

Format a date
  [Arguments]  ${DAY}  ${MONTH}  ${YEAR}
  ${DAY} =
  ...  Run Keyword If  ${DAY} < 10
  ...  Set Variable  0${DAY}
  ...  ELSE
  ...  Set Variable  ${DAY}
  ${MONTH} =
  ...  Run Keyword If  ${MONTH} < 10
  ...  Set Variable  0${MONTH}
  ...  ELSE
  ...  Set Variable  ${MONTH}
  [Return]  ${DAY}/${MONTH}/${YEAR}
