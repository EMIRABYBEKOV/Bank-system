import requests


headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ4NzM0NjMzLCJqdGkiOiIzMDkyYzliODA3OWI0YWQ2YjVkMWZjYmU3YWZlMjVlNyIsInVzZXJfaWQiOjE5fQ.Z9egEE3DlhSxMMHZTFZbSmy32zE4WXjEM9VLXZlKVn0'}

endpoint = f"http://127.0.0.1:8000/verificate/"
endpoint = "http://127.0.0.1:8000/check_code/"


data = {'code': 467191}

# get_response = requests.post(endpoint, json=data, headers=headers)
# print(get_response.json())
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
#
# # now = str(date.today())
# now = '1/1/2022'
# date_format = '%d/%m/%Y'
# dtObj = datetime.strptime(now, date_format)
# month = 20
#
# future_date = dtObj + relativedelta(month=month)
#
# print(future_date)

print(datetime.now().strftime('%d/%m/%Y'))
date_after_month = datetime.today()+ relativedelta(months=30, days=5)
print('After Month:', date_after_month.strftime('%d/%m/%Y'))


print(datetime.today() - datetime.today())