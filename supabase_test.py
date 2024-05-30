import time
import jieba
import configparser
import pandas as pd
import sqlite3
import os
import dotenv
import supabase
from supabase import create_client, Client
from tqdm import tqdm
# jieba.load_userdict('./userdict/2000000-dict.txt')

dotenv.load_dotenv()
supabase_url: str = os.environ.get("SUPABASE_URL")
supabase_key: str = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)
resource_id = '86f93c93-6c4a-49d0-977f-68ab9174c47e'

# 向table里面写入条目

# up_json = {'resource_id': '86f93c93-6c4a-49d0-977f-68ab9174c47e', 'term': '外', 'df': 2, 'chunk_info': {'989f6540-b1af-4f4f-ae5c-e9a4f7890682': {'count': 1, 'clean_length': 133}, '318f25b3-bb79-495e-9f00-7cd8b081dd74': {'count': 1, 'clean_length': 260}}}
# supabase.table("resource_bm25").insert(up_json).execute()

# 读取数据
# chunks = supabase.table('resource_bm25').select("*").filter("resource_id", "eq", resource_id).limit(5).execute().data  # -->list(dict)
# print(chunks)
# print(len(chunks))

# 删除数据
# supabase.table('resource_bm25').delete().eq('resource_id','86f93c93-6c4a-49d0-977f-68ab9174c47e').execute()


# merge两次算出的词频信息结果
# def merge_bm25_core(former_resul, new_resul):
#     """
#     resul格式示例list(dict)
#     [
#     {'resource_id': '86f93c93-6c4a-49d0-977f-68ab9174c47e', 
#     'term': '外', 
#     'df': 2, 
#     'chunk_info': {'989f6540-b1af-4f4f-ae5c-e9a4f7890682': {'count': 1, 'clean_length': 133}, '318f25b3-bb79-495e-9f00-7cd8b081dd74': {'count': 1, 'clean_length': 260}}},
#     .....
#     ]
#     """
#     for x in new_resul:
#         for y in former_resul:
#             if x["term"] == y["term"]:
#                 y["df"] = y["df"] + x["df"]
#                 y['chunk_info'].update(x["chunk_info"])
#                 break
#         former_resul.append(y)
#     return former_resul
            





# 更新表
# data_upsert1 = {'resource_id': '86f93c93-6c4a-49d0-977f-68ab9174c47e', 'term': '外', 'df': 2, 'chunk_info': {"测试":"hah"}}
# data_upsert2 = {'resource_id': '86f93c93-6c4a-49d0-977f-68ab9174c47e', 'term': '外', 'df': 2, 'chunk_info': {'989f6540-b1af-4f4f-ae5c-e9a4f7890682': {'count': 1, 'clean_length': 133}, '318f25b3-bb79-495e-9f00-7cd8b081dd74': {'count': 1, 'clean_length': 260}}}
# def update_resource_bm25(data_upsert):
#     # 如果有'resource_id'、"term"两个字段的值与待更新的数据相同，则更新该数据；如没有，插入一条新数据
#     data, _ = supabase.table('resource_bm25').update(data_upsert).match({'resource_id': data_upsert["resource_id"], "term" : data_upsert["term"]}).execute()
#     if data[1]:
#         pass
#     else:
#         supabase.table("resource_bm25").insert(data_upsert1).execute()


# 迭代读取supabase的内容
# offset = 0
# while True:
#     response = supabase.table('resource_bm25').select("*").limit(1).offset(offset).execute().data
#     offset += 1
#     if not response:
#         break
#     print(response)


# 读取bm25_param
# response = supabase.table("resources").select("*").filter("id", "eq", resource_id).execute().data[0]["bm25_param"]
# print(response)
# print(type(response))

# 写入bm25_param
# res_id = "028f8dcc-75f1-4dd4-8e63-93806a2dc69c"
# bm25_param = {'N': 102, 'AVG_L': 400}
# supabase.table("resources").update({"bm25_param":bm25_param}).eq("id",res_id).execute()


# 读取resource_bm25的分词的关键参数
# response = supabase.table("resource_bm25").select("*").match({"resource_id":resource_id, "term":"外"}).execute().data  # 返回长度为1的列表
# df = response[2]["df"]
# chunk_info = response[2]["chunk_info"]
# print(response)
# print("%"*100)
# print(df)
# print("%"*100)
# print(chunk_info)

# dict iter测试
# dict1 = {'318f25b3-bb79-495e-9f00-7cd8b081dd74': {'count': 1, 'clean_length': 260}, '989f6540-b1af-4f4f-ae5c-e9a4f7890682': {'count': 1, 'clean_length': 133}}
# for item in dict1:
#     print(item)  # key str
#     print(type(item))
# print("%"*100)

# for item in dict1.items():
#     print(item)  #(key, value) tuple
#     print(type(item))

