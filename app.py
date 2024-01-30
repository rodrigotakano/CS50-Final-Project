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
        table = c.execute("SELECT rowid,* FROM {}".format(tablename))
        
        # Transform sqlite cursor object to list
        table_shown = []
        for i in table:
            table_shown.append(i)

        # Create separate lists for rowid and displayed table
        table_rowid = []
        table_temp = []       
        for index, i in enumerate(table_shown):
            table_rowid.append(table_shown[index][0])
            table_temp.append(table_shown[index][1:])               
        table_shown = table_temp                   
        
        column_names = [description[0] for description in table.description[1:]]  
             
        return render_template("table.html", table_shown = table_shown, table_rowid = table_rowid, column_names = column_names, tablename = tablename)
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
        con.commit()     
        

        return render_template("add.html", tablename=tablename)                                
   
    # If table name contains malicious characters 
    else:
        return render_template("error.html")    
       
    
@app.route("/delete", methods=["POST"])
def delete():  
    tablename = request.form.get("table")

    # Check for user injected malicious characters
    if injection_check(tablename):

        # Fetch table from database
        table = c.execute("SELECT rowid,* FROM {}".format(tablename))        

        # Get which row was selected to be deleted
        rowid = int(request.form.get("rowid"))       
                
        c.execute("DELETE FROM {} WHERE rowid={}".format(tablename, rowid))
        con.commit()
        return render_template("delete.html", tablename=tablename)

    # If table name contains malicious characters 
    else:
        return render_template("error.html") 

    
@app.route("/create", methods=["GET", "POST"])
def create():           
    if request.method == "GET":
        return render_template("create.html")
    
    elif request.method == "POST":
        tablename = request.form.get("tablename")
        if injection_check(tablename):
            column_number = request.form.get("column_number")
            if column_number.isdigit():
                column_number = int(column_number)
                datatypes = ["NULL", "INTEGER", "REAL", "TEXT", "BLOB"]
                return render_template("create_parameters.html", column_number=column_number, datatypes=datatypes, tablename=tablename)                
            else:
                return render_template("error.html")
        else:
            return render_template("error.html")
        
    
@app.route("/newtable", methods=["POST"])
def newtable():

    # Get parameters sent, concatenate them into a string to create the table
    tablename = request.form.get("tablename")

    # Check for user injected malicious characters
    if injection_check(tablename):
        print(tablename)
        column_number = int(request.form.get("column_number"))    
        templist = []
        for i in range(column_number):
            column_name = request.form.get("column {}".format(i))

            # Returns error if first char from column name is a digit, sqlite does not allow it
            if column_name[0].isdigit():
                return render_template("error.html")
            datatype = request.form.get("{}".format(i))
            parameters_join = " ".join([column_name, datatype])
            templist.append(parameters_join)
        table_parameters = ", ".join(templist) 

        # Execute command to create table
        c.execute("CREATE TABLE {}({})".format(tablename, table_parameters))
        con.commit()  
        return render_template("created.html", tablename = tablename) 
    else:
        return render_template("error.html")

@app.route("/droptable", methods=["GET", "POST"])
def drop():
    if request.method == "GET":
        tablename = request.args.get('table')
        return render_template("drop.html", tablename = tablename)
    
    elif request.method == "POST":
        tablename = request.form.get("table")
        if injection_check(tablename):
            c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
            table = [row[0] for row in c]
            if tablename in table:
                print(tablename)
                c.execute("DROP TABLE {}".format(tablename))
                return render_template("dropped.html")
        else:
            return render_template("error.html")
