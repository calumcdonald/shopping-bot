import requests
import json
from datetime import datetime, timedelta

with open("data/details.json") as f:
    data = json.load(f)

with open("data/products.json") as f:
    products = json.load(f)

product = products['phone_case']

s = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

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
deldate = datetime.now() + timedelta(days = 2)
pload = {"provider":"small_box_home_delivery_standard_delivery","priceAmountWithVat":0,"priceVatRate":20,"priceCurrency":"GBP","date":deldate.strftime("%Y-%m-%d"),"timeSlot":"2DST"}
put = s.put('https://api.currys.co.uk/store/api/baskets/' + cart_id + '/consignments/small-box-home-delivery/deliverySlot', headers=headers, data=pload)
print("Delivery slot status code: " + str(put.status_code))

# get the customer id
pload = json.dumps({'email':data['email'],'isGuest':True,'password':''})
post = s.post("https://api.currys.co.uk/store/api/customers", headers=headers, data=pload)
customer_id = json.loads(post.content)['payload']['customerId']
print(customer_id)

# stumped from here
# marketing preferences
pload = json.dumps({"email":data['email'],"phone":data['mobile'],"specialOffersViaEmail":False})
put = s.put('https://api.currys.co.uk/store/api/customers/' + customer_id + '/marketingPreferences', headers=headers, data=pload)
print("Marketing preferences status code: " + str(put.status_code))

# delivery info
pload = json.dumps({"type":"guest","title":"mr","firstName":data['firstname'],"lastName":data['surname'],"email":data['email'],"company":None,"line1":data['address1'],"line2":None,"line3":None,"city":data['city'],"postCode":data['postcode'],"phone":data['mobile']})
post = s.post('https://api.currys.co.uk/store/api/customers/' + customer_id + '/addresses', headers=headers, data=pload)
print("Delivery info status code: " + str(post.status_code))

# payment method
pload = {"paymentMethodType":"card"}
post = s.post('https://api.currys.co.uk/store/api/baskets/' + cart_id + '/payments', headers=headers, data=pload)
print("Payment method status code: " + str(post.status_code))