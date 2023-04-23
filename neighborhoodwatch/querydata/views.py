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
        selectedYears = request.POST.getlist('year')
        stateQuery = '\' OR statename = \''.join(selectedStates)
        typeQuery = '\' OR agencytype = \''.join(selectAgencyType)
        yearQuery = '\' OR year = \''.join(selectedYears)

        #initial query pulls the table results to display on the next page
        #checks if a previous query view exists in the data base if so removes it
        cursor.execute("SELECT view_name FROM user_views")
        checkViews = cursor.fetchall()
        for columns in checkViews:
            for views in columns:
                if views == 'AVAILABLEAGENCIES':
                    cursor.execute("DROP VIEW availableagencies")
                if views == 'AGENCIESID':
                    cursor.execute("DROP VIEW agenciesid")
          
        #adds the query view for the current session and displays all items available
        #creates separate view with respective agencyid for later querying
        cursor.execute("CREATE VIEW agenciesid AS SELECT distinct agencyid, statename, agencyname, year FROM agency WHERE (statename = \'" + stateQuery + "\') AND (agencytype = \'" + typeQuery + "\') AND (year = \'" + yearQuery + "\')") 
        cursor.execute("CREATE VIEW availableagencies AS SELECT distinct statename, agencyname, agencytype FROM agency WHERE (statename = \'" + stateQuery + "\') AND (agencytype = \'" + typeQuery + "\')")
        cursor.execute("SELECT * FROM availableagencies")
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
            "selectAgencyType" : selectAgencyType,
            "selectedYears" : selectedYears
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

    crimeFamilyQuery = ""
    #builds a query to union all selected parent tables for their repsective crime family
    #and extracts their unique crimeID
    for family in selectedCrimeFamily:
        if family == selectedCrimeFamily[len(selectedCrimeFamily) - 1]:
            crimeFamilyQuery = crimeFamilyQuery + " SELECT distinct CRIMEID FROM " + family
        else:
            crimeFamilyQuery = crimeFamilyQuery + " SELECT distinct CRIMEID FROM " + family + " UNION"

    #checks if the updated family ID view is in the session yet
    #if so removes it and recreates it with the necessary values
    cursor.execute("SELECT view_name FROM user_views")
    checkViews = cursor.fetchall()
    for columns in checkViews:
        for views in columns:
            if views == 'FAMILYIDS':
                cursor.execute("DROP VIEW familyids")

    #create view with desired crime family ID values
    cursor.execute("CREATE VIEW familyids AS" + crimeFamilyQuery)
    cursor.execute("SELECT * FROM familyids")
    familyIDS = cursor.fetchall()
    
    #prepares necessary string to join necessary 
    allCrimeTables = ["assault", "drugnarcotic", "fraud", "gambling", "homicide", "humantrafficking", "otherproperty", "othersociety", "prostitution", "sexoffense", "theft"]
    updatedCrimeTable = []

    #iterate over each table with name from allCrimeTables and find if they share a respective crimeID 
    #with users selection if so add them to the updated list
    for crimeTypes in allCrimeTables:
        cursor.execute("SELECT distinct CRIMEID FROM " + crimeTypes)
        checkID = cursor.fetchall()
        for columns in checkID:
            for cID in columns:
                for col in familyIDS:
                    for fID in col:
                        if cID == fID:
                            updatedCrimeTable.append(crimeTypes)

    #checks to see if previously updated views are in the database
    cursor.execute("SELECT view_name FROM user_views")
    checkViews = cursor.fetchall()
    for crimes in allCrimeTables:
        crimeToCheck = "updated" + crimes
        for columns in checkViews:
            for views in columns:
                if crimeToCheck.upper() == views:
                    cursor.execute("DROP VIEW " + crimeToCheck)

    updatedViewTables = []

    #creates new views for each crime table that matches selected
    # crimeID without the crimeID column
    for crimes in updatedCrimeTable:
        newViewName = "updated" + crimes
        newView = "CREATE VIEW " + newViewName + " AS SELECT "
        cursor.execute("SELECT * FROM " + crimes)
        for col in cursor.description:
            if col[0] == 'CRIMEID':
                continue
            else:
                if col[0] == cursor.description[len(cursor.description) - 1][0]:
                    newView = newView + col[0]
                else:
                    newView = newView + col[0] + ", "
        newView = newView + " FROM " + crimes
        updatedViewTables.append(newViewName)
        cursor.execute(newView)
    
    #builds query to compile the final table view that comprises of all items joined together
    combinedView = ""
    for views in updatedViewTables:
        if views == updatedViewTables[0]:
            combinedView = views + " LEFT JOIN "
        elif views == updatedViewTables[len(updatedViewTables) - 1]:
            combinedView = combinedView + views + " using (CRIMESID)"
        else:
            combinedView = combinedView + views + " using (CRIMESID) LEFT JOIN "

    #Checks to see if the final crime table view exists from a previous iteration
    #or if final agencies view exists
    cursor.execute("SELECT view_name FROM user_views")
    checkViews = cursor.fetchall()
    for columns in checkViews:
        for views in columns:
            if views == 'FINALCRIMETABLE':
                cursor.execute("DROP VIEW FINALCRIMETABLE")
            if views == 'FINALAGENCIES':
                cursor.execute("DROP VIEW FINALAGENCIES")

    agencies = "\' OR agenciesid.agencyname = \'".join(selectedAgencies)
    #final agencies table
    print("CREATE VIEW finalagencies AS SELECT * FROM agenciesid WHERE agenciesid.agencyname = \'" + agencies + "\'")
    cursor.execute("CREATE VIEW finalagencies AS SELECT * FROM agenciesid WHERE agenciesid.agencyname = \'" + agencies + "\'")
    cursor.execute("CREATE VIEW finalcrimetable AS SELECT distinct * FROM " + combinedView)


    cursor.execute("SELECT * FROM finalagencies INNER JOIN finalcrimetable ON finalagencies.agencyid = finalcrimetable.crimesid")
    res = cursor.fetchall()
    
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



    





