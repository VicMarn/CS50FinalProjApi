# CS50FinalProjApi
API, developed with Flask, to act as the server-side of my CS50's final project.

>This is the server side of my CS50's final project, if you wanna take a look at the client side, [click here](https://github.com/VicMarn/CS50FinalProjApp)

Running Tracker is a native Android app, developed with Jetpack Compose, whose purpose is to track running activities and present them to the user in a user-friendly UI.
The main idea of the app is to serve as a system that a person who practices running can use to record each of their training sessions or competitive runs. Although, theorically, it can also be used for other long-distance sports, such as cycling, swimming, triathlon or even hiking.

The app has 5 features:
1. **Create record**
2. **Delete record**
3. **Get all records**
4. **Get summary**
5. **Get weather forecast**

Each record is composed of the following data:
- **Date**
- **Time**
- **Distance**
- **Comment**

**Date** -> Date is simply the day in which the acitivity happened.

**Time** -> The amount of time it took for the user to complete the activity.

**Distance** -> The amount of space, in kilometers, the user traveled during the activity.

**Comment** -> Comment is simply a small text input the user can write to make an observation about the activity, such as "Today my performance was pretty good" or "performance was not the best today".

The system uses a client-server architecture, the Android app being the client and a REST API being the server-side.
The client side is a native Android app, which was developed using Jetpack Compose toolkit and also the third party libraries Retrofit and Coil.
The server side is a REST API developed with Flask, SQLAlchemy and SQLite for the database.

The client and server communicate through JSON.

All the API's bussiness logic is written inside the app.py file.
Inside the file, first Flask and the SQLITE database are configured.
A class called ActivityRecord is defined to model the only table present on the database, activity_record, which has the following fields:
- **id**
- **date**
- **distance**
- **time**
- **comment**

**Id** -> The table's primary key and it auto-increments, so it doesn't need to be filled by the user.

**Date** -> Declared with the Date data type, can't be nullable, and has the restrictions a normal date would have, such as the user being unable to enter February 31 2024 or July 45 2021, for example.

**Distance** -> A float with 2 decimal places, can't be nullable.

**Time** -> Declared with the time data type, can't be nullable and has some restrictions: hour has to be in the range 0..23, minutes and seconds have both to be in the range 0..59. Time represents the amount of time it took for the user to finish the activity, although it's being stored in the database as a specific time in a day.

**Comment** -> A string which can have a maximum of 350 characters and call be null.


The api has 4 routes defined, they are:
- **/**
- **/records**
- **/record/\<id\>**
- **/summary**

**/** -> Just redirects to /records

**/records** -> Allows two methods: GET and POST. records_get simply gets all records in the activity_record table, including all the 5 fields. records_post takes the user input via the request object, creates a new ActivityRecord object and stores it in the database. If any type of value exception occurs, the API catches the exception and returns status code 400: Bad Request.

**/records/\<id\>** -> Allows the DELETE method only. It takes an id input from the user and query the database for a record with that id. If the record is found, it is properly deleted, otherwise the API returns status code 404: Resource not Found.

**/summary** -> Allows GET method only. The summary route returns three values: number_of_days, which uses func.count method to count the total amount of records in the table. total_distance, which uses func.sum to sum the values from the whole distance column. total_time, which does a calculation to return the total time, in seconds, that the user has spend during the activities. The formula is the following: 3600 * sum(hours) + 60 * sum(minutes) + sum(seconds).


The app.py file also includes two helper functions:

**formatTime(timeString)** -> Which takes a list with the time values as a parameters and corrects possible value errors that could cause an exception. formatTime replaces empty strings with "00" and replaces negative numbers with 0. This function gets called inside records_post to avoid exceptions.

**handle_exception(e):** -> This function takes an HTTPException object as argument and returns a json with the values: code, name and description

> Python's built-in Venv module was used to manage the virtual environment and specific dependencies for the server side of this project.
> The dependencies can be found in requirements.txt file and can be installed using the command: `pip install -r requirements.txt`



