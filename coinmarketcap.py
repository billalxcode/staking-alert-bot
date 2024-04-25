from coinmarketcapapi import CoinMarketCapAPI

API_KEY = "165526c2-ae2f-4e24-8fb4-1cfa4390ef58"

cmc = CoinMarketCapAPI(api_key=API_KEY)
rep = cmc.tools_priceconversion(symbol="PIA", amount=1)
print (rep.credit_count)
print (rep.data[0]['quote']['USD']['price'])