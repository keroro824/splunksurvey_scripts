import csv
from contextlib import closing
from sqlite3 import connect

DATABASE = "surveyresults.db"
SQLSCRIPT = "scripts/surveyresults.sql"
QUESTIONS_CSV = "data/CSV/Questions.csv"
QUESTION_OPT_CSV = "data/CSV/QuestionOptions.csv"
RESPONDENTS_CSV = "data/CSV/Respondents.csv"
RESPONSES_TEXT_CSV = "data/CSV/ResponsesText.csv"
RESPONSES_CSV = "data/CSV/Responses.csv"
QUESTION_OPT_LABEL_CSV = "data/CSV/question_option_labels_for_graphing.csv"

def init(script):
    execute_db_script(script)

def execute_db_script(script):
    with closing(connect_db()) as db:
        with open(script) as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return connect(DATABASE)

def load(csvfile):
    db = connect_db()
    with open(csvfile, 'rU') as csvdata:
        csvreader = csv.reader(csvdata)
        first = True
        for row in csvreader:
            if first: # if there's a header -- a line with the column names in it -- skip it
                first = False
                continue
            insert_information(csvfile, db, *row) # assume row is a list containing three values, one for column1, one for column2, and one for column3
    db.close()

def insert_information(csvfile, db, *row):
    if csvfile == QUESTIONS_CSV:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Questions \
                    (QuestionID, PageID, Position, QType, Heading) \
                    VALUES (?,?,?,?,?)",
                    [row[0], row[1], row[2], row[3], row[4]])
        db.commit()

    if csvfile == QUESTION_OPT_CSV:
        cursor = db.cursor()
        cursor.execute("INSERT INTO QuestionOptions \
                    (OptionID, OptionType, OptionNum, QuestionID, OptionText) \
                    VALUES (?,?,?,?,?)",
                    [unicode(row[0], errors='ignore'), unicode(row[1], errors='ignore'), unicode(row[2], errors='ignore'), unicode(row[3], errors='ignore'), unicode(row[4], errors='ignore')])         
        db.commit()  

    if csvfile == RESPONSES_CSV:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Responses \
                    (RespondentID, CollectorID, QuestionID, Key1, Key2, Key3, DateAdded) \
                    VALUES (?,?,?,?,?,?,?)",
                    [row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
        db.commit()

    if csvfile == RESPONDENTS_CSV:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Respondents \
                    (RespondentID, CollectorID, IPAddress, Email, FirstName, LastName, CustomData, DateAdded) \
                    VALUES (?,?,?,?,?,?,?,?)",
                    [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
        db.commit() 

    if csvfile == RESPONSES_TEXT_CSV:
        cursor = db.cursor()
        cursor.execute("INSERT INTO ResponsesText \
                    (RespondentID, CollectorID, QuestionID, Key1, ResponsesText, DateAdded) \
                    VALUES (?,?,?,?,?,?)",
                    [row[0], row[1], row[2], row[3], row[4], row[5]])
        db.commit()

    if csvfile == QUESTION_OPT_LABEL_CSV:
        cursor = db.cursor()
        cursor.execute("INSERT INTO OptionLabel \
                    (OptionID, OptionLabel) \
                    VALUES (?,?)",
                    [row[0], row[1]])
        db.commit()

init(SQLSCRIPT)
load(QUESTIONS_CSV)
load(QUESTION_OPT_CSV)
load(RESPONDENTS_CSV)
load(RESPONSES_CSV)
load(RESPONSES_TEXT_CSV)
load(QUESTION_OPT_LABEL_CSV)

