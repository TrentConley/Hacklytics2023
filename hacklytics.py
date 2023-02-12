from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import datetime
import time
import config

key = config.API_KEY
url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/historical'


def get_data_for_date(date, key = key, url = url):
	parameters = {
	  'date' : date,
	  'start':'1',
	  'limit':'5000',
	  'convert':'USD'
	}
	headers = {
	  'Accepts': 'application/json',
	  'X-CMC_PRO_API_KEY': key,
	}

	session = Session()
	session.headers.update(headers)

	try:
		response = session.get(url, params=parameters)
		data = json.loads(response.text)
		print(data['data'][0]['quote']['USD']['percent_change_24h'])
	  # print(data)
	except (ConnectionError, Timeout, TooManyRedirects) as e:
	  print(e)
  

# date = datetime.datetime(2023, 2, 10)
# unix_timestamp = int(date.timestamp())
# Get current time
current_time = int(time.time())

# get_data_for_date(time)



def write_to_csv():
	# Define a list to store the data
	data = []

	# Get the data for the past 365 days (1 year)
	for i in range(365):
		try:
			# Get the date for each day in the past 365 days
			date = current_time - (i * 24 * 60 * 60)
			# Call the get_data_for_date function with the date
			data_for_date = get_data_for_date(date)
			# Append the data to the list
			data.append(data_for_date)
		except (json.decoder.JSONDecodeError) as e:
			print(e)

	# Create a pandas data frame with the data
	df = pd.DataFrame(data)

	# Save the data frame to a csv file
	df.to_csv('data.csv', index=False)