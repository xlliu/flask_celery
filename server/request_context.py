# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

"""
@version: ??
@author: xlliu
@contact: liu.xuelong@163.com
@site: https://github.com/xlliu
@software: PyCharm
@file: request_context.py
@time: 2016/4/14 0014 下午 4:40
"""
import logging
import re
import gc

import html2text
from bson import ObjectId
from collections import OrderedDict

from common.mongodb_conn import mongodb_conn


class BreakException():
    pass


class RequestAction(object):
    def __init__(self):
        self.logger = logging.getLogger("log_output")
        set_mongo_conn_edy = mongodb_conn("10.10.0.2", 27017, "xyt_survey", flag=0)
        # set_mongo_conn_edy = mongodb_conn("120.131.64.225", 27017, "xyt_survey", flag=1)
        set_mongo_conn_edy_insert = mongodb_conn("10.10.0.2", 27017, "xyt_survey_data", flag=0)
        # set_mongo_conn_edy = mongodb_conn("120.131.70.8", 27017, "xyt_survey_survey", flag=1)
        # set_mongo_conn_edy = mongodb_conn("127.0.0.1", 27017, "xyt_survey")
        self.get_mongo_conn_edy = set_mongo_conn_edy.get_conn()
        self.get_mongo_conn_edy_insert = set_mongo_conn_edy_insert.get_conn()
        self.mongo_collection_edy = set_mongo_conn_edy.get_db()
        self.mongo_collection_edy_insert = set_mongo_conn_edy_insert.get_db()

        # set_mongo_conn = mongodb_conn("127.0.0.1", 27017, "xyt_survey")
        # self.get_mongo_conn = set_mongo_conn.get_conn()
        # self.mongo_collection = set_mongo_conn.get_db()
        # mysql_conn = mysqldb_conn("localhost", 3306, "test").conn()

    def answers_action(self, aid):
        try:
            document_answer, document_question, document_question_struct, document_option, document_option_matrix, document_project = self.init_collection()
            self.handle_data(aid, document_answer, document_question, document_question_struct, document_option,document_option_matrix, document_project)
        finally:
            self.close_connector()

    def question_action(self, pid, limit_num, skip_num):
        temp_id = {'project_id': pid}
        # 初始化数据库
        document_answer, document_question, document_question_struct, document_option, document_option_matrix, document_project = self.init_collection()
        rdata = document_answer.find(temp_id, no_cursor_timeout=True).limit(limit_num).skip(skip_num)

        num = skip_num
        # gc.disable()
        for answer in rdata:
            num += 1
            self.logger.info("PROJECT_ACTION==> for project_data in a_num: %d, pid : %s, aid: %s" %(num, pid, answer["_id"]))
            #     continue
            try:
                self.handle_data(answer["_id"], document_answer, document_question, document_question_struct,
                                 document_option,document_option_matrix, document_project)
            except:
                pass
        self.close_connector()

    # gc.enable()
    def all_action(self):
        document_answer, document_question, document_question_struct, document_option, document_option_matrix, document_project = self.init_collection()
        rdata = document_project.find({},{"_id":1},no_cursor_timeout=True).limit(30).skip(20)
        
        num_p = 0 
        for p_action in rdata:
            self.logger.info("ALL_ACTION==> for all_data in p_num: %d, pid: %s" %(num_p, p_action["_id"]))
            self.question_action(str(p_action["_id"]),1000000,0)
            num_p += 1


    def init_collection(self):
        document_answer = self.mongo_collection_edy.xyt_survey_answers
        document_question = self.mongo_collection_edy.xyt_survey_question
        document_question_struct = self.mongo_collection_edy.xyt_survey_question_struct
        document_option = self.mongo_collection_edy.xyt_survey_option
        document_option_matrix = self.mongo_collection_edy.xyt_survey_option_matrix
        document_project = self.mongo_collection_edy.xyt_survey_project
        # document_answer = self.mongo_collection.xyt_survey_answers
        # document_question = self.mongo_collection.xyt_survey_question
        # document_option = self.mongo_collection.xyt_survey_option
        # document_option_matrix = self.mongo_collection.xyt_survey_option_matrix
        return document_answer, document_question, document_question_struct, document_option, document_option_matrix, document_project

    def close_connector(self):
        # if self.get_mongo_conn is not None:
        #     self.get_mongo_conn.close()
        if self.get_mongo_conn_edy is not None:
            self.get_mongo_conn_edy.close()
        if self.get_mongo_conn_edy_insert is not None:
            self.get_mongo_conn_edy_insert.close()
            # if db is not None:
            #     mysql_conn.close()

    def generator_title(self, pid, document_project):
        p_struct = document_project.find_one({"_id": ObjectId(pid)})

        lag = p_struct.get("change_log", 0)
        temp_struct_data = []
        for question in p_struct.get("questionpage_list"):
            for q_struct in question.get("question_list"):
                question_type = q_struct.get("question_type")
                q_title_temp = q_struct.get("title")
                q_title_temp = html2text.html2text(q_title_temp)

                #text = re.match("(&nbsp;)*\d+\\\*(&nbsp;)*\.\\\*(&nbsp;)*", q_title_temp)
                #if text:
                #    n = len(text.group())
                #else:
                #    n = 0
                #q_title = q_title_temp[n:]
                q_title = q_title_temp

                if question_type == 70:
                    pass
                if question_type in (2, 3, 6):
                    temp_struct_data.append(q_title.replace(r".", "d"))

                if question_type in (4, 5):
                    for q_ in q_struct.get("matrixrow_list"):
                        q_title_t = q_title +"_%s" % html2text.html2text(q_.get("title"))
                        temp_struct_data.append(q_title_t.replace(r".", "d"))

                if question_type in (8, 50, 60, 95):
                    for q_ in q_struct.get("option_list"):
                        q_title_t = q_title + "_%s" % html2text.html2text(q_.get("title"))
                        temp_struct_data.append(q_title_t.replace(r".", "d"))

                if question_type in (7, 100):
                    for qm_ in q_struct.get("matrixrow_list"):
                        for qo_ in q_struct.get("option_list"):
                            q_title_t = html2text.html2text(q_title + "_%s_%s" % (qm_.get("title"), qo_.get("title")))
                            temp_struct_data.append(q_title_t.replace(r".", "d"))

        return temp_struct_data, lag

    def handle_data(self, aid, document_answer, document_question, document_question_struct, document_option,
                    document_option_matrix, document_project):
        temp_aid = {"_id": ObjectId(str(aid))}
        #self.logger.info("inot func handle_data, temp_aid: %s" %temp_aid)

        temp_struct_data = OrderedDict()
        result_answer = document_answer.find_one(temp_aid)
        pid = result_answer.get('project_id')
        title_m, lag = self.generator_title(pid, document_project)
        temp_struct_data[u"0d开始时间"] = result_answer.get('starttime')
        temp_struct_data[u"0d结束时间"] = result_answer.get('endtime')
        temp_struct_data[u"0d序号"] = str(result_answer.get('_id'))
        temp_struct_data[u"0d用户"] = result_answer.get('uuid')
        temp_struct_data[u"0d版本"] = lag
        temp_struct_data = OrderedDict(temp_struct_data.items()+zip(title_m, [""]*len(title_m)))
        # temp_struct_data[u"schoolCode"] = result_answer.get('schoolCode', 'None')
        answers = result_answer.get('answers')
        if not answers:
            return

        num = 0
        for question in answers:
            """
            {
              "_id" : ObjectId("570ddc27ea1967e46b8b45a1"),
              "project_id" : "570dda3aea196747618b45c7",
              "answers" : [{
                  "qid" : "570ddaf5ea19674f618b45ce",                             //性别
                  "answer" : ["570ddaf5ea19674f618b45cf"]                         //男
                }, {
                  "qid" : "570dda45ea1967386c8b45aa",                             //单项选择题2
                  "answer" : ["570dda45ea1967386c8b45ab"]
                }, {
                  "qid" : "570dda6fea1967376c8b459b",                             //多项选择题3
                  "answer" : [["570dda6fea1967376c8b459d"]]
                }
                ......
            """

            q_title = ""
            question_type = None
            option = {} 
            for k, v in question.items():
                if "qid" == k:
                    temp_qid = {"_id": ObjectId(str(v))}
                    #self.logger.info("Into deal with key, qid: %s" %temp_qid)
                    q_struct = document_question.find_one(temp_qid)
                    if not q_struct:
                        temp_qid = {"_id": str(v)}
                        #self.logger.info("Into deal with key, key is str, qid: %s" %temp_qid)
                        q_struct = document_question.find_one(temp_qid)
                        if not q_struct:
                            self.logger.info("next return")
                            return
                    q_title_temp_kk = q_struct.get('title')
                    q_title_temp_kk = html2text.html2text(q_title_temp_kk)
                    #text = re.match("(&nbsp;)*\d+\\\*(&nbsp;)*\.\\\*(&nbsp;)*", q_title_temp_kk)
                    #if text:
                    #    n = len(text.group())
                    #else:
                    #    n = 0
                    #q_title = q_title_temp_kk[n:]
                    q_title = q_title_temp_kk
                    # q_title = q_struct.get('title')

                    q_title = q_title.replace(r".", "d")
                    # q_title = "(%s)%s"%(num,q_title)
                    num += 1
                    question_type = q_struct.get('question_type')
                    break

            for k, v in question.items():
                # self.logger.info("Into deal with value")
                if "answer" == k:
                    # 单项选择题2
                    """
                    {
                      "qid" : "570dda45ea1967386c8b45aa",                            //单项选择题2
                      "answer" : ["570dda45ea1967386c8b45ab"]                        //[option_id]
                    }
                    """
                    if question_type == 2:
                        temp_value_id = {"_id": ObjectId(str(v[0]))}
                        a_context = document_option.find_one(temp_value_id)
                        a_value = a_context.get('title')
                        #temp_struct_data[q_title] = html2text.html2text(a_value)
                        temp_struct_data[q_title] = a_value
                        break
                    # 多项选择题3
                    """
                    {
                      "qid" : "570dda6fea1967376c8b459b",                             //多项选择题3
                      "answer" : [["570dda6fea1967376c8b459d"]]                       //[[option_id],...]
                    }
                    """
                    if question_type == 3:
                        a_value_temp = []
                        for value in v:
                            temp_value_id = {"_id": ObjectId(str(value[0]))}
                            a_context = document_option.find_one(temp_value_id)
                            a_value_temp.append(a_context.get('title'))
                        a_value = a_value_temp
                        #temp_struct_data[q_title] = html2text.html2text(",".join(a_value))
                        temp_struct_data[q_title] = ",".join(a_value)
                        break
                    # 表格单选题4------
                    """
                    {
                      "qid" : "570dda69ea1967e5608b45ca",                             //表格单选题4
                      "answer" : {
                        "570dda69ea1967e5608b45cd" : ["570dda69ea1967e5608b45cc"],    //option_matrix_id:[option_id]
                        "570dda69ea1967e5608b45ce" : ["570dda69ea1967e5608b45cb"]
                      }
                    }
                    """
                    if question_type == 4:
                    # if question_type == 5:
                        for k_4, v_4 in v.items():
                            q_title_temp = document_option_matrix.find_one({"_id": ObjectId(str(k_4))}).get('title')
                            temp_value_id = {"_id": ObjectId(str(v_4[0]))}
                            a_context = document_option.find_one(temp_value_id)
                            a_value = a_context.get('title')

                            #temp_struct_data[
                        #        q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = html2text.html2text(a_value)
                            temp_struct_data[
                                q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = a_value
                        break
                    # 表格多选题5
                    """
                    {
                      "qid" : "570dda77ea1967dc608b45bb",                             //表格多选题5
                      "answer" : {
                        "570dda77ea1967dc608b45be" : [["570dda77ea1967dc608b45bc"]],  //option_matrix_id:[[option_id]]
                        "570dda77ea1967dc608b45bf" : [["570dda77ea1967dc608b45bc"], ["570dda77ea1967dc608b45bd"]]
                      }
                    }
                    """
                    if question_type == 5:
                    # if question_type == 4:
                        for k_5, v_5 in v.items():
                            q_title_temp = document_option_matrix.find_one({"_id": ObjectId(str(k_5))}).get('title')
                            a_value_temp = []
                            for v_5v in v_5:
                                temp_value_id = {"_id": ObjectId(str(v_5v[0]))}
                                a_context = document_option.find_one(temp_value_id)
                                a_value_temp.append(a_context.get('title'))
                            a_value = a_value_temp

                            #temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = html2text.html2text(",".join(a_value))
                            temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = ",".join(a_value)
                        break
                    # 选择排序题60
                    """
                    {
                      "qid" : "570dda88ea1967786c8b4599",                             //选择排序题60
                      "answer" : {
                        "570dda88ea1967786c8b459b" : [NumberLong(1)],                 //[option_id]:[value]
                        "570dda88ea1967786c8b459a" : [NumberLong(2)]
                      }
                    }
                    """
                    if question_type == 60:
                        for k_60, v_60 in v.items():
                            q_title_temp = document_option.find_one({"_id": ObjectId(str(k_60)[7:])}).get('title')
                            temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = v_60[0]
                            # temp_struct_data[q_title+"_%s" % q_title_temp] = "类型60，矩阵跳过"
                        break  # 单项打分题50
                    """
                    {
                      "qid" : "570dda8eea19674b6c8b4593",                             //单项打分题50
                      "answer" : {
                        "570dda8eea19674b6c8b4594" : ["5"],                           //[option_id]:["value"]
                        "570dda8eea19674b6c8b4595" : ["2"]
                      }
                    }
                    """
                    if question_type == 50:
                        for k_50, v_50 in v.items():
                            q_title_temp = document_option.find_one({"_id": ObjectId(str(k_50))}).get('title')
                            temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = v_50[0]
                        break
                    # 多项打分题7
                    """
                    {
                      "qid" : "570dda95ea196739618b45d5",                             //多项打分题7
                      "answer" : {
                        "570dda95ea196739618b45d8" : {                                //option_matrix_id:{option:value}
                          "570dda95ea196739618b45d6" : "5",
                          "570dda95ea196739618b45d7" : "3"
                        },
                        "570dda95ea196739618b45d9" : {
                          "570dda95ea196739618b45d6" : "1",
                          "570dda95ea196739618b45d7" : "5"
                        }
                      }
                    }
                    """
                    if question_type == 7:
                        for k_7, v_7 in v.items():
                            q_title_temp_1 = document_option_matrix.find_one({"_id": ObjectId(str(k_7))}).get('title')
                            for k_7k, v_7v in v_7.items():
                                q_title_temp_2 = document_option.find_one({"_id": ObjectId(str(k_7k))}).get('title')

                                #temp_struct_data[html2text.html2text(q_title + "_%s_%s" % (q_title_temp_1,
                                #                                       q_title_temp_2)).replace(r".", "d")] = html2text.html2text(v_7v)
                                temp_struct_data[html2text.html2text(q_title + "_%s_%s" % (q_title_temp_1,
                                                                       q_title_temp_2)).replace(r".", "d")] = v_7v
                        break
                    # 单项填空题6 多行文本题6
                    """
                    {
                      "qid" : "570dda9bea1967ef6b8b4592",                             //单项填空题6
                      "answer" : {
                        "570dda9bea1967ef6b8b4593_open" : "xlliu_danxiangtiankong"
                      }
                    {
                      "qid" : "570ddaaeea19673f6c8b459f",                             //多行文本题6
                      "answer" : {
                        "570ddaaeea19673f6c8b45a0_open" : "xlliu_testtesttesttesttesttesttesttesttest"
                      }
                    }
                    """
                    if question_type == 6:
                        a_value = v.values()[0]

                        #temp_struct_data[q_title] = html2text.html2text(a_value)
                        temp_struct_data[q_title] = a_value
                        break
                    # 多项填空题95
                    """
                    {
                      "qid" : "570ddaa0ea1967646c8b45a6",                             //多项填空题95
                      "answer" : {
                        "570ddaa0ea1967646c8b45a7_open" : "xlliu_duoxiangtiankong",
                        "570ddaa0ea1967646c8b45a8_open" : "xlliu_duoxiangtiankong2"
                      }
                    }
                    """
                    if question_type == 95:
                        for k_95, v_95 in v.items():
                            q_title_temp = document_option.find_one({"_id": ObjectId(str(k_95[0:-5]))}).get('title')

                            #temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = html2text.html2text(v_95)
                            temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = v_95
                        break
                    # 表格填空题100
                    """
                    {
                      "qid" : "570ddaa9ea196709618b45e1",                             //表格填空题100
                      "answer" : {
                        "570ddaa9ea196709618b45e4" : {
                          "570ddaa9ea196709618b45e2" : "xlliu_juzhenbiaoge1_1",
                          "570ddaa9ea196709618b45e3" : "xlliu_juzhenbiaoge1_2"
                        },
                        "570ddaa9ea196709618b45e5" : {
                          "570ddaa9ea196709618b45e2" : "xlliu_juzhenbiaoge2_1",
                          "570ddaa9ea196709618b45e3" : "xlliu_juzhenbiaoge2_2"
                        }
                      }
                    }
                    """
                    if question_type == 100:
                        for k_100, v_100 in v.items():
                            q_title_temp_1 = document_option_matrix.find_one({"_id": ObjectId(str(k_100))}).get('title')
                            for k_100k, v_100v in v_100.items():
                                q_title_temp_2 = document_option.find_one({"_id": ObjectId(str(k_100k))}).get('title')

                                #temp_struct_data[
                                #    html2text.html2text(q_title + "_%s_%s" % (q_title_temp_1,
                                #                          q_title_temp_2)).replace(r".", "d")] = html2text.html2text(v_100v)
                                temp_struct_data[
                                    html2text.html2text(q_title + "_%s_%s" % (q_title_temp_1,
                                                          q_title_temp_2)).replace(r".", "d")] = v_100v
                        break
                    """
                    {
                        u'qid': u'5629abcaea1967093b8b4569',                          //生日,城市(类级联操作)
                        u'answer': {
                        u'5629abcaea1967093b8b456c_open': u'3',
                        u'5629abcaea1967093b8b456b_open': u'8',
                        u'5629abcaea1967093b8b456a_open': u'1993'
                        }
                    }
                    """
                    if question_type == 8:
                        for k_8, v_8 in v.items():
                            q_title_temp = document_option.find_one({"_id": ObjectId(str(k_8[0:-5]))}).get('title')

                            #temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = html2text.html2text(v_8)
                            temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = v_8
                        break
                    if None == question_type:
                        raise "====Question_type is None, Exception===="
                    break
        dev_excel_mapping = "pid_%s" % pid
        # self.logger.info("generator db collection finally")
        collection = getattr(self.mongo_collection_edy_insert, dev_excel_mapping)
        # collection = getattr(self.mongo_collection, dev_excel_mapping)
        c = collection.find({"0d序号": str(result_answer.get('_id'))}).count()
        if c:
            self.logger.info("============ delete: %s ============" % str(temp_aid))
            collection.delete_many({"0d序号": str(result_answer.get('_id'))})
        self.logger.info("********==== handle: %s ====********" % str(temp_aid))
        result = collection.insert_one(temp_struct_data)
        if result:
            return "success"
        return "false"

        #except Exception as e:
        #    self.logger.warning("mongo insert Exception eg: %s", e)
        #    temp_data_false = {
        #        "pid": pid,
        #        "aid": aid
        #    }
        #    dev_excel_mapping = "insert_errer"
        #    getattr(self.mongo_collection_edy_insert, dev_excel_mapping).insert_one(temp_data_false)
        #    return "false"
