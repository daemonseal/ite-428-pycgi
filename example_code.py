#!/xampp/htdocs/mysql/py38/Scripts/python

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
    if (integer(form.getvalue("updid")) != 0):
        renderUpdateForm()
    else:
        renderProductForm()
    renderProductTable()
    print("</body>")


def renderFooter():
    print("<foot>")
    print("</foot>")


def renderJS():
    # Java Script confirm before update / delete
    print("""
        <script>
            function delProduct(el){
                pname = el.attributes["pname"].value
                if(!confirm("Do you really want to delete " + pname + " ?"))
                    return false
            }
            function updateProduct(el){
                pname = el.attributes["pname"].value
                if(!confirm("Do you want to update " + pname + " ?"))
                    return false
            }
        </script>
    """)


def renderCSS():
    print("""
        <style>
            #product-table{
                width: 800px;
            }
            #product-table th{
                background-color: #8A1F1F;
                color: #FFF;
            }
            #product-table tr:nth-child(odd) td{
                background-color: #FF08080;
            }
            #product-table tr:nth-child(even) td{
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

def renderProductForm():
    sql = """
        SELECT supplierid, companyname
        FROM suppliers
    """
    result = executeSQL(sql)
    print("""
        <form action="example_code.py" method="post">
            <table>
                <tr>
                    <td>Product Name</td>
                    <td><input type="text" name="pdn"></td>
                </tr>
                <tr>
                    <td>Supplier</td>
                    <td>
                        <select name="spe">
    """)
    for row in result[1]:
        print("""<option value="{0}">{1}</option>""".format(row[0], row[1]))
    print("""
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>Category</td>
                    <td>
                        <select name="ctg">
    """)
    sql = """
        SELECT categoryid, categoryname
        FROM categories
    """
    result = executeSQL(sql)
    for row in result[1]:
        print("""<option value="{0}">{1}</option>""".format(row[0], row[1]))
    print("""
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>Quantity Per Unit</td>
                    <td><input type="text" name="qpu"></td>
                </tr>
                <tr>
                    <td>Unit Price</td>
                    <td><input type="number" name="unp" value="0"></td>
                </tr>
                <tr>
                    <td>Stock</td>
                    <td><input type="number" name="stk" value="0"></td>
                </tr>
                <tr>
                    <td>On Order</td>
                    <td><input type="number" name="ood" value="0"></td>
                </tr>
                <tr>
                    <td>Re Order</td>
                    <td><input type="number" name="rod" value="0"></td>
                </tr>
                <tr>
                    <td>Discontinues</td>
                    <td><input type="checkbox" name="dct"></td>
                </tr>
                <tr>
                    <input type="hidden" name="status" value="create">
                    <td><input type="submit" value="SAVE PRODUCT"></input></td>
                </tr>
            </table>
        </form>
    """)


def renderUpdateForm():
    pid = integer(form.getvalue("updid"), 0)
    if (pid == 0):
        return
    sql = """
        SELECT productid,productname,supplierid,categoryid,quantityperunit,unitprice,unitsinstock,unitsonorder,reorderlevel,discontinued
        FROM products
        WHERE productid = {0}
    """.format(pid)
    result = executeSQL(sql)
    if (result[0] == 0):
        return
    product = result[1].fetchone()
    sql = """
        SELECT supplierid, companyname
        FROM suppliers
    """
    result = executeSQL(sql)
    print("""
        <h1>Update Products</h1>
        <form action="example_code.py" method="post">
            <table>
                <tr>
                    <td>Product Name</td>
                    <td><input type="text" name="pdn" value="{0}"></td>
                </tr>
                <tr>
                    <td>Supplier</td>
                    <td>
                        <select name="spe">
    """.format(product[1]))
    for row in result[1]:
        isDefault = ""
        if (row[0] == product[2]):
            isDefault = "selected"
        print("""<option value="{0}" {2}>{1}</option>""".format(row[0], row[1], isDefault))
    print("""
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>Category</td>
                    <td>
                        <select name="ctg">
    """)
    sql = """
        SELECT categoryid, categoryname
        FROM categories
    """
    result = executeSQL(sql)
    for row in result[1]:
        isDefault = ""
        if (row[0] == product[3]):
            isDefault = "selected"
        print("""<option value="{0}" {2}>{1}</option>""".format(row[0], row[1], isDefault))
    checked = ""
    if (product[9] == "1"):
        checked = "checked"
    print("""
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>Quantity Per Unit</td>
                    <td><input type="text" name="qpu" value="{0}"></td>
                </tr>
                <tr>
                    <td>Unit Price</td>
                    <td><input type="number" name="unp" value="{1}"></td>
                </tr>
                <tr>
                    <td>Stock</td>
                    <td><input type="number" name="stk" value="{2}"></td>
                </tr>
                <tr>
                    <td>On Order</td>
                    <td><input type="number" name="ood" value="{3}"></td>
                </tr>
                <tr>
                    <td>Re Order</td>
                    <td><input type="number" name="rod" value="{4}"></td>
                </tr>
                <tr>
                    <td>Discontinues</td>
                    <td><input type="checkbox" name="dct" {5}></td>
                <tr>
                    <td>
                        <input type="hidden" name="status" value="update">
                        <input type="hidden" name="updid" value="{6}">
                        <input type="submit" value="SAVE PRODUCT">
                    </td>
                </tr>
            </table>
        </form>
    """.format(product[4], product[5], product[6], product[7], product[8], checked, pid))


# HTML Output render
def renderProductTable():
    sql = """
        SELECT p.productid,p.productname,c.categoryname,s.companyname,p.unitprice
        FROM products p LEFT JOIN categories c USING(categoryid) LEFT JOIN suppliers s USING(supplierid)
    """
    result = executeSQL(sql)
    print("Result: {0} record(s)".format(result[0]))
    if (result[0] > 0):
        print("""
            <table id="product-table" cellspacing="0" cellpadding="0">
                <tr>
                    <th width="10%">No.</th>
                    <th>Product</th>
                    <th>Category</th>
                    <th>Supplier</th>
                    <th>Price</th>
                    <th></th>
                    <th></th>
                </tr>
        """)
        for i, row in enumerate(result[1]):
            print("""
                <tr>
                    <td align="center">{0}</td>
                    <td>{1}</td>
                    <td>{2}</td>
                    <td>{3}</td>
                    <td align="right">{4:.2f}</td>
                    <td><a href="example_code.py?delid={5}" onclick="return delProduct(this)" pname="{1}"><img src="images/Delete.jpg" width="20px"></a></td>
                    <td><a href="example_code.py?updid={5}"><img src="images/Update.jpg" width="20px"></a></td>
                </tr>
            """.format(i + 1, row[1], row[2], row[3], row[4], row[0]))
        print("</table>")


# CUD Product
def insertProduct():
    saved = False
    if (string(form.getvalue("status")) != "create"):
        return saved
    reqData = {"pdn", "spe", "ctg", "qpu", "unp", "stk", "ood", "rod"}
    if (not reqData.issubset(form.keys())):
        return saved
    pdn = string(form.getvalue("pdn"))
    spe = integer(form.getvalue("spe"), "NULL")
    ctg = integer(form.getvalue("ctg"), "NULL")
    qpu = string(form.getvalue("qpu"), "NULL")
    unp = parseFloat(form.getvalue("unp"), 0)
    stk = integer(form.getvalue("stk"), 0)
    ood = integer(form.getvalue("ood"), 0)
    rod = integer(form.getvalue("rod"), 0)
    dct = string(form.getvalue("dct"), "off")
    if (dct == "on"):
        dct = 1
    else:
        dct = 0
    sql = """
        INSERT INTO products (productname,supplierid,categoryid,quantityperunit,unitprice,unitsinstock,unitsonorder,reorderlevel,discontinued) 
        VALUES ("{0}",{1},{2},"{3}",{4},{5},{6},{7},{8})
    """.format(pdn, spe, ctg, qpu, unp, stk, ood, rod, dct)
    result = executeInsertSQL(sql)
    if (result[0] == 1):
        saved = True
        actionLog("I", result[1])
    return saved


def updateProduct():
    saved = False
    if (string(form.getvalue("status")) != "update"):
        return saved
    reqData = {"updid", "pdn", "spe", "ctg", "qpu", "unp", "stk", "ood", "rod"}
    if (not reqData.issubset(form.keys())):
        return saved
    pid = integer(form.getvalue("updid"))
    if (pid == 0):
        return saved
    pdn = string(form.getvalue("pdn"))
    spe = integer(form.getvalue("spe"), "NULL")
    ctg = integer(form.getvalue("ctg"), "NULL")
    qpu = string(form.getvalue("qpu"), "NULL")
    unp = parseFloat(form.getvalue("unp"), 0)
    stk = integer(form.getvalue("stk"), 0)
    ood = integer(form.getvalue("ood"), 0)
    rod = integer(form.getvalue("rod"), 0)
    dct = string(form.getvalue("dct"), "off")
    if (dct == "on"):
        dct = 1
    else:
        dct = 0
    sql = """
        UPDATE products 
        SET productname = "{0}",supplierid={1},categoryid={2},quantityperunit="{3}",unitprice={4},unitsinstock={5},unitsonorder={6},reorderlevel={7},discontinued={8} 
        WHERE productid = {9}
    """.format(pdn, spe, ctg, qpu, unp, stk, ood, rod, dct, pid)
    result = executeNonQuerySQL(sql)
    if (result == 1):
        saved = True
        actionLog("U", pid)
    return saved


def deleteProduct():
    deleted = False
    delid = integer(form.getvalue("delid"))
    if (delid != 0):
        sql = """
            DELETE FROM products
            WHERE productid = {0}
        """.format(form.getvalue("delid"))
        result = executeNonQuerySQL(sql)
        if (result == 1):
            deleted = True
            actionLog("D", delid)
    return deleted


# Database
def connectDB():
    global conn
    if (conn is None):
        conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db=DatabaseName)
    return conn


def closeDBConnect():
    if (conn != None):
        conn.close()


def executeSQL(sql):
    conn = connectDB()
    cur = conn.cursor()
    count = cur.execute(sql)
    cur.close()
    return (count, cur)


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
    return (count, insertedID)


# Logging
def actionLog(action, target):
    existAction = {"I", "U", "D"}
    if (action not in existAction):
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


# Main
if __name__ == "__main__":
    print("Content-type:text/html\n")
    try:
        insertProduct()
        updateProduct()
        deleteProduct()
        renderHTML()
    except Exception as e:
        errorLog(e)
        if (debugging):
            renderError(e)
        else:
            renderError("Contact admin for more detail.")
    closeDBConnect()
