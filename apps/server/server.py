from flask import Flask, json, Response
from flask_caching import Cache  
import requests, argparse

api = Flask(__name__)
api.config['CACHE_TYPE'] = 'simple'
api.cache = Cache(api) 

@api.cache.cached(timeout=60, key_prefix="current_prices")
def getCachedPrices():
	print('getting prices')
	return requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=5000', headers = {'X-CMC_PRO_API_KEY': args.apiKey}).json()
	
@api.route('/current/<symbol>', methods=['GET'])
def get_prices(symbol):
	prices = getCachedPrices()
	output = [x for x in prices['data'] if x['symbol'] == symbol.upper()]
	if len(output) == 0:
		return Response(json.dumps({'error': symbol + ' not found'}), 404, mimetype='application/json')
	else:	
		return Response(json.dumps(output[0]), mimetype='application/json')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog = 'AWSMeetupGroupCrytoTimestreamWriter', description='Get data from server and write to Timestream database')
    parser.add_argument('--api-key', '-k', dest="apiKey", action = "store", required = True, help = "API Key to call CoinMarketCap")
	api.run()

