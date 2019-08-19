# -*- coding: utf-8 -*-
# @Time    : 2019/8/17 17:06
# @Author  : liangriyu

import datetime

import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
import pandas as pd

class PymysqlPool(object):

    def __init__(self, host, port, user, passwd, db=None, charset="utf8", mincached=1, maxcached=20):
        self.pool = PooledDB(creator=pymysql,
                          mincached=mincached,
                          maxcached=maxcached,
                          host=host,
                          port=int(port),
                          user=user,
                          passwd=passwd,
                          db=db,
                          use_unicode=True,  # use_unicode=False时conversion from bytes to Decimal is not supported
                          charset=charset,
                          cursorclass=DictCursor)

    def getConn(self):
        return Pymysql(self.pool)

    def close(self):
        self.pool.close()



class Pymysql(object):

    def __init__(self, pool):
        if not isinstance(pool, PooledDB):
            raise Exception("mysql pool type must be PooledDB!")
        self._conn = pool.connection()
        self._cursor = self._conn.cursor()

    def getAll(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)

        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = []
        return result

    def getOne(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result dict/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    def getMany(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = []
        return result

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def insertMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def insert(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def updateMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()

    def pandas_read(self,sql, index_col=None, coerce_float=False, params=None,
             parse_dates=None, columns=None, chunksize=None):
        """
        读取数据返回dataframe
        :param sql:
        :param index_col:
        :param coerce_float:
        :param params:
        :param parse_dates:
        :param columns:
        :param chunksize:
        :return:
        """
        return pd.read_sql(sql, con=self._conn, index_col=index_col, coerce_float=coerce_float, params=params,
             parse_dates=parse_dates, columns=columns, chunksize=chunksize)

    def pandas_write(self, table_name, data_frame, bacth_size=1000, update=False, update_keys=[], primary_key=None):
        """
        持久化dataframe
        当update=True时，根据update_key指定的列作为条件更新。条件最好为主键
        :param table_name:
        :param data_frame:
        :param bacth_size:
        :param update:
        :param update_keys:
        :return:
        """
        if (not data_frame.empty) and (type(data_frame) ==pd.DataFrame):
            cols = data_frame.columns.values.tolist()
            #找出日期时间类型
            for k,v in data_frame.iloc[0,:].items():
                if isinstance(v, datetime.date):
                    data_frame[k] = data_frame[k].astype('str')
                elif isinstance(v, datetime.datetime):
                    data_frame[k] = data_frame[k].astype('str')
                elif isinstance(v,pd.Timedelta):#对time（mysql）类型格式化转换
                    data_frame[k] = data_frame[k].apply(lambda x :
                                                        str((datetime.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')+x)
                                                            .strftime("%H:%M:%S")))

            # 组装insert语句
            insert_cols = ','.join(cols)
            ins_sql = "insert into " + table_name + "(" + insert_cols + ") values("
            for i in range(len(cols)):
                if i == 0:
                    ins_sql += "%s"
                else:
                    ins_sql += ",%s"

            ins_sql += ")"
            update_list = []
            insert_list = []
            if update and len(update_keys)>0:
                # 组装update语句
                upd_sql = "update " + table_name + " set "
                where = " where 1=1"
                for col in cols:
                    if col in update_keys:
                        where += " and " + col + "=%s"
                    else:
                        upd_sql += col + "=%s,"
                # where=" where"+where[4:]

                sel_key = ",".join(update_keys)
                if primary_key and primary_key not in update_keys:
                    sel_key=sel_key +","+str(primary_key)
                    where= where+ " and " + str(primary_key) + "=%s"
                upd_sql = upd_sql[:-1] + where
                for index, row in data_frame.iterrows():
                    #根据update_key查询是否存在
                    sel = "select "+sel_key +" from "+ table_name+" where 1=1"
                    sel_params = []
                    for key in update_keys:
                        sel += " and " + key + "=%s"
                        sel_params.append(row[key])
                    sel += " limit 1"
                    rs = self.getOne(sel,sel_params)
                    #若存在则更新
                    if rs:
                        update_set = []
                        update_where = []
                        for col in cols:
                            if col in update_keys:
                                update_where.append(row[col])
                            else:
                                update_set.append(row[col])
                        if primary_key and primary_key not in update_keys:
                            update_where.append(rs[str(primary_key)])
                        update_params = update_set+update_where
                        update_list.append(update_params)
                    else:
                        insert_list.append(row.tolist())

                if len(update_list) > 0:
                    bacth = len(update_list) // bacth_size + 1
                    for j in range(bacth):
                        params = update_list[j * bacth_size:(j + 1) * bacth_size]
                        self.updateMany(upd_sql, params)
            elif not update:
                insert_list = data_frame.values.tolist()
            if len(insert_list) > 0:
                bacth = len(insert_list)//bacth_size + 1
                for j in range(bacth):
                    params = insert_list[j*bacth_size:(j+1)*bacth_size]
                    self.insertMany(ins_sql,params)





