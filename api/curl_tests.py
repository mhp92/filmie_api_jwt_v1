'''

Setup WatchlistViewSet / permission_classes = [IsAuthenticated]

curl http://127.0.0.1:8000/router/watchlist/ --> won't work because token is not provided

    Testing inside the terminal:
    Step 1:
        curl -X POST -d "name=admin&password=password" http://127.0.0.1:8000/api/auth/token/

        token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozMjUsInVzZXJuYW1lIjoiYWRtaW5AYWRtaW4uY29tIiwiZXhwIjoxNTUwODQ4MjU1LCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSJ9.CXq-gldrPfj09NTvNHNkBofsR6L2E1PvCkVvpzK6UZw

    pass this token inside --> curl -H "Authorization: JWT <your_token>" http://localhost:8000/protected-url/

        curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozMjUsInVzZXJuYW1lIjoiYWRtaW5AYWRtaW4uY29tIiwiZXhwIjoxNTUwODQ4OTQwLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSJ9.kZs8uy3VdMyumZBIUdiaGmfv2VLyoZHt8_CcZ0UHwtQ" http://127.0.0.1:8000/router/watchlist/

        only passing in the token allows you to get the JSON Data. (Also token expires after ending the session?)
'''

'''

token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUxMDM1MjI0LCJqdGkiOiJmZTEyMWM2OWI3ZDE0MzI3OTAzNTliNTJhY2Y3OTUxNyIsInVzZXJfaWQiOjMyNX0.vcXl-PrDuHAHWdOhr4jf0zHVoQJxcT0n_mdXxRCVqx4

inser token here: curl -H "Authorization: JWT <token>" http://127.0.0.1:8000/router/watchlist/

paste in terminal: curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUxMDM1MjI0LCJqdGkiOiJmZTEyMWM2OWI3ZDE0MzI3OTAzNTliNTJhY2Y3OTUxNyIsInVzZXJfaWQiOjMyNX0.vcXl-PrDuHAHWdOhr4jf0zHVoQJxcT0n_mdXxRCVqx4" http://127.0.0.1:8000/router/watchlist/