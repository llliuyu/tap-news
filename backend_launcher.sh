#! /bin/bash
fuser -k 3000/tcp
fuser -k 4040/tcp
fuser -k 5050/tcp
fuser -k 6060/tcp

#service redis_6379 start
#pip install -r requirements.txt
cd ./backend_server
python service.py &
cd ../news_recommendation_service
python click_log_processor.py &
python recommendation_service.py &
cd ../news_topic_modeling_service/server
python server.py &

echo“====================================”
read -p "PRESS [ENTER] TO TERMINATE PROCESSES" PRESSKEY

fuser -k 3000/tcp &
fuser -k 4040/tcp &
fuser -k 5050/tcp &
fuser -k 6060/tcp 
#service redis_6379 stop