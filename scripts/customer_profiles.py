
import sys
import sqlite3
from collections import defaultdict

def print_customers(customers, question_headings):
    num = 1
    for (name, question) in customers.iteritems():
        name = name.replace(" ", "")
        print r"""
\begin{table}[H]
\begin{footnotesize}
\begin{center}
\begin{tabular}{|p{.6\textwidth}|p{.4\textwidth}|} \hline
\textit{Question} & \textit{Answer} \\ \hline
            """
        for (id, answers) in question.iteritems():
            sys.stdout.write("%s & %s \\\\ \\hline \n" % (question_headings[id], "; ".join(answers)))
            #print question_headings[id]
            #print answers
        print r"""
\end{tabular}
\end{center}
\label{tab:%s}
\caption{Customer %d}
\end{footnotesize}
\end{table}
            """ % (name, num)
        print
        num += 1

def main():
    con = sqlite3.connect('surveyresults.db')
    con.text_factory = str
    cur = con.cursor()

    cur.execute("SELECT QuestionID FROM Questions WHERE QType = 40;") # TODO: Other question types?
    question_ids = [r[0] for r in cur.fetchall()]
    
    cur.execute("SELECT QuestionID, Heading from Questions")
    question_headings = dict(cur.fetchall())

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

    cur.execute("SELECT RespondentID, ResponsesText.QuestionID, Key1, ResponsesText \
                    FROM ResponsesText, Questions \
                    WHERE ResponsesText.QuestionID=Questions.QuestionID \
                        AND (Questions.QType=100 OR Questions.QType=80)")

    q = {}
    rows = cur.fetchall()
    for (respondent, question, key, text) in rows:
        if not question in q:
            q[question] = {}
        if not respondent in q[question]:
            q[question][respondent] = []
        q[question][respondent].append((key, text))

    for (id, question) in q.iteritems():
        if not id in questions:
            questions[id] = {}
        for (respondent, answers) in question.iteritems():
            answers = sorted(answers, key=lambda x: x[0])
            num = 1
            for (key, text) in answers:
                if not respondent in questions[id]:
                    questions[id][respondent] = {}
                questions[id][respondent]["Customer "+str(num)] = [text]
                num += 1

    print questions[528408871]

    customers = {}
    for (id, all_answers) in questions.iteritems():
        for (respondent, three_customers) in all_answers.iteritems():
            for (customer, answers) in three_customers.iteritems():
                cur.execute("SELECT ResponsesText FROM ResponsesText \
                    WHERE Key1=0 AND QuestionID=? AND RespondentID=?", [id, respondent])
                addl_info = cur.fetchall()
                name = '-'.join([str(respondent), customer])
                if not name in customers:
                    customers[name] = {}
                if len(addl_info) > 0:
                    answers = answers + [a[0] for a in addl_info]
                customers[name][id] = answers

    print_customers(customers, question_headings)

if __name__ == "__main__":
    main()
