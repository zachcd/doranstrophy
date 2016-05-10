from django.shortcuts import render
from django.http import HttpResponse
from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
from django.http import HttpResponseRedirect, JsonResponse
from operator import itemgetter
import math
import json
# Create your views here.


def index(request):
	#this will be a simple page to take summoner name input
	print("shit I fucked up")
	return HttpResponse(render(request, 'doransindex.html',))

def load(request):
	riotapi.set_api_key("3ca655bb-959d-4ed3-ab2c-287da159aa59")
	riotapi.set_rate_limits((1500, 10), (90000, 600))
	getted = request.GET
	summoner = getted.get('summ')
	region = getted.get('region')
	riotapi.set_region(region)
	#riotapi.print_calls(True)
	try:
		summ = riotapi.get_summoner_by_name(summoner)
	except APIError:
		return HttpResponseRedirect('/dorans/')
	masteries = riotapi.get_champion_masteries(summ)
	trophyChampions = {}
	count = 0
	#this sets up so that champions with lvl 4 or higher mastery but if less than 4 are found add more from lower lvls

	for champion, mastery in masteries.items():
		if mastery.level >= 4 :
			trophyChampions[champion] = mastery
			count = count + 1
	if count < 4:
		for champion, mastery in masteries.items():
			if mastery.level == 3 :
				trophyChampions[champion] = mastery
	displayChampions = []
	summid = riotapi.get_summoner_by_name(summoner).id
	for c in trophyChampions:
		print(c)
		topKDA = 0
		kills = 0
		deaths = 0
		assists = 0
		wins = 0
		losses = 0
		MVP = 0
		try:
			matches = riotapi.get_match_list(summ,champions = c, seasons="SEASON2016")
		except APIError:
			matches = riotapi.get_match_list(summ,champions = c, seasons="SEASON2016")
		if not matches:
			continue
		for m in matches:
			try:
				data = riotapi.get_match(m, include_timeline = False)
			except APIError:
				continue
			teamtotal = 0
			tgold = 0
			tdamagedlt = 0
			tdamagetkn = 0
			twards = 0
			twardkls = 0
			for player in data.participants:
				if player.summoner_id == summid: #Build stats from this players participant object
					i = 0
					if player.side.name == 'blue':
						for p in data.participants:
							i +=1
							if i < 5:
								teamtotal += p.stats.kills
								tgold += p.stats.gold_earned
								tdamagedlt +=  p.stats.damage_dealt_to_champions
								tdamagetkn +=  p.stats.damage_taken
								twards +=  p.stats.wards_placed
					else:
						for p in data.participants:
							i += 1
							if i >= 5:
								teamtotal += p.stats.kills
								tgold += p.stats.gold_earned
								tdamagedlt +=  p.stats.damage_dealt_to_champions
								tdamagetkn +=  p.stats.damage_taken
								twards +=  p.stats.wards_placed
					if teamtotal == 0 :
						teamtotal = 1;
					if twards == 0:
						twards == 1;
					topKDA = player.stats.kda if player.stats.kda > topKDA else topKDA
					kills += player.stats.kills
					deaths += player.stats.deaths
					assists += player.stats.assists
					trip = player.stats.triple_kills
					quad = player.stats.quadra_kills
					penta = player.stats.penta_kills
					kp = player.stats.kills/teamtotal
					g = player.stats.gold_earned/tgold
					cs = player.stats.cs/data.duration.seconds
					dmgdlt = player.stats.damage_dealt_to_champions/tdamagedlt
					dmgtkn = player.stats.damage_taken/tdamagetkn
					try:
						wards = player.stats.wards_placed/twards
					except ZeroDivisionError:
						wards = 0
					kda = player.stats.kda
					if kda == 1:
						kda = 1.1
					if kda == 0:
						try:
							kda = .01/p.stats.deaths
						except ZeroDivisionError:
							kda = .1
					if p.timeline.role.name ==  'solo':
						if p.timeline.lane.name == 'mid_lane': #mid
							MVP += math.log(kda)/math.log(6) * ((kp * 10)+(g * 5)+(cs * .7)+ (dmgdlt * 12) + (dmgtkn * -1) + (wards *4)  ) + trip * .25 + quad * .5 + penta * 1
						else:
							#print(math.log(kda)/math.log(6) * ((kp * 10)+(g * 5)+(cs * .7)+ (dmgdlt * 7) + (dmgtkn * 7) + (wards *4)  ))
							MVP += math.log(kda)/math.log(6) * ((kp * 10)+(g * 5)+(cs * .7)+ (dmgdlt * 7) + (dmgtkn * 7) + (wards *4)  ) + trip * .25 + quad * .5 + penta * 1
					elif p.timeline.role.name == 'carry':# carry
						#print(math.log(kda)/math.log(6) * ((kp * 10)+(g * 6)+(cs * .7)+ (dmgdlt * 12) + (dmgtkn * 1) + (wards *1)  ))
						MVP += math.log(kda)/math.log(6) * ((kp * 10)+(g * 5)+(cs * .7)+ (dmgdlt * 12) + (dmgtkn * -1) + (wards *4)  )+ trip * .25 + quad * .5 + penta * 1
					elif p.timeline.role.name == 'support': #supp
						#print(math.log(kda)/math.log(6) * ((kp * 10)+(g * 5)+(cs * .7)+ (dmgdlt * 7) + (dmgtkn * 7) + (wards *6)  ))
						MVP += math.log(kda)/math.log(6) * ((kp * 10)+(g * 5)+(cs * 1.0)+ (dmgdlt * 6) + (dmgtkn * 7) + (wards *5)  )+ trip * .25 + quad * .5 + penta * 1

					elif p.timeline.role.name == 'none': #jungle
						#print(math.log(kda)/math.log(6))
						MVP += math.log(kda)/math.log(6) * ((kp * 10)+(g * 5)+(cs * .7)+ (dmgdlt * 7) + (dmgtkn * 7) + (wards *4)  )+ trip * .25 + quad * .5 + penta * 1

					else: #unknown duo setup
						#print(math.log(kda)/math.log(6))
						MVP += math.log(kda)/math.log(6) * ((kp * 10)+(g * 5)+(cs * .7)+ (dmgdlt * 10) + (dmgtkn * 2) + (wards *4)  ) + trip * .25 + quad * .5 + penta * 1
					
					if player.stats.win:
						wins = wins + 1
					else:
						losses = losses + 1

		championStats = {}
		championStats['level'] = masteries[c].level
		championStats['topGrade'] = masteries[c].highest_grade
		championStats['points'] = masteries[c].points
		championStats['topKDA'] = round(topKDA, 2)
		if deaths == 0:
			deaths = 1
		championStats['KDA'] = round((kills + assists) / deaths , 2)
		championStats['avgkills'] = round(kills / (wins+ losses), 2)
		championStats['avgdeaths'] = round(deaths / (wins+ losses), 2)
		championStats['avgassists'] = round(assists / (wins+ losses), 2)
		championStats['avgMVP'] = round(MVP / (wins + losses), 2)
		if championStats['avgMVP'] > 5:
			championStats['avgMVP'] = 5
		if championStats['avgMVP'] < 0:
			championStats['avgMVP'] = 0
		championStats['wins'] = wins
		championStats['losses'] = losses
		imagep = c.image.link
		imagep = imagep.split('.')
		image = 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/' + imagep[0] + '_0.jpg'
		displayChampions.append({'name':str(c), 'stats':championStats, 'mastery': masteries[c], 'masterypoint':masteries[c].points, 'image': image })
	displayChampions = sorted(displayChampions, key=itemgetter('masterypoint'), reverse=True)

	request.session[request.GET.get('region')] = {}
	request.session[request.GET.get('region')][request.GET.get('summ')] = displayChampions
	request.session.modified = True
	return HttpResponse(render(request, 'doransloading.html',))

