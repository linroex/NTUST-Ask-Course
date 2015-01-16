import requests
import pyelasticsearch as pyes

class Facebook():
    def __init__(self, appId = '', appSecret = ''):
        self.appId = appId
        self.appSecret = appSecret
    def setAccessToken(self, accessToken):
        self.accessToken = accessToken
    def api(self, path, fields = [], limit = 10,method = 'get'):
        response = ''
        if method == 'get':
            response = requests.get(self.getRequestUrl(path, fields, limit))
        return response.json()
    def getRequestUrl(self, path, fields, limit = 10):
        return 'https://graph.facebook.com/v2.2/{path}?fields={fields}&limit={limit}&access_token={accessToken}'.format(path = path.strip(), fields = ",".join(fields), limit = limit, accessToken = self.accessToken)

def parseFacebookGroupsPosts(posts):
    for post in posts:
        # post['from']['name']
        # post['comments']['data'][0]
        # posts['paging']['next']
        
        try:
            dbPost = es.get('ntustask','ntusttalktalk', post['id'])
            
            if dbPost['_source']['updated_time'] == post['updated_time']:
                continue

        except pyes.exceptions.ElasticHttpNotFoundError:
            pass

        es.index('ntustask','ntusttalktalk', post, id = post['id'])        

        # es.delete_all('ntustask','ntusttalktalk')

token = ''
fields = ['from','message','comments','created_time']
fb = Facebook()
fb.setAccessToken(token)

posts = fb.api('167003826794033/feed', fields, 200)

es = pyes.ElasticSearch('http://localhost:9200/')

parseFacebookGroupsPosts(posts['data'])

setup = False

if setup:
    while True:
        try:
            parseFacebookGroupsPosts(posts['data'])
            nextPageUrl = posts['paging']['next']
            posts = requests.get(nextPageUrl).json()
        except KeyError:
            break

print('Done')
