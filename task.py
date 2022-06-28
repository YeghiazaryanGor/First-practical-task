import csv  # Importing csv module to work with data
import math

ra = 28
dec = 37
N = 10
fov_h = 60
fov_v = 70
cols = ["ra_ep2000", "dec_ep2000", "b"]
Data_sample = {}
with open("337.all.tsv") as file:
    tsv_file = csv.reader(file, delimiter='\t')
    data = list(tsv_file)


def cols_used(fl, columns):  # Selecting the columns that we will use during the task
    for col in columns:
        Data_sample[col] = []
        for i in range(2, len(fl)):
            Data_sample[col].append(float(fl[i][fl[1].index(col)]))


cols_used(data, cols)

stars_in_fov = {k: [] for k in Data_sample.keys()}
starID = []


def fov_filtering(fov_h, fov_v):  # Selecting the stars that are in our field of view
    for j in range(len(Data_sample["ra_ep2000"])):
        if (-fov_h / 2 < Data_sample["ra_ep2000"][j] < fov_h / 2) and (
                -fov_v / 2 < Data_sample["dec_ep2000"][j] < fov_v / 2):
            for col in Data_sample:
                stars_in_fov[col].append(Data_sample[col][j])
            starID.append(j + 3)


fov_filtering(fov_h, fov_v)
print(len(stars_in_fov["b"]))
print(stars_in_fov["ra_ep2000"])
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
        try:
            stars_in_fov["b"][stars_in_fov["b"].index(brightestStar)] = 10000
        except ValueError:
            pass


brightest_n_stars(N)
print(brightest_stars)
distances = {}


def calculate_distance(ra, dec):
    x = math.cos(ra) * math.cos(dec)
    y = math.sin(ra) * math.cos(dec)
    z = math.sin(dec)
    for i in brightest_stars.values():
        x1 = math.cos(stars_in_fov["ra_ep2000"][starID.index(i)]) * math.cos(
            stars_in_fov["dec_ep2000"][starID.index(i)])
        y1 = math.sin(stars_in_fov["ra_ep2000"][starID.index(i)]) * math.cos(
            stars_in_fov["dec_ep2000"][starID.index(i)])
        z1 = math.sin(stars_in_fov["dec_ep2000"][starID.index(i)])
        distances[math.sqrt((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2)] = i


calculate_distance(ra, dec)
print(distances)


def sorting_distance(dist):
    starDist = list(dist.keys())
    n = len(starDist)
    for i in range(n):
        for j in range(n - i - 1):
            if starDist[j] > starDist[j + 1]:
                starDist[j], starDist[j + 1] = starDist[j + 1], starDist[j]
    return starDist
