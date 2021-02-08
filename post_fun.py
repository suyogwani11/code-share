import keys
import hashlib
import hmac
import json
from datetime import datetime

import requests

apiid = keys.apiid
secret = keys.secret
market_url = "https://openapi-exchange.coinbene.com"
now = lambda: datetime.utcnow().isoformat()[:-3] + 'Z'
header_dict = {"Accept": "application/json", "Content-Type": "application/json; charset=UTF-8",
			   "Cookie": "locale=zh_CN"}


def sign(message, secret):
	"""
	gen sign
	:param message: message wait sign
	:param secret:  secret key
	:return:
	"""
	secret = secret.encode('utf-8')
	message = message.encode('utf-8')
	sign = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()
	return sign


# version 2 not working
def place_order_v2(instrument):
	"""
	instrument = {"symbol":"ADA/USDT","price":"0.5","quantity":"10","direction":"1","clientId":apiid}
	direction 1: buy, 2: sell
	"""
	body = json.dumps(instrument).replace(' ', '')
	req = '/api/exchange/v2/order/place{}'.format(body)
	timestamp = now()
	url = '{}{}'.format(market_url, req)
	preHash = '{}POST{}'.format(timestamp, req)
	creds = {'ACCESS-KEY': apiid, 'ACCESS-SIGN': sign(preHash, secret), 'ACCESS-TIMESTAMP': timestamp}
	response = requests.post(url, data=instrument, headers={**header_dict, **creds})
	return response


# version 3 not working
def place_order_v3(instrument):
	"""
	instrument = {"symbol":"ADA/USDT","price":"0.5","quantity":"10","direction":"1"}
	direction 1: buy, 2: sell
	"""
	body = json.dumps(instrument).replace(' ', '')
	req = '/api/v3/spot/order{}'.format(body)
	timestamp = now()
	url = '{}{}'.format(market_url, req)
	preHash = '{}POST{}'.format(timestamp, req)
	creds = {'ACCESS-KEY': apiid, 'ACCESS-SIGN': sign(preHash, secret), 'ACCESS-TIMESTAMP': timestamp}
	response = requests.post(url, data=instrument, headers={**header_dict, **creds})
	return response


# working fine
def get_closed_orders(symbol):
	"""
	symbol: 'ADA/USDT'
	"""
	href = '/api/v3/spot/closed_orders?instrument_id={}&latestOrderId='.format(symbol)
	url = market_url + href
	timestamp = now()
	creds = {'ACCESS-KEY': apiid, 'ACCESS-SIGN': sign(timestamp + 'GET' + href, secret), 'ACCESS-TIMESTAMP': timestamp}
	response = requests.get(url, headers={**header_dict, **creds})
	return response

def output(response):
	if response.status_code == 200:
		text = json.loads(response.text)
		if 'data' in text:
			result = text['data']
		else:
			result = text
	else:
		result = response.status_code
	return result

instrument = {"symbol": "ADA/USDT", "price": "0.5", "quantity": "10", "direction": "1", "clientId": apiid}
symbol = 'ADA/USDT'
# place_order_v3(instrument)
# place_order_v2(instrument)
# result = get_closed_orders(symbol)
# output(result)
