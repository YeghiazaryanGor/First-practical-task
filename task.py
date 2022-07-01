import csv, math, sys, datetime  # Importing the necessary modules to work with data

ra = float(input("Write Ra "))
dec = float(input("Write Dec "))
N = int(input("Write amount of stars "))
fov_h = float(input("Write horizontal field of view "))
fov_v = float(input("Write vertical field of view "))
cols = ["ra_ep2000", "dec_ep2000", "b"]
used_data = {}

with open("337.all.tsv") as file:
    tsv_file = csv.reader(file, delimiter='\t')
    tsv_file_data = list(tsv_file)


def cols_used(data, columns):  # Selecting the columns that we will use during the task
    for col in columns:
        used_data[col] = []
        for i in range(2, len(data)):
            try:  # If there is nothing in the necessary data, exit
                used_data[col].append(float(data[i][data[1].index(col)]))
            except:
                sys.exit("Invalid dataset!")


cols_used(tsv_file_data, cols)

stars_in_fov = {k: [] for k in used_data.keys()}
starID = []


def fov_filtering(viewh, viewv):  # Selecting the stars that are in our field of view
    for i in range(len(used_data["ra_ep2000"])):
        if (-viewh / 2 < used_data["ra_ep2000"][i] < viewh / 2) and (
                -viewv / 2 < used_data["dec_ep2000"][i] < viewv / 2):
            for col in used_data:
                stars_in_fov[col].append(used_data[col][i])
            starID.append(i + 3)


fov_filtering(fov_h, fov_v)
if stars_in_fov:
    pass
else:
    sys.exit("There are not stars in this field of view, please try again!")

brightest_stars = {}


def brightest_n_stars(num):  # Selecting the brightest N stars from our field of view
    for i in range(num):
        brightest_star = 0
        place = 0
        for j in range(len(stars_in_fov['b'])):
            if brightest_star > stars_in_fov["b"][j]:
                brightest_star = stars_in_fov["b"][j]
                place = starID[j]
        brightest_stars[brightest_star] = place
        try:
            stars_in_fov["b"][stars_in_fov["b"].index(
                brightest_star)] = 10000  # Don't want to remove it from the list because it will mess up the indexes
        except ValueError:
            sys.exit("Invalid data, please try again!")


brightest_n_stars(N)

distances = {}


def calculate_distance(pointRa, pointDec):  # Calculating distance by transforming ra/dec to xyz coordinates
    x = math.cos(pointRa) * math.cos(pointDec)
    y = math.sin(pointRa) * math.cos(pointDec)
    z = math.sin(pointDec)
    for i in brightest_stars.values():
        x1 = math.cos(stars_in_fov["ra_ep2000"][starID.index(i)]) * math.cos(
            stars_in_fov["dec_ep2000"][starID.index(i)])
        y1 = math.sin(stars_in_fov["ra_ep2000"][starID.index(i)]) * math.cos(
            stars_in_fov["dec_ep2000"][starID.index(i)])
        z1 = math.sin(stars_in_fov["dec_ep2000"][starID.index(i)])
        distances[math.sqrt((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2)] = i


calculate_distance(ra, dec)


def sorting_distance(dist):  # Sorting distances
    star_dist = list(dist.keys())
    n = len(star_dist)
    for i in range(n):
        for j in range(n - i - 1):
            if star_dist[j] > star_dist[j + 1]:
                star_dist[j], star_dist[j + 1] = star_dist[j + 1], star_dist[j]
    return star_dist


dists = sorting_distance(distances)
header = ["ID", "Ra", "Dec", "Brightness", "Distance"]
data = []
mag, num = list(brightest_stars.keys()), list(brightest_stars.values())


def data_collector(N):  # Collecting the all necessary data for the output
    for i in range(N):
        id = distances[dists[i]]
        star_ra = stars_in_fov["ra_ep2000"][starID.index(id)]
        star_dec = stars_in_fov["dec_ep2000"][starID.index(id)]
        star_b = mag[num.index(id)]
        star_distance = dists[i]
        data.append([id, star_ra, star_dec, star_b, star_distance])


data_collector(N)
current_time = datetime.datetime.now()
current_timestamp = current_time.timestamp()
with open(str(current_timestamp), "w") as fl:
    writer = csv.writer(fl)
    writer.writerow(header)
    writer.writerows(data)
