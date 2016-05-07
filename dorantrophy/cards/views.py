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
		summ = riotapi.get_summoner_by_name(summoner)
		masteries = riotapi.get_champion_masteries(summ)
		champstouse = {}
		count = 0
		#this sets up so that champions with lvl 4 or higher mastery but if less than 4 are found add more from lower lvls
		for champion, mastery in masteries:
			if mastery.level >= 4 :
				champstouse[champion] = mastery
				count = count + 1
		if count < 4:
			for champion, mastery in masteries:
			if mastery.level == 3 :
				champstouse[champion] = mastery
