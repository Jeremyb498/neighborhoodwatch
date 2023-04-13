from django.http import HttpResponse
import getpass
import oracledb

pw = getpass.getpass("Enter password: ")

connection = oracledb.connect(
    user="esteban.medero",
    password=pw,
    dsn="oracle.cise.ufl.edu:1521/orcl")

print("Successfully connected to Oracle Database")

cursor = connection.cursor()

crimes = "Crimes"

# Now query the rows back
cursor.execute("select * from " + crimes)
res = cursor.fetchall()
page = ""
for row in res:
    for item in row:
        page = page + str(item) + ", "
    page += "\n"

def index(request):
    return HttpResponse(page)
