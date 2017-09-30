cd /var/lib/jenkins/workspace/tap-news/web_server/server
npm start &
cd /var/lib/jenkins/workspace/tap-news/backend_server
python service.py &
cd /var/lib/jenkins/workspace/tap-news/news_recommendation_service
python recommendation_service.py &
python click_log_processor.py &
cd /var/lib/jenkins/workspace/tap-news/news_topic_modeling_service/server
python server.py