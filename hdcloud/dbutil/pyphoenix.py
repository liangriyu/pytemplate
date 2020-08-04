import os

import pandas as pd
from DBUtils.PooledDB import PooledDB
from hdcloud.dbutil.db import phoenixdb, jphoenix


class PyPhoenixPool(object):

    def __init__(self, host, port, user="", passwd="", mapping="true", jars=None, mincached=1, maxcached=20):
        url='jdbc:phoenix:%s:%s' % (host,port)
        driver_args = {
            'user': user,
            'passwd': passwd,
            'phoenix.schema.isNamespaceMappingEnabled': mapping
        }
        if not jars:
            lid_dir=os.path.abspath(os.path.dirname(__file__))[:-6]+"libs/"
            jars = lid_dir+"phoenix-4.14.0-cdh5.14.2-client.jar"
        self.pool = PooledDB(creator=jphoenix,
                             mincached=int(mincached),
                             maxcached=int(maxcached),
                             url=url,
                             jclassname="org.apache.phoenix.jdbc.PhoenixDriver",
                             driver_args=driver_args,
                             jars=jars)

    def getConn(self):
        return PyPhoenix(self.pool)

    def close(self):
        self.pool.close()




class PyPhoenixThinPool(object):
    def __init__(self, url=None, max_retries=None, mincached=1, maxcached=20,time_out=None):
        if not url:
            raise Exception("phoenix连接地址不能为空！")
        self.pool = PooledDB(creator=phoenixdb,
                          mincached=int(mincached),
                          maxcached=int(maxcached),
                          url=url,
                          max_retries=int(max_retries),
                          autocommit=True,
                          time_out=int(time_out),
                          cursor_factory=phoenixdb.DictCursor)

    def getConn(self):
        return PyPhoenix(self.pool)

    def close(self):
        self.pool.close()

class PyPhoenix(object):

    def __init__(self, pool):
        if not isinstance(pool, PooledDB):
            raise Exception("phoenix pool type must be PooledDB!")
        self._conn = pool.connection()
        self._cursor = self._conn.cursor()


    def get_all(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            self._cursor.execute(sql)
        else:
            self._cursor.execute(sql, param)
        result = self._cursor.fetchall()
        return result

    def get_one(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result dict 查询到的结果集
        """
        if param is None:
            self._cursor.execute(sql)
        else:
            self._cursor.execute(sql, param)
        result = self._cursor.fetchone()
        return result

    def get_many(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            self._cursor.execute(sql)
        else:
            self._cursor.execute(sql, param)
        result = self._cursor.fetchmany(num)
        return result

    def __query(self, sql, param=None):
        if param is None:
            self._cursor.execute(sql)
        else:
            self._cursor.execute(sql, param)
        return self._cursor.rowcount

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def insert_many(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        self._cursor.executemany(sql, values)
        return self._cursor.rowcount

    def insert(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def update_many(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        self._cursor.executemany(sql, values)
        return self._cursor.rowcount

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            try:
                self._conn.rollback()
            except:
                pass

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

    def pandas_read(self, sql, index_col=None, coerce_float=False, params=None,
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

    def insert_dict(self, table_name, data_dict={}):
        """

        :param table_name:
        :param data_dict:
        :param update:
        :param update_keys:
        :param primary_key:
        :param ignore_update_key:
        :return:
        """
        if (len(data_dict) > 0) and (type(data_dict) == dict):
            cols = list(data_dict.keys())
            # 组装insert语句
            insert_cols = '\",\"'.join(cols)
            ins_sql = "upsert into " + table_name + "(\"" + insert_cols + "\") values("
            for i in range(len(cols)):
                if i == 0:
                    ins_sql += "?"
                else:
                    ins_sql += ",?"

            ins_sql += ")"
            params = []
            for col in cols:
                params.append(data_dict[col])
            if len(params) > 0:
                self.insert(ins_sql, params)

    def pandas_write(self, table_name, data_frame, bacth_size=1000, auto_commit=False):
        """
        持久化dataframe
        :param table_name:
        :param data_frame:
        :param bacth_size:
        :return:
        """
        if (not data_frame.empty) and (type(data_frame) == pd.DataFrame):
            cols = data_frame.columns.values.tolist()
            # 组装insert语句
            insert_cols = '\",\"'.join(cols)
            ins_sql = "upsert into " + table_name + "(\"" + insert_cols + "\") values("
            for i in range(len(cols)):
                if i == 0:
                    ins_sql += "?"
                else:
                    ins_sql += ",?"
            ins_sql += ")"
            params_list = data_frame.values.tolist()
            if len(params_list) > 0:
                bacth = len(params_list) // bacth_size + 1
                for j in range(bacth):
                    params = params_list[j * bacth_size:(j + 1) * bacth_size]
                    self.insert_many(ins_sql, params)
                    if auto_commit:
                        self.end()
