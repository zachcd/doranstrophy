from django.shortcuts import render
from django.http import HttpResponse
from cassiopeia import riotapi
# Create your views here.


def index(request):
	#this will be a simple page to take summoner name input

def cards(request):
	if request.GET:
		riotapi.set_api_key("3ca655bb-959d-4ed3-ab2c-287da159aa59")
		getted = request.GET
		summoner = posted.get('summ')
		region = posted.get('region')
		riotapi.set_region(region)
		riotapi.get_summoner_by_name()