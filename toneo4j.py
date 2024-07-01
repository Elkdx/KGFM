import json
from neo4j import GraphDatabase

class Neo4jImport:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def import_data(self, data):
        with self._driver.session() as session:
            for record in data:
                start_node = record['start_node']
                relationship = record['relationship']
                end_node = record['end_node']
                session.execute_write(self._create_relationship, start_node, relationship, end_node)

    @staticmethod
    def _create_relationship(tx, start_node, relationship_type, end_node):
        relationship_type = relationship_type.replace("-", "_")
        relationship_type = relationship_type.replace(" ", "_")
        query = (
            "MERGE (a:Node {name: $start_node}) "
            "MERGE (b:Node {name: $end_node}) "
            f"MERGE (a)-[r:{relationship_type}]->(b) "
            "RETURN a, r, b"
        )
        result = tx.run(query, start_node=start_node, relationship_type=relationship_type, end_node=end_node)
        return result.single()

if __name__ == "__main__":
    type_organic = "Figure"
    uri = "bolt://localhost:7687"  # Neo4j数据库连接地址
    user = "neo4j"  # Neo4j数据库用户名
    password = "00351385"  # Neo4j数据库密码
    error_file = open(f"{type_organic}errorneo4jfile.txt",mode="a",newline="\n")
    for i in range(1,2):
        print(i)
        # 读取JSON文件
        try:
            with open(f'D:\\Desktop\\knowledge graph\\{type_organic}Jsonfile\\{i}.json', 'r') as f:
                import_data = json.load(f)
                print(import_data)

                # 创建Neo4jImport实例并导入数据
                neo4j_import = Neo4jImport(uri, user, password)
                neo4j_import.import_data(import_data)
                neo4j_import.close()
        except:
            error_file.write(f"{i}Error")
            print(f"{i}Error \n")



        # with open(f'D:\\Desktop\\knowledge graph\\Jsonfile\\{i}.json', 'r') as f:
        #     import_data = json.load(f)
        #     print(import_data)
        #
        #     # 创建Neo4jImport实例并导入数据
        #     neo4j_import = Neo4jImport(uri, user, password)
        #     neo4j_import.import_data(import_data)
        #     neo4j_import.close()