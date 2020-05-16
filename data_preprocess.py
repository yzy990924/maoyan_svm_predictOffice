import data_feature
import pandas as pd

#影片类型量化
def Type(df):
	movies_by_genres = data_feature.differ_type(df)
	type_process = pd.DataFrame(0, index = df.index, columns = ['类型得分'])
	for i in range(len(df)):
		typelist = df['类型'][i].split(',')
		typelist = typelist[:len(typelist)-1]
		for j in range(len(typelist)):
			type_process.loc[i, '类型得分'] +=  movies_by_genres.loc[typelist[j],'累计票房']/10000000
		type_process.loc[i, '类型得分']  = type_process.loc[i, '类型得分'] / len(typelist)
	return type_process

#主演量化
def Actor_score(df):
	actor = data_feature.score_actor(df)
	movies_noani = df
	movies_noani['演职人员2'] = movies_noani['演职人员2'].replace(' ',' ')+','+movies_noani['演职人员3'].replace(' ',' ')
	actor_score = pd.DataFrame(0, index = df.index, columns = ['演员总分','演员票房号召力'])
	for i in range(len(movies_noani)):
		actorlist = movies_noani['演职人员2'][i].split(',')[0:2]
		for j in range(len(actorlist)):
			actor_score.loc[i,'演员总分'] += actor.loc[actorlist[j],'评分']
			actor_score.loc[i,'演员票房号召力'] += actor.loc[actorlist[j],'累计票房']/1000000
		actor_score.loc[i,'演员总分'] = actor_score.loc[i,'演员总分'] / len(actorlist)

	return actor_score

#导演量化
def director__mean_office(df):
	revenue_of_director = data_feature.director_office(df)
	director = pd.DataFrame(0, index = df.index, columns = ['导演总票房(百万)'])
	for i in range(len(df)):
		actorlist = df['演职人员1'][i]
		director.loc[i, '导演总票房(百万)'] =  revenue_of_director.loc[actorlist]/1000000
	return director
