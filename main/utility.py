from asyncio import run
from haversine import haversine, Unit
from typing import Tuple, List

from yelpapi import YelpAPI
import requests
from math import radians, sin, cos, acos, ceil


class PlaceNode:
    name = None
    lat = 0
    long = 0
    rating = 0
    misc = {}



    def __str__(self):
        time = 0
        for x in self.misc['kinds'].split(','):
            if x in time_dict:
                time = time_dict[x]
                break
        return "stay at " + str(self.name) + " for " + str(time) + " hours"

    def __init__(self, name, lat, long, rating, misc):
        self.name = name
        self.lat = float(lat)
        self.long = float(long)
        self.rating = rating
        self.misc = misc

    def get_favor(self, other):
        distance = (coords_to_dist(self.lat, self.long, other.lat, other.long))
        return other.rating / (distance ** 2), distance

    def get_next_attraction(self, available: list, visited: list):
        max_favor = 0
        distance = 0
        max_obj = None
        for i in available:
            if (not visited.__contains__(i)) and (self.get_favor(i)[0] > max_favor):
                max_favor, distance = self.get_favor(i)
                max_obj = i

        visited.append(max_obj)
        if max_obj is None:
            raise Exception('Not enough places')
        return max_obj, distance


def get_yelp_review(latitude: float, longitude: float, name: str, token_num: int) -> float:
    # tokens = [
    #     "JwyKsopjKmwG41IpB_mUzDtY7JSiNZsPGpiWzdlGrDZ5GHfXZE0kCx11sPtH-epP20pBnbUXxj4Nhz_AY0cKzTBktSbu2CjnfLfyyM-wsUeleiAM1YStOBFdvHl7YHYx ",
    #     "pUUE2sp9znWz3doMfBQuO9NpsjrXxd1buJ5ECvqcuUmgnDYxf5ov375i9xwThXEZ_7sQJuPN_djpXGF9GMChQWgrpsxw1lyytnBh4V3W3IK_CYIK4m_2bALI8bV7YHYx",
    #     "rzbaE_ls0PITatDUuJrGK_sxkXRsoCfkflk8KAr_USpYfdy-8hV_At3W8qQdAtC3Jw6F6r8T38zt_QKX8LLxBwefZxX3P1QnhKYN1mUr-e5or5fpNSoSgufLG7d7YHYx"]
    tokens = [
        'ZXKOaBUsftySJ9WlHg2Vr-pjNpcfTg--4K89dratYsHrfRIj0Vw9MqsFLTQREaTOkrxzheA4KPrbd1jIMJuJypj8QcrHvsHQYNs3EJgfNF-gQtQH6RzvqipN_1d8YHYx',
        'cIUBiccbQCizZmj-2MpQrBgmDg3ibWcjVGDkC8xk76L7G4KaHmx2s-Qpq7STWo0GldLVsp6LAmWbLJ682Eq00OQ5b3FzC_hWmk8BPKmPghJ9u6rm8kPDGAQI_Fp8YHYx'
    ]
    token_num = token_num % len(tokens)
    yelp_api = YelpAPI(tokens[token_num])
    response = yelp_api.search_query(latitude=latitude, longitude=longitude, term=name, radius=200, limit=1)
    print(name)
    try:
        return response['businesses'][0]['rating']
    except (IndexError, TypeError):
        return 0


def format_attractions(latitude: float, longitude: float, radius: int) -> Tuple[List[PlaceNode], List[PlaceNode]]:
    attractions_list = otm_get("radius", attractions_query(latitude, longitude, radius))
    foods_list = otm_get("radius", foods_query(latitude, longitude, radius))

    # attractions_ratings = [get_yelp_review(x['point']['lat'], x['point']['lon'], x['name']) for x in attractions_list]

    async def add_review(arr, lat, lon, n, t):
        arr.append(get_yelp_review(lat, lon, n, t))

    attractions_ratings = []
    foods_rating = []
    counter = 0
    for x in attractions_list:
        if 'interesting_places' in x['kinds'] and 'foods' not in x['kinds']:
            run(add_review(attractions_ratings, x['point']['lat'], x['point']['lon'], x['name'], counter))
            counter += 1

    for x in foods_list:
        run(add_review(foods_rating, x['point']['lat'], x['point']['lon'], x['name'], counter))
        counter += 1

    attractions = []
    foods = []
    index = 0
    for rating in attractions_ratings:
        print(str(rating) + " attraction")
        if rating > 3.5:
            name = attractions_list[index]['name']
            if name:
                lat = attractions_list[index]['point']['lat']
                lon = attractions_list[index]['point']['lon']

                attractions.append(PlaceNode(name, lat, lon, rating, attractions_list[index]))
        index += 1

    index = 0
    for rating in foods_rating:
        print(str(rating) + " food")
        if rating > 3.5:
            name = foods_list[index]['name']
            print(name)
            if name is not None and name:
                lat = foods_list[index]['point']['lat']
                lon = foods_list[index]['point']['lon']

                foods.append(PlaceNode(name, lat, lon, rating, foods_list[index]))
        index += 1

    return attractions, foods


