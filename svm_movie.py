from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.svm import LinearSVR
from sklearn import metrics
from sklearn import preprocessing
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np
import pandas as pd
from sklearn import preprocessing
import data_preprocess
from texttable import Texttable
from sklearn.model_selection import GridSearchCV

# 1 准备数据
file = 'd:\\movie.xls'
data = pd.read_excel(file)
df = pd.DataFrame(data)

df = df[(df['累计票房']!='暂无')]
df['月份'] = pd.to_datetime(df['上映时间']).apply(lambda x: x.month)
df['评分人数'] = df['评分人数'].str.replace('万',' ')

df.dropna(axis=0, how='any', inplace=True)#去掉含空值的行
df = df[~df.isin(['暂无'])]

df.reset_index(drop=True, inplace=True)#重新排序

type_process = data_preprocess.Type(df) #类型量化
actor_score = data_preprocess.Actor_score(df) #演员量化
director = data_preprocess.director__mean_office(df) #导演量化

df_result = pd.concat([df,type_process,director,actor_score], axis=1) #合并

df = pd.DataFrame(df_result,columns = ['月份','类型得分','评分人数','评分','首周票房','导演总票房(百万)','演员总分','演员票房号召力','累计票房'])
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)#重新排序

df = df.astype(float)
list=df.values.tolist()

# tb=Texttable()
# tb.header(df.columns.to_numpy())
# tb.add_rows(df.values,header=False)
# print(tb.draw())


x = []
label_encoder = []
y = []
for row in range(len(df)):
	for  a in range(3):
		if type(list[row][a]) == float:
			list[row][a] = list[row][a]
		else :
			label_encoder.append(preprocessing.LabelEncoder())
			list[row][a]= label_encoder[-1].fit_transform(list[row][a])
	x.append(list[row][:8])
	y.append(list[row][8]/1000000)
X = np.array(x)
Y = np.array(y)



# 2 分割训练数据和测试数据
# 随机采样25%作为测试 75%作为训练
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=33)


# 3 训练数据和测试数据进行标准化处理
ss_x = StandardScaler()
x_train = ss_x.fit_transform(x_train)
x_test = ss_x.transform(x_test)

ss_y = StandardScaler()
y_train = ss_y.fit_transform(y_train.reshape(-1, 1))
y_test = ss_y.transform(y_test.reshape(-1, 1))

# 4 模型选取(支持向量机模型进行学习和预测) 及评估
# 调参
clf = GridSearchCV(SVR(),param_grid={'kernel':['poly','sigmoid','rbf'],'C': [0.1,1,10],'gamma': [0.1,1,10]},cv=5)
clf.fit(x_train,y_train)
print("best_param:",clf.best_params_)
print("best_score:", clf.best_score_)

#  # ① 线性核函数
# clf = LinearSVR(C=2)
# clf.fit(x_train,y_train)
# y_pred = clf.predict(x_test)
# print("线性核函数：")
# print("训练集评分：", clf.score(x_train,y_train))
# print("测试集评分：", clf.score(x_test,y_test))
# print("测试集均方差：",metrics.mean_squared_error(y_test,y_pred.reshape(-1,1)))
# print("测试集R2分：",metrics.r2_score(y_test,y_pred.reshape(-1,1)))

# # ② 高斯核函数
# clf = SVR(kernel='rbf',C=10,gamma=0.1,coef0=0.1)
# clf.fit(x_train,y_train)
# y_pred = clf.predict(x_test)
# print("高斯核函数：")
# print("训练集评分：", clf.score(x_train,y_train))
# print("测试集评分：", clf.score(x_test,y_test))
# print("测试集均方差：",metrics.mean_squared_error(y_test,y_pred.reshape(-1,1)))
# print("测试集R2分：",metrics.r2_score(y_test,y_pred.reshape(-1,1)))

# # ③ sigmoid核函数
# clf = SVR(kernel='sigmoid',C=2)
# clf.fit(x_train,y_train)
# y_pred = clf.predict(x_test)
# print("sigmoid核函数：")
# print("训练集评分：", clf.score(x_train,y_train))
# print("测试集评分：", clf.score(x_test,y_test))
# print("测试集均方差：",metrics.mean_squared_error(y_test,y_pred.reshape(-1,1)))
# print("测试集R2分：",metrics.r2_score(y_test,y_pred.reshape(-1,1)))

# # ④ 多项式核函数
# clf = SVR(kernel='poly',C=2)
# clf.fit(x_train,y_train)
# y_pred = clf.predict(x_test)
# print("多项式核函数：")
# print("训练集评分：", clf.score(x_train,y_train))
# print("测试集评分：", clf.score(x_test,y_test))
# print("测试集均方差：",metrics.mean_squared_error(y_test,y_pred.reshape(-1,1)))
# print("测试集R2分：",metrics.r2_score(y_test,y_pred.reshape(-1,1)))

# 5 实例输出


# input_data = [ '1',  '0.290323',   '99',    '13.6',   '8.6',    '5713.0',   '233.000000',  '17.20']
# input_data_encoded = [-1] * len(input_data)
# count = 0
# for i, item in enumerate(input_data):
# 	input_data_encoded[i] = float(input_data[i])

# input_data_encoded = np.array(input_data_encoded)

# print("Predicted traffic:", float(linear_svr.predict([input_data_encoded])[0]))