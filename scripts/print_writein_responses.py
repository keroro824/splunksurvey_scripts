
import sys
import sqlite3
from collections import defaultdict

def main():
    con = sqlite3.connect('surveyresults.db')
    con.text_factory = str
    cur = con.cursor()
    
    cur.execute("SELECT RespondentID, ResponsesText.QuestionID, Key1, ResponsesText \
                    FROM ResponsesText, Questions \
                    WHERE ResponsesText.QuestionID=Questions.QuestionID \
                        AND (Questions.QType=40)")

    rows = cur.fetchall()
    questions = defaultdict(list)
    for (respondent, question, key, text) in rows:
        questions[question].append(text)
    

    for (question, text_list) in questions.iteritems():
        print question
        print r"\squishitem"
        print "\n".join(["\item " + s for s in text_list])
        print r"\squishend"

if __name__ == "__main__":
    main()
