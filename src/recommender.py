# -*- coding:utf-8 -*-
# author = oulaline

import os
import sys
import codecs
import pandas as pd
import math

class recommender(object):
	def __init__(self, path):
		self.csvpath = path #格式应为'UserID','MusicID','Rating', 要有列头

	def readRatingDate(self, path='../ml-1m/ratings.dat'):  
	    ''''' 
	    读取评分数据并存储为csv文件 
	    :param path:文件路径 
	    :return: DataFrame 
	    '''  
	    f = pd.read_table(path,sep='::',names=['UserID','MusicID','Rating','Timestamp'],engine = 'python')  
	    f.to_csv('../ml-1m/ratings.csv',columns =['UserID','MusicID','Rating'], index=False)  
	    return f  

	def calcuteSimilar(self, series1,series2):  
	    ''''' 
	    计算余弦相似度 
	    :param data1: 数据集1 Series 
	    :param data2: 数据集2 Series 
	    :return: 相似度 
	    '''  
	    unionLen = len(set(series1) & set(series2))  
	    if unionLen == 0: return 0.0  
	    product = len(series1) * len(series2)  
	    similarity = unionLen / math.sqrt(product)  
	    return similarity  

	def calcuteUser(self, targetID=1,TopN=10):  
	    ''''' 
	    计算targetID的用户与其他用户的相似度 
	    :return:相似度TopN的UserID
	    '''  
	    frame = pd.read_csv(self.csvpath)                                                        #读取数据  
	    targetUser = frame[frame['UserID'] == targetID]['MovieID']                          #目标用户数据  
	    otherUsersID = [i for i in set(frame['UserID']) if i != targetID]                   #其他用户ID  
	    otherUsers = [frame[frame['UserID'] == i]['MovieID'] for i in otherUsersID]         #其他用户数据  
	    similarlist = [self.calcuteSimilar(targetUser,user) for user in otherUsers]              #计算  
	    similarSeries = pd.Series(similarlist,index=otherUsersID)                           #Series  
	    return similarSeries.sort_values()[-TopN:].index

if __name__ == "__main__":
	if len(sys.argv) < 2:
		path = '../ml-1m/ratings.csv'
	else:
		path = sys.argv[1]
	rec = recommender(path)
	rec.readRatingDate()
	sim = rec.calcuteUser(targetID = 50, TopN = 5)
	for si in sim:
		print si





