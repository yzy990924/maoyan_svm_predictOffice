import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from xlrd import open_workbook # xlrd用于读取xld
from texttable import Texttable
import seaborn as sns
import re

#票房Top 10
def office_top_10(df):
	data1=pd.DataFrame(df,columns=['名称','上映时间', '类型','评分','累计票房'])
	data1['累计票房'] = data1['累计票房'].apply(int)
	data1 = data1.sort_values(by='累计票房', ascending=False)[0:10]
	tb=Texttable() #表格展示
	tb.header(data1.columns.to_numpy())
	tb.add_rows(data1.values,header=False)
	print(tb.draw())

#票房影响因素
def office_influence(df):
	data2 = pd.DataFrame(df,columns = ['评分','首周票房','时长','评分人数','累计票房'])
	data2['评分人数'] = data2['评分人数'].str.replace('万元',' ')
	data2['评分人数'] = data2['评分人数'].str.replace('万',' ')
	data2['时长'] = data2['时长'].str.replace('分钟',' ')
	data2.dropna(axis=0, how='any', inplace=True)#去掉含空值的行
	data2 = data2.astype(float)
	ax = sns.heatmap(data2.corr(), annot=True, vmax=1, square=True, cmap="Blues")
	ax.set_ylim(5.0, 0) 


#电影总类型统计
def countN(column):
    count = dict()
    for row in column:
    	row = row.split(',')
    	row = row[:len(row)-1]
    	for ele in row:
            if ele in count:
                count[ele] += 1
            else:
                count[ele] = 1
    return count

def movie_type(df):
	data3 = pd.DataFrame(df,columns = ['名称', '类型','年份'])
	#每种类型出现的次数除以总的影片数，以此作为该种类型的频数百分比
	genres = pd.Series(countN(data3['类型'])).sort_values()
	genres_avg = genres / len(data3)
	genres_avg.plot(kind = 'barh', title = '类型频率')
	#选取前5种类型，观察它们在这15年间每年的数量与当年影片总数之比的变化
	genres_by_year = data3.groupby('年份')['类型'].sum()
	genres_count = pd.DataFrame([], index = genres_by_year.index, columns = genres.index[len(genres)-5:])
	print(len(genres))
	for g in genres_count.columns:
	    for y in genres_count.index:
	        genres_count.loc[y,g] = genres_by_year[y].count(g) / len(genres_by_year[y])
	genres_count.plot(figsize = (10,6), title = 'Evolution of Movies in 5 Genres')

#不同类型影片的票房
#对于某种类型，计算所有该类影片的票房，再除以该类影片的数量
def differ_type(df):
	data3 = pd.DataFrame(df,columns = ['名称', '类型','年份'])
	genres = pd.Series(countN(data3['类型'])).sort_values()
	movies_by_genres = pd.DataFrame(0, index = genres.index, columns = ['累计票房', '评分'])

	for i in range(len(df)):
	    row = df['类型'][i].split(',')
	    row = row[:len(row)-1]
	    for g in row:
	        movies_by_genres.loc[g, '累计票房'] += df['累计票房'][i]    #该类影片的总票房
	        movies_by_genres.loc[g, '评分'] += df['评分'][i]    #该类型影片的总评分
	movies_by_genres = movies_by_genres.div(genres.values, axis=0)
	movies_by_genres.sort_values('累计票房', ascending=False)[['累计票房']].plot( kind = 'bar', title='Average Revenue in Different Genres')
	return movies_by_genres

#导演的票房分布
def director_office(df):
	df['累计票房'] = df['累计票房'].astype(float)
	revenue_of_director = df.groupby('演职人员1').累计票房.mean()    #平均票房
	return revenue_of_director

#主演的票房分布
def count_actor(column):
    count = dict()
    for row in column:
    	row = row.split(',')
    	for ele in row:
            if ele in count:
                count[ele] += 1
            else:
                count[ele] = 1
    return count
def score_actor(df):
	# movies_noani = df[~df['类型'].str.contains('动画', regex=False)].reset_index(drop = 'True') 
	movies_noani = df
	movies_noani['演职人员2'] = movies_noani['演职人员2'].replace(' ',' ')+','+movies_noani['演职人员3'].replace(' ',' ')
	actors = pd.Series(count_actor(movies_noani['演职人员2'])).sort_values()
	movies_by_actors = pd.DataFrame(0, index = actors.index, columns = ['累计票房', '评分'])
	#按不同权重统计演员的票房：
	r4 = [0.4, 0.3, 0.2, 0.1]    #如果有4位主演，按此加权，以下类似
	r3 = [0.4, 0.3, 0.3]
	r2 = [0.6, 0.4]
	r1 = [1]
	r = [r1, r2, r3, r4]
	for i in range(len(movies_noani)):
		actorlist = movies_noani['演职人员2'][i].split(',')[0:2]
		for j in range(len(actorlist)):
			movies_by_actors.loc[actorlist[j], '累计票房'] += movies_noani['累计票房'][i] * r[len(actorlist)-1][j] #一个演员的总票房
			movies_by_actors.loc[actorlist[j], '评分'] += movies_noani['评分'][i] * r[len(actorlist)-1][j]   #一个演员的总评分
	movies_by_actors = movies_by_actors.div(actors.values, axis=0)    #求平均值
	return movies_by_actors



#档期分布
def month_movie(df):
	df['month'] = pd.to_datetime(df['上映时间']).apply(lambda x: x.month)
	revenue_month = df.groupby('month')['累计票房'].sum() / df.groupby('month').size()
	revenue_month.plot(kind='bar', title='Average Revenue per Month')
	return revenue_month


##main函数
# if __name__ == "__main__":
# #数据读取并预处理
# data = pd.read_excel(file)
# df = pd.DataFrame(data)
# df = df[(df.累计票房!='暂无')]
# df['年份'] = pd.to_datetime(df['上映时间']).apply(lambda x: x.year)
# df.dropna(axis=0, how='any', inplace=True)#去掉含空值的行
# df = df[~df.isin(['暂无'])]
# df.reset_index(drop=True, inplace=True)#重新排序
# file = 'd:\\movie.xls'

# office_top_10(df)
# office_influence(df)
# movie_type(df)
# differ_type(df)
# revenue_of_director = director_office(df)
# revenue_of_director.sort_values().tail(10).plot(kind = 'barh', title = 'Directors with Top Revenue')
# actor = score_actor(df)
# actor['累计票房'].sort_values().tail(10).plot(kind = 'barh')
# month_movie(df)


# plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
# plt.rcParams['font.serif'] = ['KaiTi']
# plt.rcParams['axes.unicode_minus'] = False
# plt.show()