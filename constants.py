#############################
###  CONSTANT PARAMETERS  ###
### To set here like in a ###
###     config file       ###      
#############################

# Scope is the general url of Google Spreadsheet
SCOPE = "https://spreadsheets.google.com/feeds"

# KEY is the name of the json file that you created to have access to the Google API 
# See: https://socraticowl.com/post/integrate-google-sheets-and-jupyter-notebooks/
KEY = "Jupyter_meets_GSheet-a279ad757691.json"

# This is the ID of your google spreadsheet, it is contained in its URL, in our case, see:
# https://docs.google.com/spreadsheets/d/WHAT IS HERE/edit#gid=0
SPREADSHEET_ID = "1ANV9TXjL75vUaxxuBCvMqYgc7fgg3uruUy_BdKKyr30"

# The name of the tab you want to export. 
WORKSHEET = "Full_DB"

# Add all names as key and a list of the questions they contain as list 
SECTIONS_DICT = {
                 "1" : [1, 2, 3, 4, 5], 
                 "2" : [1, 2, 3, 4, 5, 6, 7, 8, 9],
                 "3" : [1, 2, 3, 4, 5, 6, 7, 8, 9],
                 "4" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                 "5" : [1, 2, 3, 4, 5, 6],
                 "6" : [1, 2, 3, 4, 5, 6],
                 "7" : [1, 2, 3, 4],
                 "8" : [1, 2, 3, 4, 5],
                 "9" : [1, 2, 3, 4, 5, 6, 7, 8],
                 "10": [1, 2, 3, 4]
                }
# List of all question numbers
QUESTIONS_LS = list(SECTIONS_DICT.values())

# List of all sections numbers 
SECTIONS_LS = list(SECTIONS_DICT.keys())

# Dictonary that maps the names of the columns we'll use for the data transformation and their shortened names in Italian 
# which we will use for the visulation in the spidercharts. 
SECTIONS_SHORT_NAMES = {"Section_1":"Dichiarazioni \nPubbliche", 
                 "Section_2":"Modello \nAnticorruzione", 
                 "Section_3":"Codice",
                 "Section_4":"Whistleblowing", 
                 "Section_5":"Lobbying", 
                 "Section_6":"Conflitto \nd'Interesse",
                 "Section_7":"Finanziamenti \nPolitici",
                 "Section_8":"Traspareza \nOrganizzativa",
                 "Section_9":"Formazione", 
                 "Section_10":"Sostenibilità"}


# List that contains the long form of the names of the sections we will use in the company profles .docx as headings.  
SECTIONS_LONG_NAMES = ["Dichiarazioni e posizioni pubbliche", "Modello 231 o piano anti corruzione", "Codice etico o di condotta", "Politica di whistleblowing e sistema di segnalazione", "Lobbying","Conflitto d'interesse", "Finanziamento alla politica (Partiti, candidati, e fondazioni politiche)", "Trasparenza organizzativa e attività estere", "Formazione anti corruzione", "Progetti di sostenibilità"]

# List of sections maximum scores possible (used in utils.py to calculate the average per section).
MAX_RESULTS_LS = [10, 17, 18, 20, 12, 12, 10, 10, 16, 8]


# Create dictionary to associate bands to score ranges. 
BANDS_DICT = {0 : "non soddisfacente", 0.25 : "poco soddisfacente", 0.50 : "soddisfacente", 0.75 : "eccellente", 1.0 : "WhatevsThisWilNeverBeUsed"}

# Parameters for the folder structure. We create the root folder and then a list of our subfolders. 
ROOT = "deliverables"
SUB_FOLDERS_LS = ["data", "company_profiles"] 

INTRO_FOR_ANALYSIS_DOCX = """Nel seguente documento si presenterà un'analisi dettagliata del piano anti corruzione di {}, secondo la metologia di Transparency International Italia. L'azienda ha ottenuto un indice TRAC {} (pari a {:.1%}). Per effettuare la seguente analisi si sono principalmente usate le seguenti fonti (ove reperibili): Sito Ufficiale, Codice di Condotta, Modello di Gestione e Controllo, Programma di Compliance e i vari Bilanci Annuali e/o di Sosteibilità. Nei casi in cui l'azienda in studio fosse detenuta con partecipazione di controllo da una holding estera, si è spesso fatto riferimento ai documenti della holding estera."""
