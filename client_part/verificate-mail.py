import requests


headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ4NzM0NjMzLCJqdGkiOiIzMDkyYzliODA3OWI0YWQ2YjVkMWZjYmU3YWZlMjVlNyIsInVzZXJfaWQiOjE5fQ.Z9egEE3DlhSxMMHZTFZbSmy32zE4WXjEM9VLXZlKVn0'}

endpoint = "http://127.0.0.1:8000/verificate/"
endpoint = "http://127.0.0.1:8000/check_code/"


data = {'code': 467191}

get_response = requests.post(endpoint, json=data, headers=headers)

print(get_response.json())