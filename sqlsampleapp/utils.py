import requests
import urllib
import re

from geopy.distance import geodesic

def make_dis(pos1, pos2):
    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
    s_quote = urllib.parse.quote(pos1)
    response = requests.get(makeUrl + s_quote)
    longitude1, latitude1 = response.json()[0]["geometry"]["coordinates"]

    s_quote = urllib.parse.quote(pos2)
    response = requests.get(makeUrl + s_quote)

    longitude2, latitude2 = response.json()[0]["geometry"]["coordinates"]

    distance = geodesic((latitude1,longitude1),(latitude2,longitude2))
    num = round(float((re.search(r"[+-]?(?:\d+\.\d*|\.\d+|\d+\.)",str(distance))).group()),1)
    return(num)


pos1='石川県金沢市もりの里1丁目45-1'
pos2='千葉県南房総市富浦町青木123-1'

num=make_dis(pos1,pos2)
print(num)
