# -*- coding:utf-8 -*-
# __author__ = 'gupan'

def create_sql(table, data):
    sql = "UPDATE %s SET data = update_obj WHERE name = %s"%(table, data)
    return sql