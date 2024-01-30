# SQL MANAGER
 This is the final project for the CS50 course

## DISCLAIMER: Due to SQLite limitations, this app is not entirely safe from injection attacks. Please do not use it to store sensitive data, as it was made purely for learning purposes

### Video Demo:  <https://www.youtube.com/watch?v=s2Oj5LYdENE>

### Description: This web-app allows you to perform various actions on a SQLite Database, such as create and delete tables, and add and delete rows from them.  


### Contents:

The file "app.py" contains the main portion of the code, that deals with the app's backend via Flask.
There is also a auxiliary file called "helpers.py" with some functions to allow the implementations of some features.\
In the "templates" folder are the html files for the multiple pages from the app, such as the layout, and the index page. There is also a "styles.css" file in the "static" folder containing some css styles used.\  
For the html pages, various Bootstrap features were used. 

### Main code:

The main file "app.py" contains the main functionalities from the app.\
The framework used was Flask, so it was possible to create multiple html pages and create links to them, as well as use forms and use data inputted on them via the POST Method.\
For the SQL Database, SQLite was used, as it is free and simple to use.\

The main problem encountered when writing this code was the injection attack safety. The issue is that SQLite does not allow the Placeholders (?) input method when providing the name of a table. As an alternative, the name of the table is sent to the SQLite Query via a string, which is not a safe proccess. To try to make up for it, in the file "helpers.py" there is a function that checks if the string sent to the query has any malicious characters, such as single quotes, or hyphens. 

### Functionalities:

#### Create tables
It is possible to create new tables to the database. You can choose the number of columns needed, as well as the datatype for each of them.

#### View tables
View all the existing tables from the database

#### Drop tables
Drop a table from the database

#### Add rows to table
Add a row of values to a table

#### Delete rows from table
Delete a row of values from a table

### To be added:

#### Primary/Foreign keys
A useful feature when creating relational databases is the ability to add primary and foreign keys to a table. This feature was not implemented because it would increase the complexity of the project, so it was not within my time scope.

#### Injection attack safety
It would be very important to find a workaround to SQLite limitations regarding the values accepted when creating a table from a python query. This would allow better safety against injection attacks.



