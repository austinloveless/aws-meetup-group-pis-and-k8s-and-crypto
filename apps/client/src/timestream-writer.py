import time, sys, boto3, pprint, requests
from botocore.config import Config
import settings

def createWriteClient(region, profile = None):
    print("Connecting to timestream ingest in region: ", region)
    config = Config()
    session = boto3.Session()
    client = session.client(service_name = 'timestream-write', region_name = region, config = config)
    return client

def describeTable(client, databaseName, tableName):
    response = client.describe_table(DatabaseName = databaseName, TableName = tableName)
    print("Table Description:")
    pprint.pprint(response['Table'])

def get_current_time():
    return str(int(round(time.time() * 1000)))

def writeRecords(symbol, client, dbName, tblName, price, trend):
  n = str(get_current_time())
  r = [{
    'MeasureValue': str(price),
    'MeasureName': 'price',
    'MeasureValueType': 'DOUBLE',
    'Dimensions': [
      {
        'Name': 'Symbol',
        'Value': symbol
      }
    ],
    'Time': n
  },
  {
    'MeasureValue': str(trend),
    'MeasureName': 'trend_hourly',
    'MeasureValueType': 'DOUBLE',
    'Dimensions': [
      {
        'Name': 'Symbol',
        'Value': symbol
      }
    ],
    'Time': n
  }]
  client.write_records(DatabaseName=dbName, TableName=tblName, Records=r, CommonAttributes={})

if __name__ == "__main__":
    try:
        tsClient = createWriteClient(settings.AWS_REGION)
        describeTable(tsClient, settings.DATABASE_NAME, settings.TABLE_NAME)
    except Exception as e:
        print(e)
        sys.exit(0)

    while True:
        quote = (requests.get(settings.API_HOST + '/current/' + settings.CRYPTO_SYMBOL).json())['quote']['USD']
        price = quote['price']
        trendHourly = quote['percent_change_1h']
        writeRecords(settings.CRYPTO_SYMBOL, tsClient, settings.DATABASE_NAME, settings.TABLE_NAME, price, trendHourly)
        time.sleep(30)


