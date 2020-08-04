# -*- coding:utf-8 -*-
# time:  11:24
# Author: DuanYuanJie

import os
import pandas as pd
import re
import numpy as np

pd.set_option('display.max_rows', None)

def read_file_by_name(file_object, params):
    """
    根据文件地址读取文件读取
    :param file_path: 文件地址
    :return: 文件内容
    """
    pass
    # save_path = os.path.join(os.path.dirname(__file__), 'static')
    # if file_object.filename.endswith('.pdf'):
    #     # file_obj被传输后，文件指针会指向最后，所以需要调整指针的位置到最前面
    #     file_object.seek(0)
    #
    #     #  file_obj存储到本地
    #     file_object.save(os.path.join(save_path, 'pdf\\' + file_object.filename))
    #
    #     # 读取解析pdf文件
    #     with pdfplumber.open(save_path + '\\pdf\\' + file_object.filename) as pdf:
    #         page_list = []
    #         if params['type'] == '7':
    #             for i in range(len(pdf.pages)):
    #                 for table in pdf.pages[i].extract_tables(table_settings={'horizontal_strategy': 'text', 'vertical_strategy': 'text'}):
    #                     if i == 0:
    #                         for j in range(len(table)):
    #                             if table[j][0] == '00:00':
    #                                 t_head_list = table[: j]
    #                                 if re.search(r"(\d{2}:\d{2})", table[j][-1]):
    #                                     table_data = table[j:]
    #                                 else:
    #                                     table_data = table[j: len(table) - 1]
    #                         t_head_np = np.array(t_head_list)
    #                         t_head_np[t_head_np == None] = ''
    #                         print(t_head_np)
    #                         t_head_np = t_head_np.sum(axis=0)
    #                         table_header = t_head_np.tolist()
    #                     else:
    #                         table_data = table
    #                 page_list.extend(table_data)
    #             table_header = [t_name.replace("\n", "") for t_name in table_header]
    #             data_df = pd.DataFrame(columns=table_header, data=page_list)
    #             data_df = data_df.set_index('时刻点')
    #         else:
    #             page_all_dict = dict()
    #             table_header = []
    #             for i in range(len(pdf.pages)):
    #                 for table in pdf.pages[i].extract_tables():
    #                     if i % 2 == 0:
    #                         table_header.extend(table[0])
    #                         table_data = table[1:]
    #                         page_all_dict[i] = table_data
    #                     else:
    #                         page_all_dict[i] = table
    #             parallel_list, serial_list = [], []
    #             for key, value in page_all_dict.items():
    #                 if key % 2 == 0:
    #                     for v in value:
    #                         parallel_list.append(v)
    #                 else:
    #                     for v in value:
    #                         serial_list.append(v)
    #             chunk_count = len(pdf.pages) // 2
    #             parallel_new_list, serial_new_list = [], []
    #             m = 0
    #             while m < chunk_count:
    #                 parallel_new_list.extend(parallel_list[m * (len(parallel_list) // chunk_count): (m + 1) * (len(parallel_list) // chunk_count)])
    #                 parallel_new_list.extend(serial_list[m * (len(serial_list) // chunk_count): (m + 1) * (len(serial_list) // chunk_count)])
    #                 serial_new_list.extend(parallel_list[(m + 1) * (len(parallel_list) // chunk_count): (m + 2) * (len(parallel_list) // chunk_count)])
    #                 serial_new_list.extend(serial_list[(m + 1) * (len(serial_list) // chunk_count): (m + 2) * (len(serial_list) // chunk_count)])
    #                 m = m + 2
    #             for i in range(len(parallel_new_list)):
    #                 if len(serial_new_list) == 0:
    #                     break
    #                 else:
    #                     parallel_new_list[i].extend(serial_new_list[i])
    #             data_df = pd.DataFrame(columns=table_header, data=parallel_new_list)
    #             data_df = data_df.set_index('时间')
    # elif file_object.filename.endswith('.xls'):
    #     pass
    # return data_df