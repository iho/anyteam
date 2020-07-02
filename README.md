# anyteam

## How to run
1. `cp .env.example .env`
2. Paste your Binance apis
3. Run `docker-compose up`

To check if service working properly run: 

 ```
 curl --header "Content-Type: application/json" \
      --request POST \
      --data '{ "in_currency": "BTC", "out_currency": "USDT", "in_amount": "2"}' \
      http://localhost:8000/calc/
```
