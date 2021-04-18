from yelpapi import YelpAPI
import requests
from math import radians, sin, cos, acos


def get_yelp_review(latitude: float, longitude: float, name: str) -> float:
    key = "JwyKsopjKmwG41IpB_mUzDtY7JSiNZsPGpiWzdlGrDZ5GHfXZE0kCx11sPtH-epP20pBnbUXxj4Nhz_AY0cKzTBktSbu2CjnfLfyyM" \
          "-wsUeleiAM1YStOBFdvHl7YHYx "
    yelp_api = YelpAPI(key)
    response = yelp_api.search_query(latitude=latitude, longitude=longitude, term=name, radius=100, limit=1)
    print(name)
    try:
        return response['businesses'][0]['rating']
    except (IndexError,TypeError):
        return 0


def format_attractions(latitude: float, longitude: float, radius: int) -> list:
    attractions_list = otm_get("radius", radius_query(latitude, longitude, radius))
    attractions_ratings = [get_yelp_review(x['point']['lat'], x['point']['lon'], x['name']) for x in attractions_list]
    attractions = []
    outer_index = 0
    inner_index = 0
    for rating in attractions_ratings:
        print(rating)
        if (rating > 3.5):
            name = attractions_list[outer_index]['name']
            if name:
                attractions.append((attractions_list[outer_index]['name'], rating, attractions_list[outer_index]))
        outer_index += 1
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

# otmget("radius",radiusquery(41.66127,-91.53680, 1000))
