import requests 

headers = {}
headers['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUxMDQyMjk5LCJqdGkiOiIyYmQ4Yjg3MGM0MWI0OGY2OTIzYmVmNTNlNTNkYWFkYyIsInVzZXJfaWQiOjMyNX0.lj5PreKS3Liv06J3albz9SJnzfeNfGEqx8adSX5qWU0'

url = 'http://127.0.0.1:8000/router/watchlist/?type_id=1' 

r = requests.get(url, headers=headers)

print(r.text)


'''

In terminal cd to api $ python send.py 

get access and refresh token:
http post http://127.0.0.1:8000/api/token/ email=vitor password=password

first request with access token:
http http://127.0.0.1:8000/router/watchlist/?type_id=1 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUxMDQzNTM3LCJqdGkiOiJhZWY5NGJjNTJiNjk0NTE5OTM1NGRjZjI2NzJjYTE0NyIsInVzZXJfaWQiOjMyNX0.7f12pwXFshYFfsc4rNwAuvVP2ZiKH8yCqt7ZtWgSaOY'

get next access token with the refresh token
http post http://127.0.0.1:8000/api/token/refresh/ refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU1MTEyODM5OSwianRpIjoiMDliZmI2OWM2YWFjNGU0Mjk4Y2MyMjc4ZTM2NjdiZjIiLCJ1c2VyX2lkIjozMjV9.aOdzVlhFtvTz7nwOAON_FBC3ONOJfuNufmJujFjv5LQ

'''
