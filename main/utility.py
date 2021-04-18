from asyncio import run, wait

from yelpapi import YelpAPI
import requests
from math import radians, sin, cos, acos
import threading


def get_yelp_review(latitude: float, longitude: float, name: str, token_num: int) -> float:
    tokens = [
        "JwyKsopjKmwG41IpB_mUzDtY7JSiNZsPGpiWzdlGrDZ5GHfXZE0kCx11sPtH-epP20pBnbUXxj4Nhz_AY0cKzTBktSbu2CjnfLfyyM-wsUeleiAM1YStOBFdvHl7YHYx ",
        "pUUE2sp9znWz3doMfBQuO9NpsjrXxd1buJ5ECvqcuUmgnDYxf5ov375i9xwThXEZ_7sQJuPN_djpXGF9GMChQWgrpsxw1lyytnBh4V3W3IK_CYIK4m_2bALI8bV7YHYx",
        "rzbaE_ls0PITatDUuJrGK_sxkXRsoCfkflk8KAr_USpYfdy-8hV_At3W8qQdAtC3Jw6F6r8T38zt_QKX8LLxBwefZxX3P1QnhKYN1mUr-e5or5fpNSoSgufLG7d7YHYx"]
    yelp_api = YelpAPI(tokens[token_num])
    response = yelp_api.search_query(latitude=latitude, longitude=longitude, term=name, radius=100, limit=1)
    print(name)
    try:
        return response['businesses'][0]['rating']
    except (IndexError, TypeError):
        return 0


def format_attractions(latitude: float, longitude: float, radius: int) -> list:
    attractions_list = otm_get("radius", radius_query(latitude, longitude, radius))

    # attractions_ratings = [get_yelp_review(x['point']['lat'], x['point']['lon'], x['name']) for x in attractions_list]

    async def add_review(arr, lat, lon, n, t):
        arr.append(get_yelp_review(lat, lon, n, t))

    attractions_ratings = []
    counter = 0
    for x in attractions_list:
        run(add_review(attractions_ratings, x['point']['lat'], x['point']['lon'], x['name'], counter))
        counter += 1
        counter %= 3

    attractions = []
    index = 0
    for rating in attractions_ratings:
        print(rating)
        if rating > 3.5:
            name = attractions_list[index]['name']
            if name:
                lat = attractions_list[index]['point']['lat']
                lon = attractions_list[index]['point']['lon']

                attractions.append(PlaceNode(name, lat, lon, rating, attractions_list[index]))
        index += 1
    return attractions


def radius_query(latitude: float, longitude: float, rad: int) -> str:
    limit = 1000
    whitelist = 'architecture%2Ccultural%2Chistoric%2Cnatural%2Cfoods%2Cshops%2Camusements'
    string = f"radius={rad}&limit={limit}&offset=0&lat={latitude}&lon={longitude}&format=json&kinds={whitelist}"
    return string


def otm_get(method: str, query: str):
    otm_key = "5ae2e3f221c38a28845f05b6e93dcff7317a493d8bb313a3fd186d0c"

    reqstr = "https://api.opentripmap.com/0.1/en/places/"
    reqstr += method + "?apikey=" + otm_key + "&" + query
    r = requests.get(reqstr)
    return r.json()


def coords_to_dist(slat: float, slon: float, elat: float, elon: float) -> float:
    slat = radians(slat)
    slon = radians(slon)
    elat = radians(elat)
    elon = radians(elon)
    return 6371.01 * acos(sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon))


def get_next_attraction(self, available: list, visited: list, lat: float, lon: float):
    max_favor = 0
    max_obj = None
    for i in available:
        if self.get_favor(i) > max_favor:
            max_favor = self.get_favor(i)
            max_obj = i
            visited.append(i)

    return max_obj


def get_next_attraction_s(lat, lon, available: list, visited: list):
    dummy = PlaceNode(None, lat, lon, 0, {})
    max_favor = 0
    max_obj = None
    for i in available:
        if (not visited.__contains__(i)) and (dummy.get_favor(i) > max_favor):
            max_favor = dummy.get_favor(i)
            max_obj = i
            visited.append(i)

    return max_obj


class PlaceNode:
    name = None
    lat = 0
    long = 0
    rating = 0
    mist = {}

    def __str__(self):
        return "wip"

    def __init__(self, name, lat, long, rating, misc):
        self.name = name
        self.lat = lat
        self.long = long
        self.rating = rating
        self.misc = misc

    def get_favor(self, other) -> float:
        return other.rating / ((coords_to_dist(self.lat, self.long, other.lat, other.long)) ** 2)

    def get_next_attraction(self, available: list, visited: list):
        max_favor = 0
        max_obj = None
        for i in available:
            if (not visited.__contains__(i)) and (self.get_favor(i) > max_favor):
                max_favor = self.get_favor(i)
                max_obj = i
                visited.append(i)

        return max_obj

#architecture%2Ccultural%2Chistoric%2Cnatural%2Cfoods%2Cshops%2Camusements'
time_dict = {
    "architecture" : 2,
    "cultural" : 3,
    "natural" : 3,
    "historic": 2,
    "foods" : 2,
    "shops" : 1,
    "amusements" : 6
}



# otmget("radius",radiusquery(41.66127,-91.53680, 1000))
