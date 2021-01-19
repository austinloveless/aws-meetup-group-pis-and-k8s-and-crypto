import random, time, sys, argparse, boto3, pprint
from botocore.config import Config
import requests

def createWriteClient(region, profile = None):
    if profile == None:
        print("Using credentials from the environment")

    print("Connecting to timestream ingest in region: ", region)
    config = Config()
    if profile != None:
        session = boto3.Session(profile_name = profile)
        client = session.client(service_name = 'timestream-write',
                                region_name = region, config = config)
    else:
        session = boto3.Session()
        client = session.client(service_name = 'timestream-write',
                                region_name = region, config = config)
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
  client.write_records(DatabaseName=dbName, TableName=tblName,
                                              Records=r, CommonAttributes={})

#########################################
######### Main ##########
#########################################
if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog = 'TimestreamSampleContinuousDataIngestorApplication', description='Execute a example application generating and ingesting time series data.')

    parser.add_argument('--database-name', '-d', dest="databaseName", action = "store", required = True, help = "The database name in Amazon Timestream - must be already created.")
    parser.add_argument('--table-name', '-t', dest="tableName", action = "store", required = True, help = "The table name in Amazon Timestream - must be already created.")
    parser.add_argument('--endpoint', '-e', action = "store", required = True, help="Specify the service region endpoint. E.g. 'us-east-1'")
    parser.add_argument('--symbol', '-s', action = "store", required = True, help="Specify symbol to get data for")
    parser.add_argument('--host', '-ho', action = "store", required = True, help="Specify host used to get data")
    
    args = parser.parse_args()
    print(args)

    ## Verify the table
    try:
        tsClient = createWriteClient(args.endpoint)
        describeTable(tsClient, args.databaseName, args.tableName)
    except Exception as e:
        print(e)
        sys.exit(0)

    while True:
        quote = (requests.get(args.host + '/current/' + args.symbol).json())['quote']['USD']
        price = quote['price']
        trendHourly = quote['percent_change_1h']
        writeRecords(args.symbol, tsClient, args.databaseName, args.tableName, price, trendHourly)
        time.sleep(30)


