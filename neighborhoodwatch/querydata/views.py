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

cursor = connection.cursor()

crimes = "crimes"

# Now query the rows back
cursor.execute("select * from " + crimes)
columnnames = []

for item in cursor.description:
    columnnames.append(item[0])

res = cursor.fetchall()

def index(request):
    query = res
    template = loader.get_template("querydata/index.html")
    context = {
        "query" : query,
        "columns" : columnnames
    }
    return HttpResponse(template.render(context, request))

