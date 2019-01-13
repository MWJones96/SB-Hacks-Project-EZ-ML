import csv


f = open('data.csv')
csv_f = list(csv.reader(f))

data = [[]]
i = 0
j = 0

for i in range(0,len(csv_f)):
	row = []
	# row = csv_f[i]
	for j in range(0,len(csv_f[0])):
		item = csv_f[i][j]
		row.append(item)
	data.append(row)
f.close()
print str(data)[1:-1]


	
