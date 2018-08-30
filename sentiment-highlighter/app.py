import json
import csv

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
	# df = pd.read_csv('data.csv').drop('Open', axis=1)
	# chart_data = df.to_dict(orient='records')
	# chart_data = json.dumps(chart_data, indent=2)
	# data = {'chart_data': chart_data}
	return render_template("index.html")

@app.route('/search', methods= ['POST', 'GET'])
def search():
	# if request.method == 'POST':
	result = request.form['tweet']
	print(result)

	dictionary = {}
	ref = {}
	ref["nodes"] = []
	ref["links"] = []

	with open('../../SentiWordNet_3.0.0/SentiWordNet_3.0.0_20130122.txt') as file:
		data = file.readlines()
		for line in data:
			line = line.rstrip()
			if line[0] == '#':
				continue
			items = line.split("\t")
			pos = items[2]
			neg = items[3]
			words = items[4].split(" ")
			for word in words:
				dictionary[word.replace("_", " ")[:len(word) - 2]] = (pos, neg)

	# sampleTweet = "There is nothing that I would want more for our Country than true FREEDOM OF THE PRESS. The fact is that the Press is FREE to write and say anything it wants, but much of what it says is FAKE NEWS, pushing a political agenda or just plain trying to hurt people. HONESTY WINS!"
	
	sampleTweet = result.lower()
	words = sampleTweet.split(" ")
	prev = ""
	for index, word in enumerate(words):
		if word in dictionary:
			pos, neg = dictionary[word]
			ntype = 3
			if pos > neg:
				ntype = 1
			if neg > pos:
				ntype = 2
			ref["nodes"].append({
				"id": index,
				"group": ntype,
				"word": word,
			})
			# print(word, dictionary[word])
		else:
			ref["nodes"].append({
				"id": index,
				"group": 3,
				"word": word,
			})
			# print(word)
		if prev:
			ref["links"].append({
				"source": prev,
				"target": index,
			})
		prev = index

	chart_data = json.dumps(ref, indent=4)

	data = {'chart_data': chart_data}

	return render_template("search.html", data=data)

if __name__ == "__main__":
	app.run(debug=True)
