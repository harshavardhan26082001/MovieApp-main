from dataclasses import dataclass
import json
from django.forms.widgets import NullBooleanSelect
from django.shortcuts import render
from requests.sessions import session
from Movies.models import Movies as MoviesModel
from .forms import add_movie_form
from Movies.models import Movies as MovieModel
from tmdbv3api import TMDb, Discover,Account,Authentication
import requests
from django.http import HttpResponseRedirect
import random

apikey = '56db406e58392c2ff59a312e7368fc82'
session_delete_payload = []
img = 'http://image.tmdb.org/t/p/original/{your image poster path}'
tmdb = TMDb()
tmdb.api_key = apikey
account = Account()
auth = Authentication(username="harsha_amir",password="harsha2608")
details = account.details()

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.token
        return r


def getLatestMovies():
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    response = requests.get(url=url, headers=headers).json()
    return response["results"]


def getTopRatedMovies():
    url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    response = requests.get(url=url, headers=headers).json()
    return response["results"]


def getUpcomingMovies():
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    response = requests.get(url=url, headers=headers).json()
    return response["results"]


def getPopularMovies():
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    response = requests.get(url=url, headers=headers).json()
    return response["results"]

def getMovieIdfromMovieName(movie_name):
    url = "https://api.themoviedb.org/3/search/movie?query="+movie_name+"&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    response = requests.get(url=url, headers=headers).json()
    return response["results"][0]["id"]

def Movies(request):
    
    top_movies = ["Gravity", "Inception", "Interstellar", "Seven", "Lift"]
    movie_id = getMovieIdfromMovieName(random.choice(top_movies))
    recommended_movies = getRecommendedMoviesOrSeries(str(movie_id), "movie")
    latest_movies = getLatestMovies()
    toprated_movies = getTopRatedMovies()
    upcoming_movies = getUpcomingMovies()
    
    isLoggedIn = False
    if request.GET.get('request_token') and request.GET.get('approved') == 'true':
        isLoggedIn = True

    context = {
        'recommended_movies':recommended_movies,
        'latest_movies':latest_movies,
        'toprated_movies':toprated_movies,
        'upcoming_movies': upcoming_movies,
        'isLoggedIn': isLoggedIn,
    }
    return render(request, 'index.html',context)
    

def add_movie(request, movie_id):
    
    url = "https://api.themoviedb.org/3/account/"+account_id+"/watchlist"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    payload = {
        "media_type" : "movie",
        "media_id": movie_id, 
        "watchlist": True
    }
    
    response = requests.get(url=url, headers=headers, json=payload).json()
    
    context = {
        "AddedToWatchList" : True
    }
    
    return render(request, 'index.html',context)

