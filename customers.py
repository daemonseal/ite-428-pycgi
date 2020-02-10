#!\xampp\htdocs\ite-428-pycgi\venv\Scripts\python

import pymysql
import cgi
import csv
from datetime import datetime

# Static Variable
form = cgi.FieldStorage()
conn = None
debugging = True
DatabaseName = "northwind"


# HTML Render
def renderHTML():
    renderHeader()
    renderBody()
    renderFooter()


def renderHeader():
    print("<head>")
    renderCSS()
    renderJS()
    print("</head>")


def renderBody():
    print("<body>")
    if string(form.getvalue("updid"), "NULL") != "NULL":
        renderUpdateForm()
    else:
        renderCustomerForm()
    renderCustomerTable()
    print("</body>")


def renderFooter():
    print("<foot>")
    print("</foot>")


def renderJS():
    # Java Script confirm before update / delete
    print("""
        <script>
            function delCustomer(el){
                company_name = el.attributes["company_name"].value
                if(!confirm("do you really want to delete " + company_name + " ?"))
                    return false
            }
            function updateCustomer(el){
                company_name = el.attributes["company_name"].value
                if(!confirm("do you want to update " + company_name + " ?"))
                    return false
            }
        </script>
    """)


def renderCSS():
    print("""
        <style>
            #customer-table{
                width: 1000px;
            }
            #customer-table th{
                background-color: #8A1F1F;
                color: #FFF;
            }
            #customer-table tr:nth-child(odd) td{
                background-color: #FF08080;
            }
            #customer-table tr:nth-child(even) td{
                background-color: #FCA6A6;
            }
        </style>
    """)


# Error HTML Render
def renderError(e):
    print("<title>ERROR</title>")
    print("<h1>Server Error</h1>")
    print("<p>{0}</p>".format(e))


# HTML Form Render
def renderCustomerForm():
    print("""
        <form action="customers.py" method="post">
            <table>
                <tr>
                    <td>Customer ID</td>
                    <td><input type="text" name="customer_id"></td>
                </tr>
                <tr>
                    <td>Company Name</td>
                    <td><input type="text" name="company_name"></td>
                </tr>
                <tr>
                    <td>Contact Name</td>
                    <td><input type="test" name="contact_name"></td>
                </tr>
                <tr>
                    <td>Address</td>
                    <td><input type="text" name="address"></td>
                </tr>
                <tr>
                    <td>City</td>
                    <td><input type="text" name="city"></td>
                </tr>
                <tr>
                    <td>Region</td>
                    <td><input type="text" name="region"></td>
                </tr>
                <tr>
                    <td>Postal Code</td>
                    <td><input type="text" name="postal_code"></td>
                </tr>
    """)
    print("""
                <tr>
                    <td>Country</td>
                    <td>
                        <select name="country">
    """)
    for row in readCountryData():
        print("""<option value="{0}">{0}</option>""".format(row))
    print("""
                        </select>
                    </td>
                </tr> 
    """)
    print("""
                <tr>
                    <td>Phone</td>
                    <td><input type="tel" name="phone"></td>
                </tr>
                <tr>
                    <td>Fax</td>
                    <td><input type="tel" name="fax"></td>
                </tr>
                <tr>
                    <input type="hidden" name="status" value="create">
                    <td><input type="submit" value="SAVE PRODUCT"></input></td>
                </tr>
            </table>
        </form>
    """)


