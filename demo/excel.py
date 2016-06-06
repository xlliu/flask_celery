# encoding: utf-8


"""
@version: ??
@author: xlliu
@contact: liu.xuelong@163.com
@site: https://github.com/xlliu
@software: PyCharm
@file: excel.py
@time: 2016/4/26 18:15
"""
def post():
    return send_from_directory(filepath, filename, as_attachment=True,
          attachment_filename=begin_date + '--' + end_date + u'房源详细表.xlsx')

    filepath = appconfig.EXCEL_FILEPATH
    workbook = xlsxwriter.Workbook(filepath + filetime + 'khtjb.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, unicode('日期', 'utf-8'))
    worksheet.write(0, 1, unicode('客户总数', 'utf-8'))
    worksheet.write(0, 2, unicode('新增客户数', 'utf-8'))
    worksheet.write(0, 3, unicode('操作人', 'utf-8'))
    worksheet.write(0, 4, unicode('新增判重客户数', 'utf-8'))
    worksheet.write(0, 5, unicode('分组', 'utf-8'))
    worksheet.write(0, 6, unicode('大区', 'utf-8'))
    worksheet.write(0, 7, unicode('城市', 'utf-8'))
    worksheet.write(0, 8, unicode('部门', 'utf-8'))
    search = CustomerStatistics.select().where(dy).order_by(CustomerStatistics.date.desc())
    row = 1
    for e in search:
        t = CommonUtils.unixtime_to_str(e.date)
        worksheet.write(row, 0, t)

    workbook.close()
    filename = filetime + 'khtjb.xlsx'
    return filename


def format_data():
        p_struct = project.find_one({"_id": ObjectId(pid)})
        question_type = None
        temp_struct_data = []
        for question in p_struct.get("questionpage_list"):
            for q_struct in question.get("question_list"):
                q_title = q_struct.get("title")
                if question_type == 70:
                    pass

                if question_type in (2, 3, 6):
                    temp_struct_data.append(q_title)

                if question_type in (4, 5):
                    for q_ in q_struct.get("matrixrow"):
                        q_title += "_%s" % q_.get("title")
                        temp_struct_data.append(q_title)

                if question_type in (8, 50, 60, 95):
                    for q_ in q_struct.get("option_list"):
                        q_title += "_%s" % q_.get("title")
                        temp_struct_data.append(q_title)

                if question_type in (7, 100):
                    for qm_ in q_struct.get("matrixrow"):
                        for qo_ in q_struct.get("option_list"):
                            q_title += "_%s_%s" % (qm_.get("title"), qo_.get("title"))
                        # 表格多选题5
                        # """
                        # {
                        #   "qid" : "570dda77ea1967dc608b45bb",                             //表格多选题5
                        #   "answer" : {
                        #     "570dda77ea1967dc608b45be" : [["570dda77ea1967dc608b45bc"]],  //option_matrix_id:[[option_id]]
                        #     "570dda77ea1967dc608b45bf" : [["570dda77ea1967dc608b45bc"], ["570dda77ea1967dc608b45bd"]]
                        #   }
                        # }
                        # """
                        # if question_type == 5:
                        #     for k_5, v_5 in v.items():
                        #         q_title_temp = document_option_matrix.find_one({"_id": ObjectId(str(k_5))}).get('title')
                        #         a_value_temp = []
                        #         for v_5v in v_5:
                        #             temp_value_id = {"_id": ObjectId(str(v_5v[0]))}
                        #             a_context = document_option.find_one(temp_value_id)
                        #             a_value_temp.append(a_context.get('title'))
                        #         a_value = a_value_temp
                        #         temp_struct_data[q_title + "_%s" % q_title_temp.replace(r".", "(d)")] = a_value.replace(
                        #                 r"<br>", "")
                        #     break
                        # 选择排序题60
                        # """
                        # {
                        #   "qid" : "570dda88ea1967786c8b4599",                             //选择排序题60
                        #   "answer" : {
                        #     "570dda88ea1967786c8b459b" : [NumberLong(1)],                 //[option_id]:[value]
                        #     "570dda88ea1967786c8b459a" : [NumberLong(2)]
                        #   }
                        # }
                        # """
                        # if question_type == 60:
                        #     for k_60, v_60 in v.items():
                        #         q_title_temp = document_option.find_one({"_id": ObjectId(str(k_60))}).get('title')
                        #         temp_struct_data[q_title + "_%s" % q_title_temp.replace(r".", "(d)")] = v_60[0]
                        #         # temp_struct_data[q_title+"_%s" % q_title_temp] = "类型60，矩阵跳过"
                        #     break  # 单项打分题50
                        # """
                        # {
                        #   "qid" : "570dda8eea19674b6c8b4593",                             //单项打分题50
                        #   "answer" : {
                        #     "570dda8eea19674b6c8b4594" : ["5"],                           //[option_id]:["value"]
                        #     "570dda8eea19674b6c8b4595" : ["2"]
                        #   }
                        # }
                        # """
                        # if question_type == 50:
                        #     for k_50, v_50 in v.items():
                        #         q_title_temp = document_option.find_one({"_id": ObjectId(str(k_50))}).get('title')
                        #         temp_struct_data[q_title + "_%s" % q_title_temp.replace(r".", "(d)")] = v_50[0]
                        #     break
                        # 多项打分题7
                        # """
                        # {
                        #   "qid" : "570dda95ea196739618b45d5",                             //多项打分题7
                        #   "answer" : {
                        #     "570dda95ea196739618b45d8" : {                                //option_matrix_id:{option:value}
                        #       "570dda95ea196739618b45d6" : "5",
                        #       "570dda95ea196739618b45d7" : "3"
                        #     },
                        #     "570dda95ea196739618b45d9" : {
                        #       "570dda95ea196739618b45d6" : "1",
                        #       "570dda95ea196739618b45d7" : "5"
                        #     }
                        #   }
                        # }
                        # """
                        # if question_type == 7:
                        #     for k_7, v_7 in v.items():
                        #         q_title_temp_1 = document_option_matrix.find_one({"_id": ObjectId(str(k_7))}).get('title')
                        #         for k_7k, v_7v in v_7:
                        #             q_title_temp_2 = document_option.find_one({"_id": ObjectId(str(k_7k))}).get('title')
                        #             temp_struct_data[q_title + "_%s_%s" % (q_title_temp_1.replace(r".", "(d)"),
                        #                                                    q_title_temp_2.replace(r".",
                        #                                                                           "(dian)"))] = v_7v.replace(
                        #                     r"<br>", "")
                        #     break
                        # 单项填空题6 多行文本题6
                        # """
                        # {
                        #   "qid" : "570dda9bea1967ef6b8b4592",                             //单项填空题6
                        #   "answer" : {
                        #     "570dda9bea1967ef6b8b4593_open" : "xlliu_danxiangtiankong"
                        #   }
                        # {
                        #   "qid" : "570ddaaeea19673f6c8b459f",                             //多行文本题6
                        #   "answer" : {
                        #     "570ddaaeea19673f6c8b45a0_open" : "xlliu_testtesttesttesttesttesttesttesttest"
                        #   }
                        # }
                        # """
                        # if question_type == 6:
                        #     a_value = v.values()[0]
                        #     temp_struct_data[q_title] = a_value.replace(r"<br>", "")
                        #     break
                        # 多项填空题95
                        # """
                        # {
                        #   "qid" : "570ddaa0ea1967646c8b45a6",                             //多项填空题95
                        #   "answer" : {
                        #     "570ddaa0ea1967646c8b45a7_open" : "xlliu_duoxiangtiankong",
                        #     "570ddaa0ea1967646c8b45a8_open" : "xlliu_duoxiangtiankong2"
                        #   }
                        # }
                        # """
                        # if question_type == 95:
                        #     for k_95, v_95 in v.items():
                        #         q_title_temp = document_option.find_one({"_id": ObjectId(str(k_95[0:-5]))}).get('title')
                        #         temp_struct_data[q_title + "_%s" % q_title_temp.replace(r".", "(d)")] = v_95.replace(
                        #                 r"<br>", "")
                        #     break
                        # 表格填空题100
                        # """
                        # {
                        #   "qid" : "570ddaa9ea196709618b45e1",                             //表格填空题100
                        #   "answer" : {
                        #     "570ddaa9ea196709618b45e4" : {
                        #       "570ddaa9ea196709618b45e2" : "xlliu_juzhenbiaoge1_1",
                        #       "570ddaa9ea196709618b45e3" : "xlliu_juzhenbiaoge1_2"
                        #     },
                        #     "570ddaa9ea196709618b45e5" : {
                        #       "570ddaa9ea196709618b45e2" : "xlliu_juzhenbiaoge2_1",
                        #       "570ddaa9ea196709618b45e3" : "xlliu_juzhenbiaoge2_2"
                        #     }
                        #   }
                        # }
                        # """
                        # if question_type == 100:
                        #     for k_100, v_100 in v.items():
                        #         q_title_temp_1 = document_option_matrix.find_one({"_id": ObjectId(str(k_100))}).get('title')
                        #         for k_100k, v_100v in v_100:
                        #             q_title_temp_2 = document_option.find_one({"_id": ObjectId(str(k_100k))}).get('title')
                        #             temp_struct_data[
                        #                 q_title + "_%s_%s" % (q_title_temp_1.replace(r".", "(d)"),
                        #                                       q_title_temp_2.replace(r".", "(d)"))] = v_100v.replace(
                        #                     r"<br>", "")
                        #     break
                        # """
                        # {
                        #     u'qid': u'5629abcaea1967093b8b4569',                          //生日,城市(类级联操作)
                        #     u'answer': {
                        #     u'5629abcaea1967093b8b456c_open': u'3',
                        #     u'5629abcaea1967093b8b456b_open': u'8',
                        #     u'5629abcaea1967093b8b456a_open': u'1993'
                        #     }
                        # }
                        # """
                        # if question_type == 8:
                        #     q_title_temp = []
                        #     for k_8, v_8 in v.items():
                        #         q_title_temp.append(
                        #                 document_option.find_one({"_id": ObjectId(str(k_8[0:-5]))}).get('title'))
                        #     temp_struct_data[q_title + "(%s)" % ",".join(q_title_temp)] = ",".join(v.values()).replace(
                        #             r"<br>", "")
                        #     break
                        if None == question_type:
                            raise "====Question_type is None, Exception===="
                        break
                c = collection.find({"序号": str(result_answer.get('_id'))}).count()
                if c:
                    self.logger.info("============ delete: %s ============" % str(temp_aid))
                    collection.delete_one({"序号": str(result_answer.get('_id'))})
                self.logger.info("********==== handle: %s ====********" % str(temp_aid))
                result = collection.insert_one(temp_struct_data)
                if result:
                    return "success"
                return "false"