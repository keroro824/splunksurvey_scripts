
import sys
import sqlite3
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt

def main():
    con = sqlite3.connect('surveyresults.db')
    con.text_factory = str
    cur = con.cursor()
    
    cur.execute("SELECT ResponsesText FROM ResponsesText WHERE QuestionID=528408871")
    responses = cur.fetchall()
    print r"\squishitem"
    for (response,) in responses:
        print r"\item", response
    print r"\squishend"
    
    cur.execute("SELECT ResponsesText FROM ResponsesText WHERE QuestionID=528408904")
    values = [int(r[0]) for r in cur.fetchall()]

    d = {}
    d["0-9"] = 0
    d["10-99"] = 0
    d["100-999"] = 0
    d["1000+"] = 0

    for value in values:
        if value >= 0 and value <= 9:
            d["0-9"] += 1
        if value >= 10 and value <= 99:
            d["10-99"] += 1
        if value >= 100 and value <= 999:
            d["100-999"] += 1
        if value >= 1000:
            d["1000+"] += 1

    d = sorted(d.items(), key=lambda x: x[0])
    response_count = [i[1] for i in d]
    print response_count
    response_label = [i[0] for i in d]

    max_count = max(response_count)
    ypos = np.arange(len(response_label))
    
    fig, ax = plt.subplots()
    rects = plt.barh(ypos, response_count, align="center", color="black", height=.25)

    plt.yticks(ypos, response_label)
    plt.xlim(xmax=((max_count/10+1)*10))
    plt.xlabel("Number of customers (n=42)")
    plt.subplots_adjust(left=.3)
    
    for rect in rects:
        width = rect.get_width()
        ax.text(width+.5, rect.get_y()+rect.get_height()/2., '%d'%int(width),
                ha="left", va="center")

    plt.savefig("".join(["figs/528408904.png"]))
    plt.close()

if __name__ == "__main__":
    main()
