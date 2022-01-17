# TradeHelper

From within project directory:<br />

Build and start : $ docker-compose up -d --build<br />
Live logs : $ docker-compose logs -f<br />
Stop : $ docker-compose down<br />

First time running?<br />
 $ docker-compose exec backend aerich init-db<br />
 Success create app migrate location migrations/models<br />
 Success generate schema for app "models"<br />
 
 Made changes to the models?<br />
 $ docker-compose exec backend aerich migrate<br />
 $ docker-compose exec backend aerich upgrade<br />

Want a python interpreter?<br />
 $ docker exec -it backend ipython<br />
Want to connect to db?<br />
 $ docker-compose exec db psql --username=postgres_user --dbname=db<br />

<br />

 !! YOU must manully create your own .env file for the following services...or adding them do docker-compose.yml environment:
  
/backend/.env:<br />
  POSTGRES_USER=postgres_user<br />
  POSTGRES_PASSWORD=some_password<br />
  POSTGRES_DB=db<br />
  SECRET_KEY=some_secret_key<br />
 
 /db/.env:<br />
  POSTGRES_USER=postgres_user<br />
  POSTGRES_PASSWORD=some_password<br />
  POSTGRES_DB=db<br />
  
 /notifier/.env:<br />
  TELEGRAM_CHAT_ID=some_number<br />
  TELEGRAM_TOKEN=some_code<br />


/scheduler/.env:<br />
  BINANCE_API_KEY=some_code<br />
  BINANCE_API_SECRET=some_secret<br />
  HUEY_DB=/tmp/huey.db<br />

* secret keys can be generated with : openssl rand -hex 32
