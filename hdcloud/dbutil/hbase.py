# -*- coding: utf-8 -*-
# @Time    : 2019/8/17 17:01
# @Author  : liangriyu
import threading

import happybase
import pandas as pd



class _PyHbase(object):

    _instance_lock = threading.Lock()

    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 9090
    DEFAULT_TRANSPORT = 'buffered'
    DEFAULT_COMPAT = '0.98'
    DEFAULT_PROTOCOL = 'binary'
    DEFAULT_POOL_SIZE = 5

    # 连接池对象
    _pool = None
    _conn = None

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, timeout=None,
                 autoconnect=True, table_prefix=None,
                 table_prefix_separator=b'_', compat=DEFAULT_COMPAT,
                 transport=DEFAULT_TRANSPORT, protocol=DEFAULT_PROTOCOL, pool_size=DEFAULT_POOL_SIZE):

        self.host = host or self.DEFAULT_HOST
        self.port = port or self.DEFAULT_PORT
        self.timeout = timeout
        self.autoconnect = autoconnect
        self.table_prefix = table_prefix
        self.table_prefix_separator = table_prefix_separator
        self.compat = compat
        self.transport = transport or self.DEFAULT_TRANSPORT
        self.protocol = protocol or self.DEFAULT_PROTOCOL
        self.pool_size = pool_size or self.DEFAULT_POOL_SIZE
        self._pool = happybase.ConnectionPool(size=self.pool_size,
                                          host=self.host,
                                          port=self.port,
                                          timeout=self.timeout,
                                          autoconnect=self.autoconnect,
                                          table_prefix=self.table_prefix,
                                          table_prefix_separator=self.table_prefix_separator,
                                          compat=self.compat,
                                          transport=self.transport,
                                          protocol=self.protocol
                                          )

    def __new__(self, *args, **kwargs):
        if not hasattr(_PyHbase, "_instance"):
            with _PyHbase._instance_lock:
                if not hasattr(_PyHbase, "_instance"):
                    _PyHbase._instance = object.__new__(self)
        return _PyHbase._instance

    def get_by_rowkey(self, table_name, row_start, row_stop, columns=None, filter=None, timestamp=None,
             include_timestamp=False, batch_size=1000, scan_batching=None,
             limit=None, sorted_columns=False, reverse=False, decode=False):
        with self._pool.connection() as conn:
            conn.open()
            table = conn.table(table_name)
            result = table.scan(row_start=str(row_start).encode(), row_stop=str(row_stop).encode(),
             columns=columns, filter=filter, timestamp=timestamp,
             include_timestamp=include_timestamp, batch_size=batch_size, scan_batching=scan_batching,
             limit=limit, sorted_columns=sorted_columns, reverse=reverse)
            df = pd.DataFrame()
            if decode:
                for key, data in result:
                    data = dict(data)
                    cols = data.keys()
                    dict_data = {'row_key': key.decode()}
                    for col in cols:
                        dict_data[col.decode()] = data.get(col).decode()
                    df = df.append(dict_data, ignore_index=True)
            else:
                for key, data in result:
                    data[b'row_key'] = key
                    df = df.append(data, ignore_index=True)
                if not df.empty:
                    df.set_index([b'row_key'], inplace=True)
            conn.close()
            return df

    def get_by_row_prefix(self, table_name, row_prefix, columns=None, filter=None, timestamp=None,
             include_timestamp=False, batch_size=1000, scan_batching=None,
             limit=None, sorted_columns=False, reverse=False):
        with self._pool.connection() as conn:
            table = conn.table(table_name)
            result = table.scan(row_prefix=row_prefix.encode(),
             columns=columns, filter=filter, timestamp=timestamp,
             include_timestamp=include_timestamp, batch_size=batch_size, scan_batching=scan_batching,
             limit=limit, sorted_columns=sorted_columns, reverse=reverse)
            df = pd.DataFrame()
            for key, data in result:
                data[b'row_key'] = key
                df = df.append(data, ignore_index=True)
            if not df.empty:
                df.set_index([b'row_key'], inplace=True)
            conn.close()
            return df

    def put(self,table_name,row_key,col_data):
        with self._pool.connection() as conn:
            conn.open()
            table = conn.table(table_name)
            table.put(row_key, col_data)
            conn.close()

    def batch(self,table_name,list_tuple2,bacth_size=1000):
        if list_tuple2:
            with self._pool.connection() as conn:
                conn.open()
                table = conn.table(table_name)
                with table.batch(batch_size=bacth_size) as b:
                    for k, v in list_tuple2:
                        b.put(k, v)
                conn.close()

    def put_df(self,table_name,data_frame=pd.DataFrame(),bacth_size=1000):
        if not data_frame.empty:
            with self._pool.connection() as conn:
                conn.open()
                table = conn.table(table_name)
                with table.batch(batch_size=bacth_size) as b:
                    for index, row in data_frame.iterrows():
                        data = dict(row)
                        for k in list(data.keys()):
                            if not pd.notna(data.get(k)) or not pd.notnull(data.get(k)):
                                del data[k]
                        b.put(index, data)
                conn.close()
