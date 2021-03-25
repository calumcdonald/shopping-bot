import requests
import json

with open("data/details.json") as f:
    data = json.load(f)

with open("data/products.json") as f:
    products = json.load(f)

product = products['phone_case']

s = requests.Session()
headers = {'Referer':'https://www.currys.co.uk/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

# add to basket
pload = '{"fupid":"' + product['pid'] + '","quantity":1}'
# do i need this get?
get = s.get(product['url'])
post = s.post('https://www.currys.co.uk/api/cart/addProduct', data=pload)
print("Add to basket status code: " + str(post.status_code))

# get cart id
post = s.post("https://api.currys.co.uk/store/api/token")
cart_id = json.loads(post.content)['bid']

# delivery location
pload = {'location': 'PA2 8RT', 'latitude': 55.8250598, 'longitude': -4.4427907}
put = s.put('https://api.currys.co.uk/store/api/baskets/' + cart_id + '/deliveryLocation', headers=headers, data=pload)
print("Delivery location status code: " + str(put.status_code))

# delivery slot
pload = {"provider":"small_box_home_delivery_standard_delivery","priceAmountWithVat":0,"priceVatRate":20,"priceCurrency":"GBP","date":"2021-03-27","timeSlot":"2DST"}
put = s.put('https://api.currys.co.uk/store/api/baskets/' + cart_id + '/consignments/small-box-home-delivery/deliverySlot', headers=headers, data=pload)
print("Delivery slot status code: " + str(put.status_code))

# stumped from here
# marketing preferences
pload = {"email":"{}".format(data['email']),"phone":"{}".format(data['mobile']),"specialOffersViaEmail":"false"}
put = s.put('https://api.currys.co.uk/store/api/customers/104612810/marketingPreferences', headers=headers, data=pload)
print("Marketing preferences status code: " + str(put.status_code))

# delivery info
pload = {"type":"guest","title":"mr","firstName":"{}".format(data['firstname']),"lastName":"{}".format(data['surname']),"email":"{}".format(data['email']),"company":None,"line1":"{}".format(data['address1']),"line2":None,"line3":None,"city":"{}".format(data['city']),"postCode":"{}".format(data['postcode']),"phone":"{}".format(data['mobile'])}
post = s.post("https://api.currys.co.uk/store/api/customers/104612810/addresses", headers=headers, data=pload)
print("Delivery info status code: " + str(post.status_code))