def renderUpdateForm():
    customer_id = string(form.getvalue("updid"), "NULL")
    if customer_id == "NULL":
        return
    sql = """
        SELECT CustomerID, CompanyName, ContactName, ContactTitle,
        Address, City, Region, PostalCode, Country, Phone, Fax 
        FROM customers 
        WHERE CustomerID = "{0}"
    """.format(customer_id)
    result = executeSQL(sql)
    if result[0] == 0:
        return

    result = executeSQL(sql)[1]

    print(f"""
        <form action="customers.py" method="post">
            <table>
                <tr>
                    <td>Customer ID</td>
                    <td><input type="text" name="customer_id">{result['CustomerID']}</td>
                </tr>
                <tr>
                    <td>Company Name</td>
                    <td><input type="text" name="company_name">{result['CompanyName']}</td>
                </tr>
                <tr>
                    <td>Contact Name</td>
                    <td><input type="test" name="contact_name">{result['ContactName']}</td>
                </tr>
                <tr>
                    <td>Contact Name</td>
                    <td><input type="test" name="contact_title">{result['ContactTitle']}</td>
                </tr>
                <tr>
                    <td>Address</td>
                    <td><input type="text" name="address">{result['ContactTitle']}</td>
                </tr>
                <tr>
                    <td>City</td>
                    <td><input type="text" name="city">{result['Address']}</td>
                </tr>
                <tr>
                    <td>Region</td>
                    <td><input type="text" name="region">{result['City']}</td>
                </tr>
                <tr>
                    <td>Postal Code</td>
                    <td><input type="text" name="postal_code">{result['Region']}</td>
                </tr>
    """)
    print(f"""
                <tr>
                    <td>Country</td>
                    <td>
                        <select name="country" value="{result['Country']}">
    """)
    for row in readCountryData():
        print("""<option value="{0}">{0}</option>""".format(row))
    print("""
                        </select>
                    </td>
                </tr> 
    """)
    print(f"""
                <tr>
                    <td>Phone</td>
                    <td><input type="tel" name="phone">{result['Phone']}</td>
                </tr>
                <tr>
                    <td>Fax</td>
                    <td><input type="tel" name="fax">{result['Fax']}</td>
                </tr>
                <tr>
                     <td>
                        <input type="hidden" name="status" value="update">
                        <input type="hidden" name="updid" value="{result['CustomerID']}">
                        <input type="submit" value="SAVE PRODUCT">
                    </td>
                </tr>
            </table>
        </form>
    """)


# HTML Output render
def renderCustomerTable():
    sql = """
        SELECT CustomerID, CompanyName, ContactName, ContactTitle,
        Address, City, Region, PostalCode, Country, Phone, Fax 
        FROM customers
    """
    result = executeSQL(sql)
    print("Result: {0} record(s)".format(result[0]))
    if result[0] > 0:
        print("""
            <table id="customer-table" cellspacing="0" cellpadding="5">
                <tr>
                    <th width="10%">CustomersID</th>
                    <th>CompanyName</th>
                    <th>ContactName</th>
                    <th>ContactTitle</th>
                    <th>Address</th>
                    <th>City</th>
                    <th>Region</th>
                    <th>PostalCode</th>
                    <th>Country</th>
                    <th>Phone</th>
                    <th>Fax</th>
                    <th>Delete</th>
                    <th>Update</th>
                </tr>
        """)
        for i, row in enumerate(result[1]):
            print(f"""
                <tr>
                    <td>{row['CustomerID']}</td>
                    <td>{row['CompanyName']}</td>
                    <td>{row['ContactName']}</td>
                    <td>{row['ContactTitle']}</td>
                    <td>{row['Address']}</td>
                    <td>{row['City']}</td>
                    <td>{row['Region']}</td>
                    <td>{row['PostalCode']}</td>
                    <td>{row['Country']}</td>
                    <td>{row['Phone']}</td>
                    <td>{row['Fax']}</td>
                    <td><a href="customers.py?delid={row['CustomerID']}" onclick="return delCustomers(this)" company_name="{row['CompanyName']}">
                    <img src="images/Delete.jpg" width="20px"></a></td>
                    <td><a href="customers.py?updid={row['CustomerID']}"><img src="images/Update.jpg" width="20px"></a></td>
                </tr>
            """)
        print("</table>")


# CUD Customers
def insertCustomers():
    saved = False
    if string(form.getvalue("status")) != "create":
        return saved
    reqData = {"customer_id", "company_name", "contact_name", "contact_title",
               "address", "city", "region", "postal_code", "country", "phone", "fax"}
    if not reqData.issubset(form.keys()):
        return saved
    customer_id = string(form.getvalue("customer_id"))  # 0
    company_name = string(form.getvalue("company_name"), "NULL")  # 1
    contact_name = string(form.getvalue("contact_name"), "NULL")  # 2
    contact_title = string(form.getvalue("contact_title"), "NULL")  # 3
    address = string(form.getvalue("address"), "NULL")  # 4
    city = string(form.getvalue("city"), "NULL")  # 5
    region = string(form.getvalue("region"), "NULL")  # 6
    postal_code = string(form.getvalue("postal_code"), "NULL")  # 7
    country = string(form.getvalue("country"), "NULL")  # 8
    phone = string(form.getvalue("phone"))  # 9
    fax = string(form.getvalue("fax"))  # 10
    sql = """
        INSERT INTO customers (CustomerID, CompanyName, ContactName,
        ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax) 
        VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}");
    """.format(customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country,
               phone, fax)
    result = executeInsertSQL(sql)
    if result[0] == 1:
        saved = True
        actionLog("I", result[1])
    return saved


