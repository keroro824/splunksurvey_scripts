import json

INFILE = 'splunksurvey.json'
OUTFILE = 'splunksurvey_polished.json'

lookup = {}
count = 1

infile = open(INFILE, "r")
data = json.load(infile)
for question in data:
  customers = question['customers']
  for customer in customers:
    if customer[0] not in lookup:
      lookup[customer[0]] = count
      count += 1
new = data
for question in new:
  customers = question['customers']
  for customer in customers:
    customer[0] = lookup[customer[0]]
outfile = open(OUTFILE, "w")
print new
json.dump(new, outfile, indent=4)