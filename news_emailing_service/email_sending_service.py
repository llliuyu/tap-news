import os
import sys
import yagmail

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

NEWS_LIMIT = 5
EMAIL_PUSHING_THRESHOLD = 0.35

NEWS_TABLE_NAME = 'news-test'
PREFERENCE_MODEL_TABLE_NAME = 'user_preference_model'


def pushingNews(user_id, user_preference):
	news = list(db[NEWS_TABLE_NAME].find({'class':user_preference}).sort([('publishedAt', -1)]).limit(NEWS_LIMIT))

	to = user_id
	subject = 'News you might like'
	html_front = '''\
				<html>
   				 	<style> .title{font-weight:bold;font-size:18px;} </style>
    				<body>
    					<img className='logo' src="https://image.ibb.co/kxwzzQ/logo.png" alt='logo' />'''
	html_end = '''
					</body>
				</html> '''
	html_mid = ''

	for item in news:
		news_title = item['title'];
		news_description = item['description']
		news_url = item['url']
		news_urlToImage = item['urlToImage']
		html_mid += '''

			<a className='list-group-item' href='''+news_url+'''>
                <div className='row'>
                    <div className='col s4 fill' style="float:left;">
                        <img src='''+news_urlToImage+''' alt='news' style="width="300px" height="200px"/>
                    </div>
                    <div className="col s8" style=" float:left;style="width="800px" height="200px"">
                        <h1>'''+news_title+'''</h1>
                        <div className="news-description">
                        <p><h2>'''+news_description+'''<h2></p>
                        </div>
                    </div>
                </div>
            </a>
		'''
	html = html_front + html_mid + html_end
	# print html
	yag.send(to = to, subject = subject, contents = [html])


if __name__ == '__main__':
	yag = yagmail.SMTP('tapnews503@gmail.com')

	db = mongodb_client.get_db()
	preferencesForAllUsers = list(db[PREFERENCE_MODEL_TABLE_NAME].find())
	for item in preferencesForAllUsers:
		preference = item['preference']
		print preference
		print item['userId']
		user_preference = ''
		user_id = ''
		num = 0
		for c,v in preference.items():

			if v > EMAIL_PUSHING_THRESHOLD:
				num += 1
				user_id = item['userId']
				user_preference = c
				pushingNews(user_id, user_preference)

		