# # 拿chunk
# id = '318f25b3-bb79-495e-9f00-7cd8b081dd74'
# response = supabase.table("chunks").select("*").filter("id", "eq", id).execute().data[0]["content"]  # chunk内容

# 尝试一下列表切片索引会不会超限
# lst1 = [0,1,2]
# lst2 = lst1[:4]
# print(lst2)

# 切片索引超出范围并不会报错，直接索引会报错
# lst = [x for x in range(58)]
# dict1 = {k:v for k, v in enumerate(lst)}
# for i in tqdm(range(0, len(lst), 10)):
#     current_list = lst[i:i+10]
#     print(current_list)

# 打印长度
# dict1 = {"0d08a321-3e2c-4ac9-814a-e5442c6ff658":{"count":1,"clean_length":199},"1f9cb49f-5c92-40c7-85e6-9d0713539504":{"count":1,"clean_length":145},"20c0df72-6d56-4530-870d-2f8ce776747d":{"count":1,"clean_length":5},"3165921e-41ad-40f3-997b-f77dd2af7183":{"count":1,"clean_length":9},"3bfd2e00-27f5-4a0e-98e9-e0d84f1ea422":{"count":1,"clean_length":10},"4ab01685-160e-4f3b-b556-95488fb58337":{"count":1,"clean_length":5},"50c56f21-62e4-4f54-8607-b7ea1cb2911a":{"count":1,"clean_length":12},"575d91a8-abdb-4b9b-b2e7-6ffc5803cfca":{"count":1,"clean_length":11},"715eecd5-ee20-46b8-bab0-973f353cf7e6":{"count":1,"clean_length":199},"7d915fe7-7a32-4dd2-a660-90e6c1c7c31c":{"count":1,"clean_length":9},"90f4e92f-0522-4ad9-899a-63e62eb03bb1":{"count":1,"clean_length":57},"94d206d8-638e-418e-b633-00a4c6ba9be4":{"count":1,"clean_length":195},"9966964e-2652-452f-a0a9-8f6c2e061247":{"count":1,"clean_length":10},"a12d08ce-3d8f-46e7-b47a-9e8b873fe9ad":{"count":1,"clean_length":11},"a9b02509-7de7-4032-85b0-8b369298e14f":{"count":1,"clean_length":199},"aa30c83a-348c-45b3-b96f-92ff35b89377":{"count":1,"clean_length":5},"aaba5741-dbaf-4203-97e0-9a055bd59d62":{"count":1,"clean_length":145},"ad7d8bcf-084a-49f0-b835-caf547f2c457":{"count":1,"clean_length":12},"ae78a2cb-6227-41e7-9feb-b396e0fdaa1b":{"count":1,"clean_length":11},"b997a785-9467-4726-b933-d86fdf6fcfd6":{"count":1,"clean_length":195},"bccfb4b5-76f5-468e-811d-6d247788b60e":{"count":1,"clean_length":57},"c0e0d672-f68f-47a7-b40d-b81451aca745":{"count":1,"clean_length":195},"c125004e-2ecb-4e19-a222-a19bfef02e6f":{"count":1,"clean_length":10},"c153ced7-6de6-4a21-800a-ef039e5f266f":{"count":1,"clean_length":57},"d98455bd-4b53-47e6-8025-039efbe5b95f":{"count":1,"clean_length":9},"dddaad1d-7c7f-4cfa-87eb-0e72cdac7f85":{"count":1,"clean_length":12},"f42e066c-3a57-41f6-b3a3-f205f6cdd057":{"count":1,"clean_length":145}}
# print(len(dict1))

# # 看一下这个类属性，在实例方法中使用self.class_attribute去更改，并不会改变另一个实例的属性
# class MyClass:
#     class_attribute = "这是一个类属性"

#     def instance_method(self):
#         self.class_attribute = "这是另一个类属性"

#     def print_class_attribute(self):
#         print(self.class_attribute)

# c1 = MyClass()

# c1.instance_method()
# c1.print_class_attribute()
# # 这是另一个类属性

# c2 = MyClass()
# c2.print_class_attribute()
# # 这是一个类属性

# # 一次性读取chunks_id列表
# chunk_ids = [
#     "0000cdd4-93de-4d10-b9d2-f9b90f0bc47f",
#     "00034423-f729-4a57-a424-83e0827012ab",
#     "0005162d-d394-404e-9678-82e056e2e677"
# ]
# response = supabase.table('chunks').select('*').in_('id', chunk_ids).execute().data
# print(response)
# print(len(response))

str1 = "你是谁"
str2 = "我是超人"
str3 = "你好呀"
dict1 = {k:v for k, v in enumerate(str999)}
dict2 = {k:v for k, v in enumerate(str2)}
dict3 = {k:v for k, v in enumerate(str2)}
lst1 = [dict1, dict2, dict3]
print(lst1)
lst2 = lst1[::-1]
print(lst2)


