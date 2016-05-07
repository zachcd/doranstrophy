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
		try:
			summ = riotapi.get_summoner_by_name(summoner)
			pass
		except Exception, e:
			raise e
		masteries = riotapi.get_champion_masteries(summ)
		trophyChampions = {}
		count = 0
		#this sets up so that champions with lvl 4 or higher mastery but if less than 4 are found add more from lower lvls

		for champion, mastery in masteries:
			if mastery.level >= 4 :
				trophyChampions[champion] = mastery
				count = count + 1
		if count < 4:
			for champion, mastery in masteries:
			if mastery.level == 3 :
				trophyChampions[champion] = mastery

		displayChampions = []
		for c in trophyChampions:
			topKDA = 0
			kills = 0
			deaths = 0
			assists = 0
			wins = 0
			losses = 0
			matches = riotapi.get_match_list(summ,champion_ids = c, seasons=“SEASON2016”)
			for m in matches:
				data = riotapi.get_match(m)
				for player in data.participants:
					if player.summoner_name == summoner: #Build stats from this players participant object
						playerStats = player.stats
						topKDA = stats.kda if stats.kda > topKDA else topKDA
						kills += stats.kills
						deaths += stats.deaths
						assists += stats.assists
						if win:
							wins = win + 1
						else:
							losses = losses + 1

			championStats = {}
			championStats['topKDA'] = topKDA
			championStats['kills'] = kills
			championStats['deaths'] = deaths
			championStats['assists'] = assists
			championStats['wins'] = wins
			championStats['losses'] = losses
			displayChampions.append({'name':str(c), 'stats':championStats, 'mastery': masteries[c], 'masterypoint':masteries[c].points})
			displayChampions = sorted(displayChampions, key=itemgetter('masterpoints', reverse=True)


		return HttpResposne(render(request, 'cards.html', {'champions' : displayChampions}))