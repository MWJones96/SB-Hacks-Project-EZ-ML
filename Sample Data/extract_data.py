import csv

with open('raw_data.csv') as raw_file:
	with open('data.csv', mode='w', newline='') as data_file:
		csv_reader = csv.reader(raw_file, delimiter=',')
		csv_writer = csv.writer(data_file, delimiter=',')
		line_num = 0
		for row in csv_reader:
			if (line_num > 0):
				csv_writer.writerow(row[2::])
			line_num += 1

with open('raw_data.csv') as raw_file:
	with open('targets.csv', mode='w', newline='') as target_file:
		csv_reader = csv.reader(raw_file, delimiter=',')
		csv_writer = csv.writer(target_file, delimiter=',')
		line_num = 0
		for row in csv_reader:
			if (line_num > 0):
				csv_writer.writerow(row[1])
			line_num += 1