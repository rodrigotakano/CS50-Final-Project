import sqlite3
from flask import Flask, redirect, render_template, request
from helpers import injection_check, Add

# Configure application
app = Flask(__name__)

# Create database
con = sqlite3.connect("database.db", check_same_thread=False)

# Create cursor to manipulate database
c = con.cursor()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/view")
def view():
    tables = c.execute("SELECT name FROM sqlite_master WHERE type='table';")    
    return render_template("view.html", tables = tables)


@app.route("/table/<tablename>")
def tableview(tablename):

    # Check for user injected malicious characters
    if injection_check(tablename):

        # Fetch table from database and send it to the html template
        table = c.execute("SELECT * FROM {}".format(tablename))
        column_names = [description[0] for description in table.description]        
        return render_template("table.html", table = table, column_names = column_names, tablename = tablename)
    else:
        return render_template("error.html")
    

@app.route("/add", methods=["POST"])
def add():    
    tablename = request.form.get("table") 

    # Check for user injected malicious characters
    if injection_check(tablename):

        # Fetch table from database
        table = c.execute("SELECT * FROM {}".format(tablename))
        column_names = [description[0] for description in table.description]
        
        # Create and populate list with values to be added to columns
        values = []  
        for i in range(len(column_names)):                                   
            values.append(request.form.get("{}".format(i)))
        
        # Call class to make the '?' placeholders in the sqlite execute method
        columns = Add(column_names)       

        # Insert values into table
        c.execute("INSERT INTO {} VALUES({})".format(tablename, columns.placeholders()), values)
                                             
   
    # If table name contains malicious characters 
    else:
        return render_template("error.html")  

    
    
    

    """
    if injection_check(tablename):
        column_count = c.execute("SELECT COUNT(*) FROM pragma_table_info('{}')".format(tablename))
        column_count = int(list(column_count)[0][0])
        print(column_count)
        for i in range(column_count - 1):
            

        return render_template("add.html")
    else:
        return render_template("add.html")
    """

    return render_template("add.html")

 