def updateCustomers():
    saved = False
    if string(form.getvalue("status")) != "update":
        return saved
    reqData = {"customer_id", "company_name", "contact_name", "contact_title",
               "address", "city", "region", "postal_code", "country", "phone", "fax"}
    if not reqData.issubset(form.keys()):
        return saved
    customer_id = string(form.getvalue("updid"), "NULL")
    if customer_id == "NULL":
        return saved
    company_name = string(form.getvalue("company_name"), "NULL")  # 1
    contact_name = string(form.getvalue("contact_name"), "NULL")  # 2
    contact_title = string(form.getvalue("contact_title"), "NULL")  # 3
    address = string(form.getvalue("address"), "NULL")  # 4
    city = string(form.getvalue("city"), "NULL")  # 5
    region = string(form.getvalue("region"), "NULL")  # 6
    postal_code = string(form.getvalue("postal_code"), "NULL")  # 7
    country = string(form.getvalue("country"), "NULL")  # 8
    phone = string(form.getvalue("phone"))  # 9
    fax = string(form.getvalue("fax"))  # 10
    sql = """
        UPDATE customers 
        SET CustomerID="{0}", CompanyName={1}, ContactName={2}, 
        ContactTitle="{3}", Address={4}, City={5}, Region={6}, PostalCode={7}, Country={8}, Phone={9}, Fax={10} 
        WHERE CustomerID = "{0}"
    """.format(customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country,
               phone, fax)
    result = executeNonQuerySQL(sql)
    if result == 1:
        saved = True
        actionLog("U", customer_id)
    return saved


def deleteCustomers():
    deleted = False
    delid = string(form.getvalue("delid"))
    if delid != 0:
        sql = """
            DELETE FROM customers
            WHERE CustomerID = "{0}"
        """.format(form.getvalue("delid"))
        result = executeNonQuerySQL(sql)
        if result == 1:
            deleted = True
            actionLog("D", delid)
    return deleted


# Database
def connectDB():
    global conn
    if conn is None:
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="",
            cursorclass=pymysql.cursors.DictCursor,
            db=DatabaseName
        )
    return conn


def closeDBConnect():
    if conn is not None:
        conn.close()


def executeSQL(sql):
    conn = connectDB()
    cur = conn.cursor()
    count = cur.execute(sql)
    cur.close()
    return count, cur


def executeNonQuerySQL(sql):
    conn = connectDB()
    cur = conn.cursor()
    count = cur.execute(sql)
    conn.commit()
    cur.close()
    return count


def executeInsertSQL(sql):
    conn = connectDB()
    cur = conn.cursor()
    count = cur.execute(sql)
    sqlGetInsertedID = """
        SELECT LAST_INSERT_ID()
    """
    cur.execute(sqlGetInsertedID)
    insertedID = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return count, insertedID


# Logging
def actionLog(action, target):
    existAction = {"I", "U", "D"}
    if action not in existAction:
        return
    time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    row = [action, time, target]
    with open("./LogData/data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)


def errorLog(error):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [time, error]
    try:
        with open("./LogData/error.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)
    except Exception:
        print("Fatal Error: cannot log error.")


# Miscellaneous
def string(s, default=""):
    try:
        return str(s)
    except Exception:
        return default


def integer(i, default=0):
    try:
        return int(i)
    except TypeError:
        return default
    except ValueError:
        return default


def parseFloat(f, default=0):
    try:
        return float(f)
    except TypeError:
        return default
    except ValueError:
        return default


def readCountryData():
    with open("Country/customers.csv") as f:
        return f.readlines()


# Main
if __name__ == "__main__":
    print("Content-type:text/html\n")
    try:
        insertCustomers()
        updateCustomers()
        deleteCustomers()
        renderHTML()
    except Exception as e:
        errorLog(e)
        if debugging:
            renderError(e)
        else:
            renderError("Contact admin for more detail.")
    closeDBConnect()
