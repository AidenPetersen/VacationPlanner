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

def radiusquery(lat, long, rad):
    str = f"radius={rad}&limit=25&offset=0&lat={lat}&lon={long}&format=json"
    return str


def otmget(method, query):
    OTM_KEY = "5ae2e3f221c38a28845f05b6e93dcff7317a493d8bb313a3fd186d0c"

    reqstr = "https://api.opentripmap.com/0.1/en/places/"
    reqstr += method + "?apikey=" + OTM_KEY + "&" + query
    r = requests.get(reqstr)
    print(r.text)

# otmget("radius",radiusquery(41.66127,-91.53680, 1000))