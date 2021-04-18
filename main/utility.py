from yelpapi import YelpAPI
import requests


def get_yelp_review(latitude: float, longitude: float, name: str) -> float:
    key = "JwyKsopjKmwG41IpB_mUzDtY7JSiNZsPGpiWzdlGrDZ5GHfXZE0kCx11sPtH-epP20pBnbUXxj4Nhz_AY0cKzTBktSbu2CjnfLfyyM" \
          "-wsUeleiAM1YStOBFdvHl7YHYx "
    yelp_api = YelpAPI(key)
    response = yelp_api.search_query(latitude=latitude, longitude=longitude, term=name, radius=100, limit=1)
    try:
        return response['businesses'][0]['rating']
    except TypeError:
        return -1


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

# otmget("radius",radiusquery(41.66127,-91.53680, 1000))
