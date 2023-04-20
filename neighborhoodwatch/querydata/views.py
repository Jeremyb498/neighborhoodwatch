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

#initial query page provides users the opportunity to select from which states they would
#like to pull statistics from
def index(request):

    #initialize cursor to connect to database
    cursor = connection.cursor()

    #queries initial options to select states
    cursor.execute("SELECT distinct statename FROM agency")
    res = cursor.fetchall()

    #create a list to store column names from current query to post at top of table
    columnnames = []
    for item in cursor.description:
        columnnames.append(item[0])

    #creates a list to pass in state names for options list
    states = []
    for items in res:
        states.append(items[0])

    #queries second field to select distinct agency types
    cursor.execute("SELECT distinct agencytype FROM agency")
    temp = cursor.fetchall()

    #creates a list to store optional agency types
    agencytypes = []
    for items in temp:
        agencytypes.append(items[0])

    #Load the necessary HTML templated to render data on
    template = loader.get_template("querydata/index.html")

    #pass along contextual items to display data in the template
    context = {
        "query" : res,
        "columns" : columnnames,
        "states" : states,
        "agencytypes" : agencytypes
    }

    #respond
    return HttpResponse(template.render(context, request))

#Second webpage view offers users the opportunity to select their desired location within
#the states they had previously selected
def agencySelection(request):

        #initialize cursor to connect to database
        cursor = connection.cursor()

        #take in all of the form selection from the state selection page and format them for 
        #a valid SQL query
        selectedStates = request.POST.getlist('selection')
        selectAgencyType = request.POST.getlist('typeAgency')
        stateQuery = '\' OR statename = \''.join(selectedStates)
        typeQuery = '\' OR agencytype = \''.join(selectAgencyType)


        #initial query pulls the table results to display on the next page
        cursor.execute("SELECT distinct statename, agencyname, agencytype FROM agency WHERE (statename = \'" + stateQuery + "\') AND (agencytype = \'" + typeQuery + "\')")
        res = cursor.fetchall()

        #create a list to store column names from current query to post at top of table
        columnnames = []
        for item in cursor.description:
            columnnames.append(item[0])

        #creatse a list to store names of specific agencies
        agencynames = []
        for items in res:
            agencynames.append(items[1])

        #Load the necessary HTML templated to render data on
        template = loader.get_template("querydata/index.html")

        #pass along contextual items to display data in the template
        context = {
            "query" : res,
            "columns" : columnnames,
            "agencynames" : agencynames,
            "selectedStates" : selectedStates,
            "selectAgencyType" : selectAgencyType
        }

        #respond 
        return HttpResponse(template.render(context, request))

def parameterSelection(request):
    #initialize cursor to connect to database
    cursor = connection.cursor()

    selectedAgencies = request.POST.getlist('nameAgency')
    selectAgencyType = request.POST.getlist('agencyType')
    selectedStates = request.POST.getlist('state')
    selectedCrimeFamily = request.POST.getlist ('crimeFamily')
    selectedYears = request.POST.getlist('year')
    crimeFamilyQuery = ", ".join(selectedCrimeFamily)
    print(selectAgencyType)
    print(selectedStates)
    print(selectedAgencies)
    print(selectedCrimeFamily)
    print(selectedYears)
    dropunecessarycolumns = ""
    allCrimeTables = "assault, drugnarcotic, fraud, gambling, homicide, humantrafficking, otherproperty, othersociety, prostituition, sexoffense, theft"
    initialStatements = "SELECT distinct * FROM agency, "

    cursor.execute("SELECT distinct * FROM agency, ")
    res = cursor.fetchall()

    #create a list to store column names from current query to post at top of table
    columnnames = []
    for item in cursor.description:
        columnnames.append(item[0])

    template = loader.get_template("querydata/index.html")

    context = {
        "query" : res,
        "columns" : columnnames,
        "selectedAgencies" : selectedAgencies,
        "selectedStates" : selectedStates,
        "selectedCrimeFamily" : selectedCrimeFamily,
        "selectAgencyType" : selectAgencyType,
        "selectedYears" : selectedYears
    }

    #respond 
    return HttpResponse(template.render(context, request))



    





