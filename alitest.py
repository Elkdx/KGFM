# -*- coding: utf-8 -*-
"""
PyCharm
@project_name: knowledge graph
@File        : alitest.py
@Author      : Xuefeng-Bai@BJUT
@Date        : 2024/5/24 10:04
"""
import json
from http import HTTPStatus

import dashscope



def call_with_messages(i, content):
    messages = [{'role': 'system',
                 'content': """You are an expert in the creation of graph databases.You create nodes and relationships based on information.All nodes should ideally be one word or two words.Returns a JSON.
                 Json only can include start_node, relationship,end_node.
                 Please follow the format strictly:
                 1.JSON file contains multiple dictionaries
                 2.Each dictionary contains three key-value pairs that: start_node, relationship, end_note
                 3.The value is a str
                 4.Please use the correct json format 
                 for example{{start_node:"word",relationship:"word",end_node:"word"},{start_node:"word",relationship:"word",end_node:"word"},...}
                 TI is title; AB is abstract.
                 If you find the name of any of the COFs materials in this, please include {start_node:"COF",relationship:"contain",end_node:"COF name in text"} in your answer
                 Try to have less data-based content and more generalized content, I'm creating a knowledge graph.
                 Outputs the result in json format, without any line breaks, etc.!
                 """},
                {'role': 'user', 'content': f"""{content}"""}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # 将返回结果格式设置为 message
    )
    if response.status_code == HTTPStatus.OK:
        # print(response)
        # 提取 content 字段
        content_str = response['output']['choices'][0]['message']['content']

        # 去掉 ```json 和最后的 ```
        if content_str.startswith('```json'):
            content_str = content_str[8:-4]
            # print(content_str)
        # 解析 JSON 字符串
        parsed_content = json.loads(content_str)

        # 现在 parsed_content 包含了解析后的 JSON 数据
        # print(parsed_content)
        # 指定要保存的文件名
        filename = f'{str(i)}.json'

        # 将内容写入文件
        with open(f"./{type_organic}Jsonfile/{filename}", 'w', encoding='utf-8') as f:
            json.dump(parsed_content, f, ensure_ascii=False, indent=4)

    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    type_organic = "Figure"
    error_file = open(f"{type_organic}errorfile.txt", mode="a", newline="\n")
    for i in range(6, 7):
        print(i)
        try:
            with open(f"./{type_organic}text/{i}.txt", mode="r", encoding="utf-8") as file:
                content = file.read()
                call_with_messages(i=i, content=content)
                # time.sleep(1)
        except:
            error_file.write(f"{i}Error")
            print(f"{i}Error")
        # with open(f"{i}.txt",mode="r",encoding="utf-8") as file:
        #     content = file.read()
        #     call_with_messages(i=i,content=content)