def cards(request):
	print (request)
	if request.is_ajax():
		print("Ajax got called")
		print(request.GET.get('region'))
		print(request.GET.get('summ'))
		json_d = {}
		try: 
			if request.GET.get('summ') in request.session.get(request.GET.get('region')):
				print("WE DID IT")
				request.session['loading' + request.GET.get('region') + request.GET.get('summ')] = False
				json_d['success'] = "True"
				return JsonResponse(json_d)
		except TypeError:
			print("oh god this is gonna print so much")
		try:
			print("trying to see if loading, loadingbool:")
			if  request.session.get('loading' + request.GET.get('region') + request.GET.get('summ')):
				request.session['loading' + request.GET.get('region') + request.GET.get('summ')] = False
				print("it found the region")
				print("It is already loading")
				json_d['success'] = "False"

				return JsonResponse(json_d)
			else:
				request.session['loading' + request.GET.get('region') + request.GET.get('summ')] = True
				request.session.modified = True
				print (request.session.get('loading' + request.GET.get('region') + request.GET.get('summ')))
				load(request)
				json_d['success'] = "False"
				return JsonResponse(json_d)
		except TypeError:
			request.session['loading' + request.GET.get('region') + request.GET.get('summ')] = True
			request.session.modified = True
			print (request.session['loading'][request.GET.get('region')][request.GET.get('summ')])
			load(request)
			json_d['success'] = "False"
			return JsonResponse(json_d)

	if request.GET:
		try:
			if request.session[request.GET.get('region')][request.GET.get('summ')]:
				return HttpResponse(render(request, 'doranscards.html', {'champions' : request.session[request.GET.get('region')][request.GET.get('summ')]}))
		except KeyError:
			return HttpResponse(render(request, 'doransloading.html',))
			
	else:
		return HttpResponseRedirect('/dorans/')