# -*- coding: utf-8 -*-
"""
PyCharm
@project_name: knowledge graph
@File        : titletoneo4j.py
@Author      : Xuefeng-Bai@BJUT
@Date        : 2024/5/24 22:10
"""
import json
from neo4j import GraphDatabase
import os


class Neo4jImport:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def import_data(self, start_nodes, end_node):
        with self._driver.session() as session:
            for start_node in start_nodes:
                session.execute_write(self._create_relationship, start_node, end_node)

    @staticmethod
    def _create_relationship(tx, start_node, end_node):
        #start_node = start_node.replace("-", "_")
        #start_node = start_node.replace(" ", "_")
        #end_node = end_node.replace("-", "_")
        #end_node = end_node.replace(" ", "_")
        query = (
            "MERGE (a:Node {name: $start_node}) "
            "MERGE (b:Node {name: $end_node}) "
            "MERGE (a)-[r:DERIVED_FROM]->(b) "
            "RETURN a, r, b"
        )
        result = tx.run(query, start_node=start_node, end_node=end_node)
        return result.single()


def extract_nodes_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    nodes = set()
    for record in data:
        nodes.add(record['start_node'])
        nodes.add(record['end_node'])
    return nodes


def extract_first_line_from_txt(file_path):
    with open(file_path, 'r') as f:
        first_line = f.readline().strip()[3:]  # Skip the first three characters
    return first_line


if __name__ == "__main__":
    type_organic = "COF"
    uri = "bolt://localhost:7687"  # Neo4j数据库连接地址
    user = "neo4j"  # Neo4j数据库用户名
    password = "00351385"  # Neo4j数据库密码

    # 设置文件编号的范围
    start_number = 1
    end_number = 7600 # 根据需要设置结束数字

    # 设置文件所在的目录
    directoryA = f"D:\\Desktop\\knowledge graph\\{type_organic}Jsonfile\\"
    directoryB = f"D:\\Desktop\\knowledge graph\\{type_organic}text\\"

    # 遍历所有文件
    for i in range(start_number, end_number + 1):
        print(i)
        try:
            json_file_path = os.path.join(directoryA, f"{i}.json")
            txt_file_path = os.path.join(directoryB, f"{i}.txt")

            if os.path.exists(json_file_path) and os.path.exists(txt_file_path):
                start_nodes = extract_nodes_from_json(json_file_path)
                end_node = extract_first_line_from_txt(txt_file_path)

                # 创建Neo4jImport实例并导入数据
                neo4j_import = Neo4jImport(uri, user, password)
                neo4j_import.import_data(start_nodes, end_node)
                neo4j_import.close()
            else:
                print(f"File {i}.json or {i}.txt does not exist.")
        except:
            print(f"{i}Error")

        # json_file_path = os.path.join(directoryA, f"{i}.json")
        # txt_file_path = os.path.join(directoryB, f"{i}.txt")
        #
        # if os.path.exists(json_file_path) and os.path.exists(txt_file_path):
        #     start_nodes = extract_nodes_from_json(json_file_path)
        #     end_node = extract_first_line_from_txt(txt_file_path)
        #
        #     # 创建Neo4jImport实例并导入数据
        #     neo4j_import = Neo4jImport(uri, user, password)
        #     neo4j_import.import_data(start_nodes, end_node)
        #     neo4j_import.close()