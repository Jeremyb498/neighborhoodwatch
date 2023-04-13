#### WELCOME TO NEIGHBORHOOD WATCH - A CRIME DATABASE APPLICATION ####

#### 1. PREREQUISITES ####

You're going to need a couple of prerequisites before you get started working on the app.
1) Download the latest version of Python - https://www.python.org/downloads/
2) Install pip - Most python environments will come preinstalled with pip but if yours is not you can run the following commands in your CLI
        - python -m ensurepip --upgrade
        - python get-pip.py
3) Install Django - After you've installed pip it should be easy to have django installed. Just run the following command
        - python -m pip install Django
4) Finally install the oracledb python module to access the CISE database - https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html

#### 2. GETTING STARTED ####

If you're unfamiliar with Django I definitely recommend going through the tutorial real quick for any answers you might need. If you follow it step by step 
you'll get the necessary essentials within an hour or two. 

******IMPORTANT NOTE*******
The tutorial will cover using a database native with Django. However for the implementation for this project since i am working on apple silicon which runs
on ARM I cannot use the necessary cx_oracle module or the oracle instant client since they run on x86. But do not fret if you're in the same boat or thinking about manually integrating a database stresses you out its not too difficult.
**************************


