
import copy
import math
import os
import sqlite3
import textwrap

import numpy as np
import matplotlib.pyplot as plt


from matplotlib import pyplot as mpl
from numpy import argsort, linspace

def plot_vertical_bar(id, response_count, response_label):
	N = len(response_count)
	ind = np.arange(N)
	width = 0.25
	maxcount = max(response_count)

	fig, ax = plt.subplots()
	plt.subplots_adjust(bottom=.5, left=.6)
	rects = ax.bar(ind+width, response_count, width, color="black", align="center")

	ax.set_ylabel("Number of customers (n=39)")
	ax.set_ymargin(1)
	ax.set_ylim(top=((maxcount/10+1)*10))

	ax.set_xticks(ind+width)
	plt.xticks(rotation=90)
	ax.set_xticklabels(response_label, multialignment="right")

	# Add numeric labels on top of bars.
	for rect in rects:
		height = rect.get_height()
		ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
				ha="center", va="bottom")

	plt.savefig("".join(["pic/", str(id), ".png"]))
	plt.close()

def plot_horizontal_bar(id, response_count, response_label):
	max_count = max(response_count)
	ypos = np.arange(len(response_label))
	
	fig, ax = plt.subplots()
	rects = plt.barh(ypos, response_count, align="center", color="black", height=.25)

	plt.yticks(ypos, response_label)
	plt.xlim(xmax=((max_count/10+1)*10))
	plt.rcParams.update({'font.size': 10})
	plt.xlabel("Number of customers (n=39)")
	if id==528410987:
		plt.subplots_adjust(left=.4)
	else:
		plt.subplots_adjust(left=.3)
	
	for rect in rects:
		width = rect.get_width()
		ax.text(width+.5, rect.get_y()+rect.get_height()/2., '%d'%int(width),
				ha="left", va="center")

	plt.savefig("".join(["pic/", str(id), ".png"]))
	plt.close()

def main():
    con = sqlite3.connect('surveyresults.db')
    con.text_factory = str
    cur = con.cursor()

    cur.execute("SELECT QuestionID FROM Questions WHERE QType = 40;") # TODO: Other question types?
    question_ids = [r[0] for r in cur.fetchall()]

    iteration = 0
    for id in question_ids:

        # For each question, get count of responses and response labels.
        cur.execute(("SELECT Questions.Heading, count(*), QuestionOptions.OptionLabel, QuestionOptions.OptionText, Questions.QuestionID \
                        FROM Questions, QuestionOptions, Responses \
                        WHERE Questions.QuestionID=? AND QuestionOptions.QuestionID=? AND QuestionOptions.OptionID=Responses.Key1 \
                        GROUP BY Questions.QuestionID, QuestionOptions.OptionID;"), [id, id])
        
        responses = cur.fetchall()
        responses = sorted(responses, key=lambda x: x[1])
        
        # Debugging information to compare to SurveyMonkey counts
        print iteration, responses[0][4], responses[0][0]
        print r"\begin{itemize}"
        for (heading, count, label, text, id) in responses:
            #print label, count, text
            print r"\item", text
        print r"\end{itemize}"
        print 
        
        response_count = [r[1] for r in responses]
        response_label = [r[2] for r in responses]

        # Plot responses.
        #plot_vertical_bar(id, response_count, response_label)
        plot_horizontal_bar(id, response_count, response_label)
        iteration += 1

if __name__ == "__main__":
	main()

	
