import requests
import os

api_key = os.environ['API_KEY']
key_sec = os.environ['KEY_ONE']

class SearchMovie():
    def __init__(self, query):

        self.results_list = []
        self.url = 'https://api.themoviedb.org/3/search/movie'
        self.param = {
            'api_key': api_key,
            'query': query
        }
        self.base_img_url = 'https://image.tmdb.org/t/p/w500'
        self.res = requests.get(self.url, self.param)
    
    def search(self):
        i = 0
        for movie in self.res.json()['results']:
            self.results_list.append({
                'title': movie['original_title'],
                'year': movie['release_date'],
                'id': movie['id'],
                
            })
            i+=1

class MovieDetails():
    def __init__(self, movie_id):
        self.url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        self.param = {
            'api_key': api_key,
        }
        self.base_img_url = 'https://image.tmdb.org/t/p/w500'
        self.res = requests.get(self.url, self.param)
        self.result = {
            'title': self.res.json()['original_title'],
            'sum': self.res.json()['overview'],
            'year': self.res.json()['release_date'][:4],
            'img_url': self.base_img_url + str(self.res.json()['poster_path']) 
        }
    