def getSimilarMoviesOrSeries(movie_id, media_type):
    url="https://api.themoviedb.org/3/"+media_type+"/"+movie_id+"/similar?language=en-US&page=1"
    headers = {
        "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    
    response = requests.get(url=url, headers=headers).json()
    return response["results"]
    

def getRecommendedMoviesOrSeries(movie_id,media_type):
    url = "https://api.themoviedb.org/3/"+media_type+"/"+movie_id+"/recommendations?language=en-US&page=1"
    headers = {
        "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    
    response = requests.get(url=url, headers=headers).json()
    return response["results"]
    
    
def getCastInfo(movie_id, media_type):
    url = "https://api.themoviedb.org/3/"+media_type+"/"+movie_id+"/credits?language=en-US"
    headers = {
        "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    
    response = requests.get(url=url, headers=headers).json()
    actors = []
    cast = response["cast"]
    
    for member in cast:
        actors.append(member)
        
    return actors
        
    


def getTrailerfromMovieIdOrSeriesId(movie_id, media_type):
    url =  "https://api.themoviedb.org/3/"+media_type+"/"+movie_id+"/videos?language=en-US"
    headers = {
        "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    
    response = requests.get(url=url, headers=headers).json()
    trailer = ""
    
    try:
        trailer = response["results"][0]["key"]
    except:
        trailer = "Not available"
    return trailer


def movie_details(request, movie_id):
    
    url = "https://api.themoviedb.org/3/movie/"+movie_id+"?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"    
    }
    
    response = requests.get(url=url, headers=headers).json()
    
    media_type = "movie"
    
    
    # for similar movies
    similar_movies = getSimilarMoviesOrSeries(movie_id, media_type)
    
    # for recommended movies
    recommended_movies = getRecommendedMoviesOrSeries(movie_id, media_type)
    
    # this contains all the similar and recommended movies of the given movie.
    smlrobj = []
    
    for result in similar_movies:
        smlrobj.append(result)
    for result in recommended_movies:
        smlrobj.append(result)
        

    # cast information
    actors = getCastInfo(movie_id, media_type)
    
    # genre information
    genre = response["genres"]
    genres = []
    for i in genre:
        genres.append(i["name"])
    
    # year of release information
    datee = response["release_date"]
    datee = str(datee)[:4]

    # trailer/Video information
    trailer = getTrailerfromMovieIdOrSeriesId(movie_id, media_type)
    
    context = {
            'actors':actors,
            'trailer':trailer,
            'datee':datee,
            'genres':genres,
            'movobj': response,
            'smlrobj': smlrobj,
        }
    return render(request, '../templates/Movies/movie_details.html', context)

def search_details(request):
    
    searchinputMovieName = request.GET.get('searchinput')
    searchinputFromDate = request.GET.get('FromDate')
    searchinputToDate = request.GET.get('ToDate')
    searchIMDBRating = request.GET.get('IMDB')
    
    if searchinputMovieName:
        url = "https://api.themoviedb.org/3/search/multi?language=en-US&include_adult=true&page=1&query="+searchinputMovieName
    else:
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
        if searchinputFromDate:
            url += "&primary_release_date.gte="+searchinputFromDate
        if searchinputToDate:
            url += "&primary_release_date.lte="+searchinputToDate
        if searchIMDBRating:
            url += "&vote_average.gte="+searchIMDBRating

    bearerToken = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    
    Search_movie = requests.get(url=url, auth=BearerAuth(bearerToken), timeout=30).json()
    srchobjmovie = Search_movie["results"]
    context = {
            'srchobj': srchobjmovie
        }
    return render(request, '../templates/Movies/search_details.html', context)


#get the series details

def series_details(request, series_id):
    url = "https://api.themoviedb.org/3/tv/"+series_id+"?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"    
    }
    
    response = requests.get(url=url, headers=headers).json()
    
    media_type = "tv"
    # for similar series
    similar_series = getSimilarMoviesOrSeries(series_id, media_type)
    
    # for recommended series
    recommended_series = getRecommendedMoviesOrSeries(series_id, media_type)
    
    # this contains all the similar and recommended series of the given series.
    smlrobj = []
    
    for result in similar_series:
        smlrobj.append(result)
    for result in recommended_series:
        smlrobj.append(result)
        

    # cast information
    actors = getCastInfo(series_id, media_type)
    
    # genre information
    genre = response["genres"]
    genres = []
    for i in genre:
        genres.append(i["name"])
    
    # year of release information
    datee = response["first_air_date"]
    datee = str(datee)[:4]

    # trailer/Video information
    trailer = getTrailerfromMovieIdOrSeriesId(series_id, media_type)
    
    context = {
            'actors':actors,
            'trailer':trailer,
            'datee':datee,
            'genres':genres,
            'movobj': response,
            'smlrobj': smlrobj,
        }
    return render(request, '../templates/Movies/series_details.html', context)



def login(request):

    uname = request.GET.get('username')
    pwd = request.GET.get('password')
    
    url = 'https://api.themoviedb.org/3/authentication/token/new'
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"    
    }

    response = requests.get(url, headers=headers).json()
    if response["success"]:
        REQUEST_TOKEN = response["request_token"]
    
    session_payload = { 
        "request_token": REQUEST_TOKEN
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    
    response = HttpResponseRedirect('https://www.themoviedb.org/authenticate/'+REQUEST_TOKEN+'?redirect_to=http://127.0.0.1:8080/')
    
    SESSION_ID = requests.post('https://api.themoviedb.org/3/authentication/session/new',headers=headers, json=session_payload).json() 
    
    if SESSION_ID["success"]:
        session_delete_payload = {  "session_id":  SESSION_ID["session_id"]   }

    return response

def register(request):
    url = 'https://api.themoviedb.org/3/authentication/token/new'
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"    
    }

    response = requests.get(url, headers=headers).json()
    if response["success"]:
        REQUEST_TOKEN = response["request_token"]
    
    session_payload = { 
        "request_token": REQUEST_TOKEN
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    
    response = HttpResponseRedirect('https://www.themoviedb.org/authenticate/'+REQUEST_TOKEN+'?redirect_to=http://127.0.0.1:8080/')
    
    SESSION_ID = requests.post('https://api.themoviedb.org/3/authentication/session/new',headers=headers, json=session_payload).json() 
    
    if SESSION_ID["success"]:
        session_delete_payload = {  "session_id":  SESSION_ID["session_id"]   }

    return response

def logout(request):
    
    
    #url = "localhost:8000"
    #requests.post(url, data=session_payload)
    
    #params={key: value}
    #requests.delete(url, params={key: value}, args)
    
    # This implementation is incomplete, will be fixed in next version.
    delete_response = {
        "success" : True,
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmRiNDA2ZTU4MzkyYzJmZjU5YTMxMmU3MzY4ZmM4MiIsInN1YiI6IjYwYTdiM2QxZTE2ZTVhMDAzZjg4YjRiZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DKsQVBkJLd5QbZklzb9mCh1hQbskzZ3K3AjLgCdLJZ4"
    }
    
    if session_delete_payload:
        delete_response = requests.delete('https://api.themoviedb.org/3/authentication/session',headers=headers, json=session_delete_payload).json()
    
    # it takes by defualt success.
    if(delete_response["success"]):
        return HttpResponseRedirect('http://127.0.0.1:8080') 
    else:
        return HttpResponseRedirect(request.path_info)
