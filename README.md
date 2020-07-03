# anyteam

## How to run
```docker-compose up```

To check if service working properly run: 

 ```
 curl --header "Content-Type: application/json" \
      --header "Sign: 1a40d06367165e81feb61b07e07f21e70ae7b4d63fda3fa127194ec3bdfae87bce14948fc2ac60d3f2fe8f47e01bf9df71518299aae6f9abaa05181e8de25fa3" \
      --request POST \
      --data '{ "in_currency": "BTC", "out_currency": "USDT", "in_amount": "2"}' \
      http://localhost:8000/calc/
```
