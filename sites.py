import csv
import json

from pprint import pprint
from geopy.geocoders import Nominatim


def json_dump(data, outfile_path):
    with open(outfile_path, 'w') as outfile:
            json.dump(data, outfile)

def json_load(infile_path):
    with open(infile_path, 'r') as infile:
        return json.load(infile)

#
# def fix_zipcode_coords():
#     zipcodes = json_load('./zipcodes.json')
#
#     for feature in zipcodes['features']:
#         print feature['properties']['ZIP']
#         fixed_coords = []
#         for coord in feature['geometry']['coordinates'][0]:
#             print coord
#             lat = coord[1]
#             long = coord[0]
#             fixed_coords.append([lat, long])
#
#         feature['geometry']['coordinates'][0] = fixed_coords
#         print "changed"
#         for coord in feature['geometry']['coordinates'][0]:
#             print coord
#
#     json_dump(zipcodes, 'zipcodes_fixed.json')


geolocator = Nominatim(user_agent="colonial_residue_map")

def address_to_coord(addr):

    print addr

    # if '333 n michigan' in addr:
        # addr += "chicago, IL"

    try:
        location = geolocator.geocode(addr)
        # print((location.latitude, location.longitude))
        print location.address
        return [ location.longitude, location.latitude ]

    except:
        if "1130 Midway" in addr:
            print addr
            return [ -87.598260, 41.787250 ]
        else:
            print "Geolocateor failed for {}".format(address)
            return [0, 0]


print address_to_coord('1227 w altgeld st, chicago, il 60614')

sites_json = {
    "type": "FeatureCollection",
    "features": []
}


with open('submissions.csv', 'rb') as f:
    reader = csv.reader(f)
    submissions = list(reader)

print "HELLO", sites_json['features']


emails = []

list_of_sites = []

for i, line in enumerate(submissions):
    # print line
    print "\n", i

    if i == 0:
        continue
    # for x in line:
        # print x

    date = line[0]
    email = line[1]
    emails.append(email)
    author = line[2]
    place = line[3]
    address = line[4]
    coord = address_to_coord(address)
    image = line[5]
    description = line[6]

    note = "(Image does not have to be included. I just had to submit this form with an image)"

    if note in description:
        description = description.split(note)[1]


    # print "date: ", date
    # print "email: ", email
    # print "author: ", author
    # print "place: ", place
    # print "address: ", address
    # print "coord: ", coord
    # print "image: ", image
    # print "description: ", description


    feature_json = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coord
        },
        "properties": {
            "name": place,
            "address": address,
            "description": description,
            "img": image,
            "investigator": author,
            "latitude": coord[0],
            "longitude": coord[1]
        }
    }

    # remove old submissions (listed in chronological order, duplicate means old one is bad)
    for site in list_of_sites:
        if site[1] == email:
            list_of_sites.remove(site)

    list_of_sites.append([date, email, author, place, address, coord, image, description,  feature_json])



for site in list_of_sites:
    sites_json['features'].append(site[-1])


# pprint(sites_json)


json_dump(sites_json, 'sites.json')
