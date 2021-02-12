import datetime
import hashlib
import hmac
import json
import urllib
import requests

def request_nosign_get(url, dic):
    header_dict = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko", \
                   "Content-Type": "application/json;charset=utf-8", "Connection": "keep-alive", \
                   "Cookie": "locale=zh_CN"}
    return http_request(url, data=dic, header_dict=header_dict, reqtype='GET')
def request_sign_get(url, dic):
    header_dict = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko", \
                   "Content-Type": "application/json;charset=utf-8", "Connection": "keep-alive", \
                   "Cookie": "locale=zh_CN"}
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    header_dict['ACCESS-KEY'] = dic['apiid']
    header_dict['ACCESS-TIMESTAMP'] = timestamp
    requestURI = dic['requestURI']
    secret = dic['secret']
    del dic['requestURI']
    del dic['secret']
    del dic['apiid']
    method = 'GET'
    data = ""
    if len(dic) > 0:
        data = "?" + urllib.parse.urlencode(dic)
    message = timestamp + method + requestURI + data
    mysign = sign(message=message, secret=secret)
    header_dict['ACCESS-SIGN'] = mysign

    url = url + data
    return http_request(url, data=None, header_dict=header_dict, reqtype='GET')
def request_sign_post(url, dic):
    header_dict = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko", \
                   "Content-Type": "application/json;charset=utf-8", "Connection": "keep-alive", \
                   "Cookie": "locale=zh_CN"}
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    header_dict['ACCESS-KEY'] = dic['apiid']
    header_dict['ACCESS-TIMESTAMP'] = timestamp
    requestURI = dic['requestURI']
    secret = dic['secret']
    del dic['requestURI']
    del dic['secret']
    del dic['apiid']
    method = 'POST'
    data = json.dumps(dic)
    message = timestamp + method + requestURI + data
    mysign = sign(message=message, secret=secret)
    header_dict['ACCESS-SIGN'] = mysign
    return http_request(url, data=dic, header_dict=header_dict)
def http_request(url, data, header_dict, reqtype='POST'):
    if reqtype == 'GET':
        reponse = requests.get(url, params=data, headers=header_dict)
    else:
        reponse = requests.post(url, data=json.dumps(data), headers=header_dict)
    try:
        if reponse.status_code == 200:
            return json.loads(reponse.text)
        else:
            return None
    except Exception as e:
        print('http failed : %s' % e)
        return None
def sign(message, secret):
    """
    这里进行签名
    :param message: message wait sign
    :param secret:  secret key
    :return:
    """
    secret = secret.encode('utf-8')
    message = message.encode('utf-8')
    sign = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()
    return sign
class ExchangeClient:
    """
        client for CoinBene exchange ,include functions of  account ,market ,trade operations
        """

    def __init__(self, apiid, secret):
        self.apiid = apiid
        self.secret = secret
        self.base_url = 'http://openapi-exchange.coinbene.com'

    def _gen_parameter(self):
        """
        gen common info for sign
        :return:
        """
        dic = {'apiid': self.apiid, 'secret': self.secret}
        return dic

    def trade_pair_list(self):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/market/tradePair/list"
        dic['requestURI'] = requrl
        url = self.base_url + requrl
        return request_nosign_get(url, dic)

    def trade_pair_one(self, symbol):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/market/tradePair/one"
        dic['requestURI'] = requrl
        dic['symbol'] = symbol
        url = self.base_url + requrl
        return request_nosign_get(url, dic)

    def order_book(self, symbol, depth):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/market/orderBook"
        dic['requestURI'] = requrl
        dic['symbol'] = symbol
        dic['depth'] = depth
        url = self.base_url + requrl
        return request_nosign_get(url, dic)

    def ticker_one(self, symbol):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/market/ticker/one"
        dic['requestURI'] = requrl
        dic['symbol'] = symbol
        url = self.base_url + requrl
        return request_nosign_get(url, dic)

    def market_trades(self, symbol):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/market/trades"
        dic['requestURI'] = requrl
        dic['symbol'] = symbol
        url = self.base_url + requrl
        return request_nosign_get(url, dic)

    def account_list(self):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/account/list"
        dic['requestURI'] = requrl
        url = self.base_url + requrl
        return request_sign_get(url, dic)

    def account_one(self, asset):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/account/one"
        dic['requestURI'] = requrl
        dic['asset'] = asset
        url = self.base_url + requrl
        return request_sign_get(url, dic)

    def order_place(self, symbol, direction, price, quantity, orderType, notional, clientId):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/order/place"
        dic['requestURI'] = requrl
        dic['symbol'] = symbol
        dic['direction'] = direction
        if price is not None:
            dic['price'] = price
        if quantity is not None:
            dic['quantity'] = quantity
        dic['orderType'] = orderType
        if notional is not None:
            dic['notional'] = notional
        if clientId is not None:
            dic['clientId'] = clientId
        url = self.base_url + requrl
        return request_sign_post(url, dic)

    def open_orders(self, symbol, latestOrderId):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/order/openOrders"
        dic['requestURI'] = requrl
        if symbol is not None:
            dic['symbol'] = symbol
        if latestOrderId is not None:
            dic['latestOrderId'] = latestOrderId;
        url = self.base_url + requrl
        return request_sign_get(url, dic)

    def close_orders(self, symbol, latestOrderId):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/order/closedOrders"
        dic['requestURI'] = requrl
        if symbol is not None:
            dic['symbol'] = symbol
        if latestOrderId is not None:
            dic['latestOrderId'] = latestOrderId;
        url = self.base_url + requrl
        return request_sign_get(url, dic)

    def order_info(self, orderId):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/order/info"
        dic['requestURI'] = requrl
        dic['orderId'] = orderId
        url = self.base_url + requrl
        return request_sign_get(url, dic)

    def trade_fills(self, orderId):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/order/trade/fills"
        dic['requestURI'] = requrl
        dic['orderId'] = orderId
        url = self.base_url + requrl
        return request_sign_get(url, dic)

    def order_cancel(self, orderId):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/order/cancel"
        dic['requestURI'] = requrl
        dic['orderId'] = orderId
        url = self.base_url + requrl
        return request_sign_post(url, dic)

    def batch_cancel(self, orderIds):
        dic = self._gen_parameter()
        requrl = "/api/exchange/v2/order/batchCancel"
        dic['requestURI'] = requrl
        dic['orderIds'] = orderIds
        url = self.base_url + requrl
        return request_sign_post(url, dic)

apiid = 'won't tell you'
secret = 'sorry'
client = ExchangeClient(apiid, secret)
order = client.order_place(symbol="ADA/USDT", direction=1, price=0.5, quantity=10, orderType=1, notional="", clientId="test")
cancel = client.order_cancel('some_order_id')
order = client.order_place("ADA/USDT", 1, 0.5, 10, 1, "", "test")
open_orders = client.open_orders("ADA/USDT", latestOrderId="")
open_order_ids = [order['orderId'] for order in open_orders['data']]
result = client.batch_cancel(open_order_ids)
print(result)