def attractions_query(latitude: float, longitude: float, rad: int) -> str:
    limit = 400
    whitelist = 'architecture%2Ccultural%2Chistoric%2Cnatural%2Cshops%2Camusements'
    string = f"radius={rad}&limit={limit}&offset=0&lat={latitude}&lon={longitude}&format=json&kinds={whitelist}"
    return string


def foods_query(latitude: float, longitude: float, rad: int) -> str:
    limit = 100
    whitelist = 'foods'
    string = f"radius={rad}&limit={limit}&offset=0&lat={latitude}&lon={longitude}&format=json&kinds={whitelist}"
    return string


def otm_get(method: str, query: str):
    otm_key = "5ae2e3f221c38a28845f05b6e93dcff7317a493d8bb313a3fd186d0c"

    reqstr = "https://api.opentripmap.com/0.1/en/places/"
    reqstr += method + "?apikey=" + otm_key + "&" + query
    r = requests.get(reqstr)
    print(r)
    return r.json()


def coords_to_dist(slat: float, slon: float, elat: float, elon: float) -> float:
    return haversine((slat, slon), (elat, elon))


def get_path(lat, lon, days, radius, available, food):
    visited = []
    path = []
    print("avail" + str(available))
    print("food" + str(food))
    try:
        for i in range(days):
            time = 9
            n, dist = get_next_attraction_s(lat, lon, available, visited)
            lunch = False
            while time < 19:
                if time > 11 and not lunch:
                    n, dist = n.get_next_attraction(food, visited)
                    print(str(dist) + "km")
                    travel_time = 1 / 15 * dist
                    time += travel_time
                    for x in n.misc['kinds'].split(','):
                        if x in time_dict:
                            time += time_dict[x]
                            break
                    path.append(f"Travel {ceil(travel_time * 60)} minutes eat at {n.name}")
                    path.append(n)

                    lunch = True
                else:
                    print(str(dist) + "km")
                    n, dist = n.get_next_attraction(available, visited)
                    travel_time = dist / 6
                    time += travel_time * dist + 1
                    path.append(f"Travel {ceil(travel_time * 60)} minutes to {n}")

                    #path.append(n)
            n, dist = n.get_next_attraction(food, visited)
            travel_time = 1 / 15 * dist
            path.append(f"Travel {ceil(travel_time * 60)} minutes eat at {n.name}")
            path.append(n)
        return path
    except Exception:
        return ['Error, not enough interesting places to visit. Go somewhere more interesting.']


def get_next_attraction_s(lat, lon, available: list, visited: list):
    dummy = PlaceNode(None, lat, lon, 0, {})
    max_favor = 0
    max_obj = None
    distance = 0
    for i in available:
        if (not visited.__contains__(i)) and (dummy.get_favor(i)[0] > max_favor):
            max_favor, distance = dummy.get_favor(i)
            max_obj = i

    visited.append(max_obj)
    if max_obj is None:
        raise Exception('not enough attractions')
    return max_obj, distance


# architecture%2Ccultural%2Chistoric%2Cnatural%2Cfoods%2Cshops%2Camusements'
time_dict = {
    "architecture": 2,
    "cultural": 3,
    "natural": 3,
    "historic": 2,
    "foods": 1,
    "shops": 1,
    "amusements": 6
}

# otmget("radius",radiusquery(41.66127,-91.53680, 1000))
