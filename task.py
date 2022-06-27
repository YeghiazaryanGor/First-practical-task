import csv

# ra = float(input('ra'))
# dec = float(input('dec'))
# N = int(input('Amount of stars'))
# fov_h = float(input("fovh"))
# fov_v = float(input("fovv"))
lib = {}
tsvfile = None
with open("337.all.tsv") as file:
    tsv_file = csv.reader(file, delimiter='\t')
    tsvfile = list(tsv_file)


def cols_used(fl, *columns):
    for col in columns:
        lib[col] = []
    for i in range(2, len(fl)):
        lib[columns[0]].append(fl[i][0])
        lib[columns[1]].append(fl[i][1])
        lib[columns[2]].append(fl[i][-1])


cols_used(tsvfile, "RA", "DEC", "b")