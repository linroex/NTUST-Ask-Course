#!/usr/bin/python3
import pyelasticsearch as pyes
from flask import Flask, json
from flask.ext import restful
from flask.ext.restful import reqparse

app = Flask(__name__)
api = restful.Api(app)

class APIControl(restful.Resource):
    def get(self):
        es = pyes.ElasticSearch('http://localhost:9200')

        parser = reqparse.RequestParser()
        
        parser.add_argument('keyword', type=str)

        args = parser.parse_args()
        # keyword = " AND ".join([str(arg) for arg in args.values() if arg != None])
        keyword = args['keyword']

        query = {'query':{'multi_match':{'type':'phrase','query':keyword,'fields':['comments.data.message','message'], 'operator':'OR'}},'sort':{'created_time':'desc'}}
        result = es.search(query, index = 'ntustask', doc_type = 'ntusttalktalk', size = 10)
        return json.jsonify(result['hits'])
            

api.add_resource(APIControl, '/')

if __name__ == '__main__':
    app.run()
