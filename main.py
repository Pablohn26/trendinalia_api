#!/usr/bin/python3
from __future__ import unicode_literals
from flask import Flask
from flask_restx import Api, Resource, fields
from bs4 import BeautifulSoup
import requests
import datetime

## Trendinalia Base URL
base_url = "https://www.trendinalia.com/twitter-trending-topics/"

## Country to get the hashtags
country = "globales"

## Date to get the hashtags
date = datetime.date.today() - datetime.timedelta(days=1)
date = date.strftime("%y%m%d")

url = "https://www.trendinalia.com/twitter-trending-topics/"+country+"/"+country+"-"+date+".html"



app = Flask(__name__)
api = Api(app, version='1.0', title='Trendinalia API',
    description='A simple Trendinalia API',
)


ns_top = api.namespace('top', description='Top Trending Topics of a day')


metadata_model = api.model("metadata", {
    'country': fields.String(description='name of the country you want the top hashtags'),
    'day': fields.String(description='day you want the top hashtags. Format YYMMDD. Default yesterday')
})

hashtag_content_model = api.model("HashtagContent", {
    'name': fields.String(description='Name of the hashtag that day in that country'),
    'time': fields.String(description='Time as Trending Topic of the name hashtag that day in that country')
})

hashtag_model = api.model('Hashtag', {
          "number": fields.Integer(required=True, description='Rank of the hashtag that day in that country'),
          "hashtag": fields.List(fields.Nested(hashtag_content_model))
})



response_model = api.model("Result", {
    'metadata': fields.List(fields.Nested(metadata_model)),
    'hashtags': fields.List(fields.Nested(hashtag_model))
})



todo = api.model('Top', {
    'country': fields.String(description='name of the country you want the top hashtags'),
    'day': fields.String(description='day you want the top hashtags. Format YYMMDD. Default yesterday'),
})

class Top_DAO(object):
    def __init__(self):
        self.metadata = [{'country': country, 'day': date}]
        self.hashtags = []

    def get(self, date, country):
        '''Get all hashtags of yesterday globally'''
        # Getting the webpage, creating a Response object.
        response = requests.get(url)
        if response.status_code == 404:
            api.abort(404, "Data for country {} and date {} don't exist".format(country,date))
        
        # Extracting the source code of the page.
        data = response.text
        
        # Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
        soup = BeautifulSoup(data, 'lxml')
        # Extracting all the <tr> tags into a list.
        table = soup.find('table').find('tbody')
        rows  = table.find_all('tr')
        
        for row in rows:
            fila = row.find_all('td')
            self.hashtags.append({'number': fila[0].get_text(), 'hashtag': {'name': fila[1].get_text(), 'time': fila[2].get_text()}})
        
        return self

    def post(self):
        api.abort(405)
    def delete(self):
        api.abort(405)
    def put(self):
        api.abort(405)

DAO = Top_DAO()


@ns_top.route('/')
class TodoList(Resource):
    '''Shows a list of all methods'''
    @ns_top.doc(params={'country': 'Name of the country. Default: global (globales)','day': 'Date you want to look for. Default yesterday ({})'.format(date)})
    @ns_top.marshal_list_with(response_model)
    @api.response(200, 'Success')
    @api.response(404, 'Trending Topic data not found')
    def get(self):
        '''List all hashtags of yesterday globally'''
        return DAO.get(date,country)
    @api.response(405, 'Method Not Allowed')
    def post(self, id):
        '''Method Not Allowed'''
        return DAO.post()
    @api.response(405, 'Method Not Allowed')
    def delete(self, id):
        '''Method Not Allowed'''
        return DAO.delete()
    @api.response(405, 'Method Not Allowed')
    def put(self, id):
        '''Method Not Allowed'''
        return DAO.put()



if __name__ == '__main__':
    app.run(debug=True)


