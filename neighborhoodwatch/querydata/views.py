from django.http import HttpResponse
from django.template import loader
import getpass
import oracledb

pw = getpass.getpass("Enter password: ")

connection = oracledb.connect(
    user="esteban.medero",
    password=pw,
    dsn="oracle.cise.ufl.edu:1521/orcl")

print("Successfully connected to Oracle Database")

def index(request):
    cursor = connection.cursor()

    # Now query the rows back
    cursor.execute("SELECT table_name FROM user_tables")
    columnnames = []

    for item in cursor.description:
        columnnames.append(item[0])

    res = cursor.fetchall()
    query = res
    template = loader.get_template("querydata/index.html")
    context = {
        "query" : query,
        "columns" : columnnames
    }
    return HttpResponse(template.render(context, request))

def tableSelection(request):

    cursor = connection.cursor()
    columnnames = []

    selectedTables = request.POST.getlist('selection')
    queries = ', '.join(selectedTables)

    cursor.execute("select * from " + queries + " where agency.statename = 'COLORADO'")

    for item in cursor.description:
        columnnames.append(item[0])

    res = cursor.fetchall()
    query = res
    template = loader.get_template("querydata/index.html")
    context = {
        "query" : query,
        "columns" : columnnames
    }
    return HttpResponse(template.render(context, request))




