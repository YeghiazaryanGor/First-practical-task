import csv

with open("337.all.tsv") as file:
    tsv_file = csv.reader(file, delimiter = '\t')
    for line in tsv_file:
        print(line)


