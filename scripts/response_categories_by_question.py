
import sqlite3
from collections import defaultdict


def main():
    con = sqlite3.connect('surveyresults.db')
    con.text_factory = str
    cur = con.cursor()

    cur.execute("SELECT QuestionID FROM Questions WHERE QType = 40;") # TODO: Other question types?
    question_ids = [r[0] for r in cur.fetchall()]
    
    questions = {}
    for id in question_ids:

        # For each question, get count of responses and response labels.
        cur.execute("SELECT RespondentID, ColumnLabel, RowLabel \
                        FROM \
                    ( SELECT OptionID as K3, OptionLabel as ColumnLabel \
                        FROM QuestionOptions ), \
                    ( SELECT OptionID as K1, OptionLabel as RowLabel \
                        FROM QuestionOptions ), \
                    Responses \
                WHERE Responses.QuestionID=? \
                    AND Responses.Key3=K3 \
                    AND Responses.Key1=K1", [id])

        respondents = {}
        responses = cur.fetchall()
        for (respondent, column_label, row_label) in responses:
            if not respondent in respondents:
                respondents[respondent] = defaultdict(list)
            respondents[respondent][column_label].append(row_label)
    
        questions[id] = respondents

    for (id, all_answers) in questions.iteritems():
        for (respondent, customers) in all_answers.iteritems():
            for (customer, answers) in customers.iteritems():
                print id, respondent, customer, answers

if __name__ == "__main__":
    main()
