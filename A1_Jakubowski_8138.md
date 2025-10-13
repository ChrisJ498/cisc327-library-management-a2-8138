Name: Chris Jakubowkski
NetID: 20388138

| Function Name | Implementation Status | Missing |
| ------------- | --------------------- | ------- |
| R1            | Complete              |         |
| R2            | Complete              |         |
| R3            | Partial               | No specific interface (only in catalog)|
| R4            | Partial               | Not usable, needs verification, updating availability, record return date, calculate/display late fees|
| R5            | Missing               | All features|
| R6            | Partial               | Needs working search functions|
| R7            | Missing               | All features|


Test Script Summary:

R2, R6, R7 unfortunatly test scripts not created

R1-Add book to catalog:
    Tests valid addition, invalids for ISBN, invalid copy amount, invalid author
    Performs as expected

R3-Borrow book:
    Tests valid borrowing, invalids for patron id, invalids for book id
    Gives false positive when letters in patron id

R4-Return book:
    Tests valid return, invalids for patron id, invalids for book id
    Does not perform since R4 code not implemented

R5-Late fee:
    Tests no late fee, invalids for patron id, invalid for book id
    Does not perform since R5 code not implemented