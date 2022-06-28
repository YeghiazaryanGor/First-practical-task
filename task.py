import csv  # Importing csv module to work with data

# ra = float(input('ra'))
# dec = float(input('dec'))
N = 10
fov_h = 60
fov_v = 70
cols = ["ra_ep2000","dec_ep2000","b"]
Data_sample = {}
with open("337.all.tsv") as file:
    tsv_file = csv.reader(file, delimiter='\t')
    data = list(tsv_file)


def cols_used(fl, columns):  # Selecting the columns that we will use during the task
    for col in columns:
        Data_sample[col] = []
        for i in range(2,len(fl)):
            Data_sample[col].append(float(fl[i][fl[1].index(col)]))


    # for i in range(2, len(fl)):
    #     Data_sample[columns[0]].append(float(fl[i][0]))
    #     Data_sample[columns[1]].append(float(fl[i][1]))
    #     Data_sample[columns[2]].append(float(fl[i][-1]))


cols_used(data, cols)

stars_in_fov = {k: [] for k in Data_sample.keys()}
starID = []


def fov_filtering(fov_h, fov_v):  # Selecting the stars that are in our field of view
    for j in range(len(Data_sample["ra_ep2000"])):
        if float(Data_sample["ra_ep2000"][j]) < fov_h and float(Data_sample["dec_ep2000"][j]) < fov_v:
            stars_in_fov["ra_ep2000"].append(Data_sample["ra_ep2000"][j])
            stars_in_fov["dec_ep2000"].append(Data_sample["dec_ep2000"][j])
            stars_in_fov["b"].append(Data_sample["b"][j])
            starID.append(j)


fov_filtering(fov_h, fov_v)
print(len(stars_in_fov["b"]))
print(stars_in_fov["b"])
print(starID)
brightest_stars = {}


def brightest_n_stars(N):  # Selecting the brightest N stars from our field of view
    for i in range(N):
        brightestStar = 0
        id = 0
        for j in range(len(stars_in_fov['b'])):
            if brightestStar > stars_in_fov["b"][j]:
                brightestStar = stars_in_fov["b"][j]
                id = starID[j]
        brightest_stars[brightestStar] = id
        stars_in_fov["b"][stars_in_fov["b"].index(brightestStar)] = 10000


brightest_n_stars(N)
print(brightest_stars)
print(len(stars_in_fov["b"]))
