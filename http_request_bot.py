import requests

s = requests.Session()

# add to basket
pload = '{"fupid":"10213971","quantity":1}'
get = s.get('https://www.currys.co.uk/gbuk/phones-broadband-and-sat-nav/mobile-phones-and-accessories/mobile-phone-cases/xqisit-samsung-galaxy-a21s-flex-case-clear-10213971-pdt.html')
post = s.post('https://www.currys.co.uk/api/cart/addProduct', data=pload)
print("Added to basket: " + str(post.status_code))

# delivery location
pload = '{"location":"PA2 8RT","latitude":55.8250598,"longitude":-4.4427907}'
put = s.put('https://api.currys.co.uk/store/api/baskets/2c157734-f5f8-4f22-a0bc-8e5e6af83215/deliveryLocation', headers=headers, data=pload)
print("Delivery location: " + str(put.status_code))
print(put.content)

"""
#delivery slot
pload = {"provider":"small_box_home_delivery_standard_delivery","priceAmountWithVat":0,"priceVatRate":20,"priceCurrency":"GBP","date":"2021-03-26","timeSlot":"2DST"}
post = s.post('https://api.currys.co.uk/store/api/baskets/607f6048-113d-45cc-abc2-bd82f9770b98/consignments/small-box-home-delivery/deliverySlot', data=pload)
print("Delivery Slot: " + str(post.status_code))

#delivery info
pload = {"type":"guest","title":"mr","firstName":"Calum","lastName":"McDonald","email":"calumcdonald@gmail.com","company":"null","line1":"103 Donaldswood Park","line2":"null","line3":"null","city":"Paisley","postCode":"PA2 8RT","phone":"07771224622"}
post = s.post("https://api.currys.co.uk/store/api/customers/104612810/addresses", data=pload)
print("Delivery info: " + str(post.status_code))
"""