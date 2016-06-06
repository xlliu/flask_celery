#!/usr/bin/env python
#coding:utf-8
# Author:   --<qingfengkuyu>
# Purpose: MongoDB的使用
# Created: 2014/4/14
#32位的版本最多只能存储2.5GB的数据（NoSQLFan：最大文件尺寸为2G，生产环境推荐64位）
import pymongo
import datetime
import random


#创建连接
from bson import ObjectId

conn = pymongo.MongoClient('127.0.0.1', 27017)
#连接数据库
db = conn.xyt_survey
#db = conn['study']

#打印所有聚集名称，连接聚集
print u'所有聚集:',db.collection_names()
posts = db.xlliu_test_struct
posts2 = db.xlliu_test_answer
mapping = db.xlliu_test_mapping
#posts = db['post']
print posts
print "---------------------------------------------"

#插入记录
new_post = {
  "_id" : ObjectId("5710a6ff3f6a9f85418b4591"),
  "project_id" : "5710a50a3f6a9f88418b4595",
  "answers" : [{
      "qid" : "5710a54a3f6a9feb598b4598",
      "answer" : ["5710a54a3f6a9feb598b4599"]
    }, {
      "qid" : "5710a5513f6a9f8c418b458f",
      "answer" : {
        "5710a5513f6a9f8c418b4590_open" : "13388886666"
      }
    }, {
      "qid" : "5710a55c3f6a9f8c418b4591",
      "answer" : ["5710a55c3f6a9f8c418b4592"]
    }, {
      "qid" : "5710a5643f6a9fea598b4597",
      "answer" : {
        "5710a5643f6a9fea598b459a" : ["5710a5643f6a9fea598b4598"],
        "5710a5643f6a9fea598b459b" : ["5710a5643f6a9fea598b4599"]
      }
    }, {
      "qid" : "5710a56c3f6a9f85418b458e",
      "answer" : {
        "5710a56c3f6a9f85418b458f_open" : "多项填空1",
        "5710a56c3f6a9f85418b4590_open" : "多项填空2",
        "5710a6a03f6a9f87418b4586_open" : "多项填空3",
        "5710a6a33f6a9f87418b4587_open" : "多项填空4"
      }
    }],
  "pconvert_data" : "{}",
  "finish_status" : "1",
  "starttime" : 1460709070,
  "endtime" : 1460709119,
  "ip" : "114.111.167.91",
  "uuid" : "5yudvC1460709070",
  "svc" : "becfba758d6c74f7f5aece4891cf08b0",
  "project_version" : "1",
  "s_code" : "0",
  "s_func_id" : "",
  "vvv" : "",
  "rand_int" : "0",
  "time_list_str" : {
    "question_5710a54a3f6a9feb598b4598" : [ "1460708787682"],
    "question_5710a5513f6a9f8c418b458f" : [ "1460708794216"],
    "question_5710a55c3f6a9f8c418b4591" : [ "1460708794308"],
    "question_5710a5643f6a9fea598b4597" : {
      "option_5710a5643f6a9fea598b459a_5710a5643f6a9fea598b4598" :  "1460708796681",
      "option_5710a5643f6a9fea598b459b_5710a5643f6a9fea598b4599" :  "1460708797895"
    },
    "question_5710a56c3f6a9f85418b458e" : {
      "option_5710a56c3f6a9f85418b458f" :  "1460708813981",
      "option_5710a56c3f6a9f85418b4590" :  "1460708814559",
      "option_5710a6a03f6a9f87418b4586" :  "1460708815053",
      "option_5710a6a33f6a9f87418b4587" :  "1460708815959"
    }
  },
  "schoolCode" : None,
  "answer_5710a54a3f6a9feb598b4598" : ["5710a54a3f6a9feb598b4599"],
  "answer_5710a5513f6a9f8c418b458f" : {
    "5710a5513f6a9f8c418b4590_open" : "13388886666"
  },
  "answer_5710a55c3f6a9f8c418b4591" : ["5710a55c3f6a9f8c418b4592"],
  "answer_5710a5643f6a9fea598b4597" : {
    "5710a5643f6a9fea598b459a" : ["5710a5643f6a9fea598b4598"],
    "5710a5643f6a9fea598b459b" : ["5710a5643f6a9fea598b4599"]
  },
  "answer_5710a56c3f6a9f85418b458e" : {
    "5710a56c3f6a9f85418b458f_open" : "多项填空1",
    "5710a56c3f6a9f85418b4590_open" : "多项填空2",
    "5710a6a03f6a9f87418b4586_open" : "多项填空3",
    "5710a6a33f6a9f87418b4587_open" : "多项填空4"
  }
}


new_post_2 = []

new_posts = [{"AccountID":22,"UserName":"liuw",'date':datetime.datetime.now()},
             {"AccountID":23,"UserName":"urling",'date':datetime.datetime.now()}]#每条记录插入时间都不一样

posts2.insert(new_post)
# posts2.insert(new_post_2)
# mapping.insert()
print '-'*20
#posts.insert(new_posts)#批量插入多条数据


#删除记录
print u'删除指定记录:\n',posts.find_one({"AccountID":22,"UserName":"libing"})
posts.remove({"AccountID":22,"UserName":"libing"})

#修改聚集内的记录
posts.update({"UserName":"urling"},{"$set":{'AccountID':random.randint(20,50)}})

#查询记录，统计记录数量
print u'记录总计为：',posts.count(),posts.find().count()
print u'查询单条记录:\n',posts.find_one()
print posts.find_one({"UserName":"liuw"})

#查询所有记录
print u'查询多条记录:'
#for item in posts.find():#查询全部记录
#for item in posts.find({"UserName":"urling"}):#查询指定记录
#for item in posts.find().sort("UserName"):#查询结果根据UserName排序，默认为升序
#for item in posts.find().sort("UserName",pymongo.ASCENDING):#查询结果根据UserName排序，ASCENDING为升序,DESCENDING为降序
for item in posts.find().sort([("UserName",pymongo.ASCENDING),('date',pymongo.DESCENDING)]):#查询结果根据多列排序
    print item

#查看查询语句的性能
#posts.create_index([("UserName", pymongo.ASCENDING), ("date", pymongo.DESCENDING)])#加索引
print posts.find().sort([("UserName",pymongo.ASCENDING),('date',pymongo.DESCENDING)]).explain()["cursor"]#未加索引用BasicCursor查询记录
print posts.find().sort([("UserName",pymongo.ASCENDING),('date',pymongo.DESCENDING)]).explain()["nscanned"]#查询语句执行时查询的记录数