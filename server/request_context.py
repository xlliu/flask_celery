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
        set_mongo_conn_edy_insert = mongodb_conn("10.10.0.2", 27017, "xyt_survey_data_two", flag=0)
        set_mongo_conn_edy_spss_format_insert = mongodb_conn("10.10.0.2", 27017, "xyt_survey_data_two_spss_format", flag=0)
        set_mongo_conn_edy_spss_insert = mongodb_conn("10.10.0.2", 27017, "xyt_survey_data_two_spss", flag=0)
        # set_mongo_conn_edy = mongodb_conn("120.131.70.8", 27017, "xyt_survey_survey", flag=1)
        # set_mongo_conn_edy = mongodb_conn("127.0.0.1", 27017, "xyt_survey")
        self.get_mongo_conn_edy = set_mongo_conn_edy.get_conn()
        self.get_mongo_conn_edy_insert = set_mongo_conn_edy_insert.get_conn()
        self.get_mongo_conn_edy_format_insert = set_mongo_conn_edy_spss_format_insert.get_conn()
        self.get_mongo_conn_edy_spss_insert = set_mongo_conn_edy_spss_insert.get_conn()
        self.mongo_collection_edy = set_mongo_conn_edy.get_db()
        self.mongo_collection_edy_insert = set_mongo_conn_edy_insert.get_db()
        self.mongo_collection_edy_spss_format_insert = set_mongo_conn_edy_spss_format_insert.get_db()
        self.mongo_collection_edy_spss_insert = set_mongo_conn_edy_spss_insert.get_db()
        
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
        
    def answers_action_spss(self, aid):
        try:
            document_answer, document_question, document_question_struct, document_option, document_option_matrix, document_project = self.init_collection()
            self.handle_data_spss(aid, document_answer, document_question, document_question_struct, document_option,document_option_matrix, document_project)
        finally:
            self.close_connector()
        
    def question_action_spss(self, pid, limit_num, skip_num):
        temp_id = {'project_id': pid}
        # 初始化数据库
        document_answer, document_question, document_question_struct, document_option, document_option_matrix, document_project = self.init_collection()
        rdata = document_answer.find(temp_id, no_cursor_timeout=True).limit(limit_num).skip(skip_num)

        num = skip_num
        # gc.disable()
        for answer in rdata:
            num += 1
            self.logger.info("PROJECT_ACTION==> for project_data_spss in a_num: %d, pid : %s, aid: %s" %(num, pid, answer["_id"]))
            #     continue
            try:
                self.handle_data_spss(answer["_id"], document_answer, document_question, document_question_struct,
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
        option_titles = []
        q_cid = []
        for question in p_struct.get("questionpage_list"):
            for q_struct in question.get("question_list"):
                question_type = q_struct.get("question_type")
                q_options = q_struct.get("option_list")
                q_custom = q_struct.get("custom_attr")
                q_title_temp = q_struct.get("title")
                q_title_temp = html2text.html2text(q_title_temp).replace("\n", "")
                q_title = q_title_temp

                if question_type == 70:
                    pass
                if question_type in (2,):
                    q_cid_t = q_struct.get("cid")
                    option_titles_min = []
                    temp_struct_data.append(q_title)
                    for qos in q_options:
                        otitle = qos.get("title")
                        option_titles_min.append(otitle)
                    q_cid.append(q_cid_t)
                    option_titles.append(option_titles_min)

                if question_type in (3,):
                    q_cid_t = q_struct.get("cid")
                    option_titles_min = []
                    temp_struct_data.append(q_title)
                    for qos in q_options:
                        otitle = qos.get("title")
                        option_titles_min.append(otitle)
                    q_cid.append(q_cid_t)
                    option_titles.append(option_titles_min)

                if question_type in (6,):
                    q_cid_t = q_struct.get("cid")
                    option_titles_min = []
                    temp_struct_data.append(q_title)
                    for qos in q_options:
                        option_titles_min.append([])
                    q_cid.append(q_cid_t)
                    option_titles.append(option_titles_min)

                if question_type in (4,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("matrixrow_list"):
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        option_titles_min = []
                        q_title_t = q_title +"%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        for qos in q_options:
                            otitle = qos.get("title")
                            option_titles_min.append(otitle)
                        q_cid.append(q_cid_t)
                        option_titles.append(option_titles_min)
                        
                if question_type in (5,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("matrixrow_list"):
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        option_titles_min = []
                        q_title_t = q_title +"%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        for qos in q_options:
                            otitle = qos.get("title")
                            option_titles_min.append(otitle)
                        q_cid.append(q_cid_t)
                        option_titles.append(option_titles_min)

                if question_type in (8,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("option_list"):
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        option_titles_min = []
                        q_title_t = q_title + "%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        for qos in q_options:
                            otitle = qos.get("title")
                            option_titles_min.append(otitle)
                        q_cid.append(q_cid_t)
                        option_titles.append(option_titles_min)
                        
                if question_type in (50,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("option_list"):
                        option_titles_min = []
                        q_title_t = q_title + "%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        min_max = xrange(int(q_custom.get("min_answer_num", "1")), int(q_custom.get("max_answer_num"))+1)
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        q_cid.append(q_cid_t)
                        option_titles_min.extend(min_max)
                        option_titles_min_v = map(lambda x: str(x), option_titles_min)
                        option_titles.append(option_titles_min)
                        option_titles.append(option_titles_min_v)
                        
                if question_type in (60,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("option_list"):
                        option_titles_min = []
                        q_title_t = q_title + "%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        for qos in q_options:
                            option_titles_min.append([])
                        q_cid.append(q_cid_t)
                        option_titles.append(option_titles_min)
                        
                if question_type in (95,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("option_list"):
                        option_titles_min = []
                        q_title_t = q_title + "%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        for qos in q_options:
                            option_titles_min.append([])
                        q_cid.append(q_cid_t)
                        option_titles.append(option_titles_min)

                if question_type in (7,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for qm_ in q_struct.get("matrixrow_list"):
                        omcid = qm_.get("cid")
                        for qo_ in q_struct.get("option_list"):
                            option_titles_min = []
                            q_title_t = html2text.html2text(q_title + "%s%s" % (qm_.get("title"), qo_.get("title"))).replace("\n", "")
                            temp_struct_data.append(q_title_t)
                            min_max = xrange(int(q_custom.get("min_answer_num", "1")), int(q_custom.get("max_answer_num"))+1)
                            ocid = qo_.get("cid")
                            q_cid_t = q_cid_t_t + omcid + ocid
                            q_cid.append(q_cid_t)
                            option_titles_min.extend(min_max)
                            option_titles_min_v = map(lambda x: str(x), option_titles_min)
                            option_titles.append(option_titles_min)
                            option_titles.append(option_titles_min_v)

                if question_type in (100,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for qm_ in q_struct.get("matrixrow_list"):
                        omcid = qm_.get("cid")
                        for qo_ in q_struct.get("option_list"):
                            option_titles_min = []
                            q_title_t = html2text.html2text(q_title + "%s%s" % (qm_.get("title"), qo_.get("title"))).replace("\n", "")
                            temp_struct_data.append(q_title_t)
                            ocid = qo_.get("cid")
                            q_cid_t = q_cid_t_t + omcid + ocid
                            for qos in q_options:
                                option_titles_min.append([])
                            q_cid.append(q_cid_t)
                            option_titles.append(option_titles_min)

        return temp_struct_data, option_titles, q_cid, lag
        
        
    def generator_option_spss(self, pid, document_project, document_option):
        set_value_option = getattr(self.mongo_collection_edy_spss_insert, "xyt_survey_option_set_value")
        p_struct = document_project.find_one({"_id": ObjectId(pid)})

        lag = p_struct.get("change_log", 0)
        temp_struct_data = []
        option_titles = []
        q_cid = []
        q_type = []
        for question in p_struct.get("questionpage_list"):
            for q_struct in question.get("question_list"):
                question_type = q_struct.get("question_type")
                q_options = q_struct.get("option_list")
                q_custom = q_struct.get("custom_attr")
                q_title_temp = q_struct.get("title")
                q_title_temp = html2text.html2text(q_title_temp).replace("\n", "")
                q_title = q_title_temp

                if question_type == 70:
                    pass
                if question_type in (2,):
                    q_cid_t = q_struct.get("cid")
                    option_titles_key = []
                    option_titles_val = []
                    option_titles_min = [option_titles_key, option_titles_val]
                    temp_struct_data.append(q_title)
                    n = 1
                    for qos in q_options:
                        otitle = qos.get("title")
                        oid = qos.get("_id")
                        ovalue = document_option.find_one({"_id": ObjectId(oid)})
                        ovalue["ovalue"] = n
                        set_value_option.save(ovalue)
                        option_titles_key.append(n)
                        option_titles_val.append(otitle)
                        n += 1
                    q_cid.append(q_cid_t)
                    q_type.append("int")
                    option_titles.append(option_titles_min)

                if question_type in (3,):
                    q_cid_t = q_struct.get("cid")
                    option_titles_key = []
                    option_titles_val = []
                    option_titles_min = [option_titles_key, option_titles_val]
                    temp_struct_data.append(q_title)
                    n = 1
                    for qos in q_options:
                        oid = qos.get("_id")
                        ovalue = document_option.find_one({"_id": ObjectId(oid)})
                        ovalue["ovalue"] = str(n)
                        set_value_option.save(ovalue)
                        otitle = qos.get("title")
                        option_titles_key.append(str(n))
                        option_titles_val.append(otitle)
                        n += 1
                    q_cid.append(q_cid_t)
                    q_type.append("string")
                    option_titles.append(option_titles_min)

                if question_type in (6,):
                    q_cid_t = q_struct.get("cid")
                    option_titles_min = None
                    temp_struct_data.append(q_title)
                    for qos in q_options:
                        oid = qos.get("_id")
                        ovalue = document_option.find_one({"_id": ObjectId(oid)})
                        set_value_option.save(ovalue)
                        # option_titles_min.append(None)
                    q_cid.append(q_cid_t)
                    q_type.append("string")
                    option_titles.append(option_titles_min)

                if question_type in (4,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("matrixrow_list"):
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        option_titles_key = []
                        option_titles_val = []
                        option_titles_min = [option_titles_key, option_titles_val]
                        q_title_t = q_title + "%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        n = 1
                        for qos in q_options:
                            oid = qos.get("_id")
                            val = set_value_option.find_one({"_id": ObjectId(oid)})
                            if not val:
                                ovalue = document_option.find_one({"_id": ObjectId(oid)})
                                ovalue["ovalue"] = n
                                set_value_option.save(ovalue)
                            otitle = qos.get("title")
                            option_titles_key.append(n)
                            option_titles_val.append(otitle)
                            n += 1
                        q_cid.append(q_cid_t)
                        q_type.append("int")
                        option_titles.append(option_titles_min)

                if question_type in (5,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("matrixrow_list"):
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        option_titles_key = []
                        option_titles_val = []
                        option_titles_min = [option_titles_key, option_titles_val]
                        q_title_t = q_title + "%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        n = 1
                        for qos in q_options:
                            oid = qos.get("_id")
                            val = set_value_option.find_one({"_id": ObjectId(oid)})
                            if not val:
                                ovalue = document_option.find_one({"_id": ObjectId(oid)})
                                ovalue["ovalue"] = str(n)
                                set_value_option.save(ovalue)
                            otitle = qos.get("title")
                            option_titles_key.append(str(n))
                            option_titles_val.append(otitle)
                            n += 1
                        q_cid.append(q_cid_t)
                        q_type.append("string")
                        option_titles.append(option_titles_min)

                if question_type in (8,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("option_list"):
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        option_titles_min = None
                        q_title_t = q_title + "%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        for qos in q_options:
                            oid = qos.get("_id")
                            ovalue = document_option.find_one({"_id": ObjectId(oid)})
                            set_value_option.save(ovalue)
                            # otitle = qos.get("title")
                            # option_titles_min.append(None)
                        q_cid.append(q_cid_t)
                        q_type.append("string")
                        option_titles.append(option_titles_min)

                if question_type in (50,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("option_list"):

                        q_title_t = q_title + "%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        min_max = xrange(int(q_custom.get("min_answer_num", "1")),
                                         int(q_custom.get("max_answer_num")) + 1)
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        q_cid.append(q_cid_t)
                        q_type.append("int")
                        option_titles_min.extend(min_max)
                        option_titles_min_v = map(lambda x: str(x), option_titles_min)
                        option_titles.append(option_titles_min)
                        option_titles.append(option_titles_min_v)

                if question_type in (60,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("option_list"):
                        option_titles_key = []
                        option_titles_val = []
                        option_titles_min = [option_titles_key, option_titles_val]
                        q_title_t = q_title + "%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        n = 1
                        for qos in q_options:
                            otitle = qos.get("title")
                            oid = qos.get("_id")
                            val = set_value_option.find_one({"_id": ObjectId(oid)})
                            if not val:
                                ovalue = document_option.find_one({"_id": ObjectId(oid)})
                                ovalue["ovalue"] = n
                                set_value_option.save(ovalue)
                            option_titles_key.append(n)
                            option_titles_val.append(otitle)
                            n += 1
                        q_cid.append(q_cid_t)
                        q_type.append("int")
                        option_titles.append(option_titles_min)

                if question_type in (95,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for q_ in q_struct.get("option_list"):
                        option_titles_min = None
                        q_title_t = q_title + "%s" % html2text.html2text(q_.get("title")).replace("\n", "")
                        temp_struct_data.append(q_title_t)
                        ocid = q_.get("cid")
                        q_cid_t = q_cid_t_t + ocid
                        for qos in q_options:
                            oid = qos.get("_id")
                            val = set_value_option.find_one({"_id": ObjectId(oid)})
                            if not val:
                                ovalue = document_option.find_one({"_id": ObjectId(oid)})
                                set_value_option.save(ovalue)
                            # option_titles_min.append(None)
                        q_cid.append(q_cid_t)
                        q_type.append("string")
                        option_titles.append(option_titles_min)

                if question_type in (7,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for qm_ in q_struct.get("matrixrow_list"):
                        omcid = qm_.get("cid")
                        for qo_ in q_struct.get("option_list"):
                            option_titles_min = []
                            q_title_t = html2text.html2text(
                                    q_title + "%s%s" % (qm_.get("title"), qo_.get("title"))).replace("\n", "")
                            temp_struct_data.append(q_title_t)
                            min_max = xrange(int(q_custom.get("min_answer_num", "1")),
                                             int(q_custom.get("max_answer_num")) + 1)
                            ocid = qo_.get("cid")
                            q_cid_t = q_cid_t_t + omcid + ocid
                            q_cid.append(q_cid_t)
                            q_type.append("int")
                            option_titles_min.extend(min_max)
                            option_titles_min_v = map(lambda x: str(x), option_titles_min)
                            option_titles.append(option_titles_min)
                            option_titles.append(option_titles_min_v)

                if question_type in (100,):
                    q_cid_t = q_struct.get("cid")
                    q_cid_t_t = q_cid_t
                    for qm_ in q_struct.get("matrixrow_list"):
                        omcid = qm_.get("cid")
                        for qo_ in q_struct.get("option_list"):
                            option_titles_min = None
                            q_title_t = html2text.html2text(
                                    q_title + "%s%s" % (qm_.get("title"), qo_.get("title"))).replace("\n", "")
                            temp_struct_data.append(q_title_t)
                            ocid = qo_.get("cid")
                            q_cid_t = q_cid_t_t + omcid + ocid
                            for qos in q_options:
                                oid = qos.get("_id")
                                ovalue = document_option.find_one({"_id": ObjectId(oid)})
                                set_value_option.save(ovalue)
                                # option_titles_min.append(None)
                            q_cid.append(q_cid_t)
                            q_type.append("string")
                            option_titles.append(option_titles_min)

        return temp_struct_data, option_titles, q_cid, q_type, lag
        
        
    def generator_options(self, pid, document_project):
        pass
        
        
    def handle_data(self, aid, document_answer, document_question, document_question_struc, document_option,
                    document_option_matrix, document_project):
        temp_aid = {"_id": ObjectId(str(aid))}
        #self.logger.info("inot func handle_data, temp_aid: %s" %temp_aid)

        temp_struct_data = OrderedDict()
        result_answer = document_answer.find_one(temp_aid)
        pid = result_answer.get('project_id')
        title_m, option_t, q_cid, lag = self.generator_title(pid, document_project)
        tsd = {}
        tsd[u"开始时间"] = result_answer.get('starttime')
        tsd[u"结束时间"] = result_answer.get('endtime')
        tsd[u"序号"] = str(result_answer.get('_id'))
        tsd[u"用户"] = result_answer.get('uuid')
        tsd[u"版本"] = lag
        temp_struct_data = OrderedDict(temp_struct_data.items()+zip(q_cid, [""]*len(q_cid)))
        # temp_struct_data[u"schoolCode"] = result_answer.get('schoolCode', 'None')
        answers = result_answer.get('answers')
        if not answers:
            return

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
                    q_struct = document_question.find_one(temp_qid)
                    if not q_struct:
                        temp_qid = {"_id": str(v)}
                        q_struct = document_question.find_one(temp_qid)
                        if not q_struct:
                            self.logger.info("next return")
                            return
                    # q_title_temp_kk = q_struct.get('title')
                    # q_title_temp_kk = html2text.html2text(q_title_temp_kk)
                    # q_title = q_title_temp_kk
                    # q_title = q_title.replace(r".", "d")
                    
                    q_title_temp_kk = q_struct.get('cid')
                    q_title = q_title_temp_kk
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
                        temp_struct_data[q_title] = html2text.html2text(a_value)
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
                        temp_struct_data[q_title] = html2text.html2text(",".join(a_value))
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
                            q_title_temp = document_option_matrix.find_one({"_id": ObjectId(str(k_4))}).get('cid')
                            temp_value_id = {"_id": ObjectId(str(v_4[0]))}
                            a_context = document_option.find_one(temp_value_id)
                            a_value = a_context.get('title')

                            #temp_struct_data[
                        #        q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = html2text.html2text(a_value)
                            temp_struct_data[
                                q_title + "%s" % q_title_temp] = html2text.html2text(a_value)
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
                            q_title_temp = document_option_matrix.find_one({"_id": ObjectId(str(k_5))}).get('cid')
                            a_value_temp = []
                            for v_5v in v_5:
                                temp_value_id = {"_id": ObjectId(str(v_5v[0]))}
                                a_context = document_option.find_one(temp_value_id)
                                a_value_temp.append(a_context.get('title'))
                            a_value = a_value_temp

                            #temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = html2text.html2text(",".join(a_value))
                            temp_struct_data[q_title + "%s" % q_title_temp] = html2text.html2text(",".join(a_value))
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
                            q_title_temp = document_option.find_one({"_id": ObjectId(str(k_60)[7:] if "option_" == str(k_60)[0:7] else str(k_60))}).get('cid')
                            temp_struct_data[q_title + "%s" % q_title_temp] = v_60[0]
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
                            q_title_temp = document_option.find_one({"_id": ObjectId(str(k_50))}).get('cid')
                            temp_struct_data[q_title + "%s" % q_title_temp] = v_50[0]
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
                            q_title_temp_1 = document_option_matrix.find_one({"_id": ObjectId(str(k_7))}).get('cid')
                            for k_7k, v_7v in v_7.items():
                                q_title_temp_2 = document_option.find_one({"_id": ObjectId(str(k_7k))}).get('cid')

                                #temp_struct_data[html2text.html2text(q_title + "_%s_%s" % (q_title_temp_1,
                                #                                       q_title_temp_2)).replace(r".", "d")] = html2text.html2text(v_7v)
                                temp_struct_data[q_title + "%s%s" % (q_title_temp_1,
                                                                       q_title_temp_2)] = html2text.html2text(v_7v)
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
                        temp_struct_data[q_title] = html2text.html2text(a_value)
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
                            q_title_temp = document_option.find_one({"_id": ObjectId(str(k_95[0:-5]))}).get('cid')

                            #temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = html2text.html2text(v_95)
                            temp_struct_data[q_title + "%s" % q_title_temp] = html2text.html2text(v_95)
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
                            q_title_temp_1 = document_option_matrix.find_one({"_id": ObjectId(str(k_100))}).get('cid')
                            for k_100k, v_100v in v_100.items():
                                q_title_temp_2 = document_option.find_one({"_id": ObjectId(str(k_100k))}).get('cid')

                                #temp_struct_data[
                                #    html2text.html2text(q_title + "_%s_%s" % (q_title_temp_1,
                                #                          q_title_temp_2)).replace(r".", "d")] = html2text.html2text(v_100v)
                                temp_struct_data[
                                    q_title + "%s%s" % (q_title_temp_1,q_title_temp_2)] = html2text.html2text(v_100v)
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
                            q_title_temp = document_option.find_one({"_id": ObjectId(str(k_8[0:-5]))}).get('cid')
                            temp_struct_data[q_title + "%s" % (q_title_temp)] = html2text.html2text(v_8)
                        break
                    if None == question_type:
                        raise "====Question_type is None, Exception===="
                    break
        dev_excel_mapping = "pid_%s" % pid
        collection = getattr(self.mongo_collection_edy_insert, dev_excel_mapping)
        # collection = getattr(self.mongo_collection, dev_excel_mapping)
        c = collection.find({"序号": str(result_answer.get('_id'))}).count()
        if c:
            self.logger.info("============ delete: %s ============" % str(temp_aid))
            collection.delete_many({"序号": str(result_answer.get('_id'))})
        self.logger.info("********==== handle: %s ====********" % str(temp_aid))
        #k_list = temp_struct_data.keys()
        v_list = temp_struct_data.values()
        tsd["k_pid"] = q_cid
        tsd["v_list"] = v_list
        #temp_struct_data["options"] = option_t
        tsd["k_list"] = title_m
        result = collection.insert_one(tsd)
        if result:
           return "success"
        return "false"
        
        
    def handle_data_spss(self, aid, document_answer, document_question, document_question_struc, document_option,
                    document_option_matrix, document_project):
        temp_aid = {"_id": ObjectId(str(aid))}
        # self.logger.info("inot func handle_data, temp_aid: %s" %temp_aid)

        temp_struct_data = OrderedDict()
        result_answer = document_answer.find_one(temp_aid)
        pid = result_answer.get('project_id')
        # 查找重复项
        # from collections import Counter
        title_m, option_t, q_cid, q_type, lag = self.generator_option_spss(pid, document_project, document_option)
        set_value_option = getattr(self.mongo_collection_edy_spss_insert, "xyt_survey_option_set_value")
        tsd = {}
        # Counter(q_cid)
        # print [qc for qc in q_cid if q_cid.count(qc)==2]
        #
        # print 'dfsfdsfdsfsdfdsf'
        tsd[u"开始时间"] = result_answer.get('starttime')
        tsd[u"结束时间"] = result_answer.get('endtime')
        tsd[u"序号"] = str(result_answer.get('_id'))
        tsd[u"用户"] = result_answer.get('uuid')
        tsd[u"版本"] = lag
        temp_struct_data = OrderedDict(temp_struct_data.items() + zip(q_cid, [""] * len(q_cid)))
        # temp_struct_data[u"schoolCode"] = result_answer.get('schoolCode', 'None')
        answers = result_answer.get('answers')
        if not answers:
            return

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
                    q_struct = document_question.find_one(temp_qid)
                    if not q_struct:
                        temp_qid = {"_id": str(v)}
                        q_struct = document_question.find_one(temp_qid)
                        if not q_struct:
                            self.logger.info("next return")
                            return
                    # q_title_temp_kk = q_struct.get('title')
                    # q_title_temp_kk = html2text.html2text(q_title_temp_kk)
                    # q_title = q_title_temp_kk
                    # q_title = q_title.replace(r".", "d")

                    q_title_temp_kk = q_struct.get('cid')
                    q_title = q_title_temp_kk
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
                        a_context = set_value_option.find_one(temp_value_id)
                        a_value = a_context.get('ovalue')
                        # temp_struct_data[q_title] = html2text.html2text(a_value)
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
                            a_context = set_value_option.find_one(temp_value_id)
                            a_value_temp.append(a_context.get('ovalue'))
                        a_value = a_value_temp
                        # temp_struct_data[q_title] = html2text.html2text(",".join(a_value))
                        temp_struct_data[q_title] = html2text.html2text(",".join([str(v) for v in a_value]))
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
                            q_title_temp = document_option_matrix.find_one({"_id": ObjectId(str(k_4))}).get('cid')
                            temp_value_id = {"_id": ObjectId(str(v_4[0]))}
                            a_context = set_value_option.find_one(temp_value_id)
                            a_value = a_context.get('ovalue')

                            # temp_struct_data[
                            #        q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = html2text.html2text(a_value)
                            temp_struct_data[
                                q_title + "%s" % q_title_temp] = a_value
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
                            q_title_temp = document_option_matrix.find_one({"_id": ObjectId(str(k_5))}).get('cid')
                            a_value_temp = []
                            for v_5v in v_5:
                                temp_value_id = {"_id": ObjectId(str(v_5v[0]))}
                                a_context = set_value_option.find_one(temp_value_id)
                                a_value_temp.append(a_context.get('ovalue'))
                            a_value = a_value_temp

                            # temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = html2text.html2text(",".join(a_value))
                            temp_struct_data[q_title + "%s" % q_title_temp] = html2text.html2text(",".join([str(v) for v in a_value]))
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
                            q_title_temp = document_option.find_one(
                                    {"_id": ObjectId(str(k_60)[7:] if "option_" == str(k_60)[0:7] else str(k_60))}).get(
                                    'cid')
                            temp_struct_data[q_title + "%s" % q_title_temp] = v_60[0]
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
                            q_title_temp = document_option.find_one({"_id": ObjectId(str(k_50))}).get('cid')
                            temp_struct_data[q_title + "%s" % q_title_temp] = v_50[0]
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
                            q_title_temp_1 = document_option_matrix.find_one({"_id": ObjectId(str(k_7))}).get('cid')
                            for k_7k, v_7v in v_7.items():
                                q_title_temp_2 = document_option.find_one({"_id": ObjectId(str(k_7k))}).get('cid')

                                # temp_struct_data[html2text.html2text(q_title + "_%s_%s" % (q_title_temp_1,
                                #                                       q_title_temp_2)).replace(r".", "d")] = html2text.html2text(v_7v)
                                temp_struct_data[q_title + "%s%s" % (q_title_temp_1,
                                                                     q_title_temp_2)] = html2text.html2text(v_7v)
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

                        # temp_struct_data[q_title] = html2text.html2text(a_value)
                        temp_struct_data[q_title] = html2text.html2text(a_value)
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
                            q_title_temp = document_option.find_one({"_id": ObjectId(str(k_95[0:-5]))}).get('cid')

                            # temp_struct_data[q_title + "_%s" % html2text.html2text(q_title_temp).replace(r".", "d")] = html2text.html2text(v_95)
                            temp_struct_data[q_title + "%s" % q_title_temp] = html2text.html2text(v_95)
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
                            q_title_temp_1 = document_option_matrix.find_one({"_id": ObjectId(str(k_100))}).get('cid')
                            for k_100k, v_100v in v_100.items():
                                q_title_temp_2 = document_option.find_one({"_id": ObjectId(str(k_100k))}).get('cid')

                                # temp_struct_data[
                                #    html2text.html2text(q_title + "_%s_%s" % (q_title_temp_1,
                                #                          q_title_temp_2)).replace(r".", "d")] = html2text.html2text(v_100v)
                                temp_struct_data[
                                    q_title + "%s%s" % (q_title_temp_1, q_title_temp_2)] = html2text.html2text(v_100v)
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
                            q_title_temp = document_option.find_one({"_id": ObjectId(str(k_8[0:-5]))}).get('cid')
                            temp_struct_data[q_title + "%s" % (q_title_temp)] = html2text.html2text(v_8)
                        break
                    if None == question_type:
                        raise "====Question_type is None, Exception===="
                    break
        dev_excel_mapping = "pid_%s" % pid
        collection = getattr(self.mongo_collection_edy_spss_format_insert, dev_excel_mapping)
        # collection = getattr(self.mongo_collection, dev_excel_mapping)
        c = collection.find({"序号": str(result_answer.get('_id'))}).count()
        if c:
            self.logger.info("============ delete: %s ============" % str(temp_aid))
            collection.delete_many({"序号": str(result_answer.get('_id'))})
        self.logger.info("********==== handle: %s ====********" % str(temp_aid))
        # k_list = temp_struct_data.keys()
        v_list = temp_struct_data.values()
        tsd[u"k_pid"] = q_cid
        tsd[u"v_list"] = v_list
        tsd[u"options"] = option_t
        tsd[u"k_list"] = title_m
        tsd[u"q_type"] = q_type
        result = collection.save(tsd)
        if result:
            return "success"
        return "false"