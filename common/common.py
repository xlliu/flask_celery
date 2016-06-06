# -*- coding: utf-8 -*-

"""
格式化表字段
"""


def split_title_list(title):
    if title == "id":
        return "`id` varchar(40) NOT NULL DEFAULT ''"
    elif title == "uid":
        return "`uid` varchar(40) NOT NULL DEFAULT '0'"
    elif title == "starttime":
        return "`starttime` int(11) NOT NULL DEFAULT '0'"
    elif title == "endtime":
        return "`endtime` int(11) NOT NULL DEFAULT '0'"
    else:
        return title+" text NOT NULL"

"""
过滤所有不含answer_*的值
"""


def filter_no_answer(dict_key):
    dict.keys()
    pass


