
from neo4j import GraphDatabase
import requests
import os
import logging
from tqdm import tqdm
import json

def get_query(question):

    url = "http://172.19.7.73:43413"
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": f"""Hello, I am working with a Neo4j database and would like you to help me construct a Cypher query based on the information I provide. Please generate a syntactically correct Cypher query statement that can be executed directly in the Neo4j environment. Ensure that the query is precise and optimized for performance. I will describe the information I need to retrieve; please make sure the generated Cypher query accurately reflects my requirements.

Now I'm going to tell you a little bit about this knowledge graph.
1. This knowledge map is a map of frame materials based on all the research literature on frame materials.
2. All the content is stored in the name attribute of node.
3. Relationships can be unrestricted in the query process to expand the search scope.
4. It is recommended that you search not only for relationships that start from the subject, but also for relationships that point to the subject.

You generate a Cypher query related to the problem. The query scope of the statement can be as broad as possible. We will also have personnel to process the data.
Please define only one node variable in Cypher's where.

My question is:
{question}

please only answer the cypher. with out any title, such as cypher.

Example:
MATCH (a:Node)-[r]->(b:Node)
WHERE a.name = ""
RETURN a, r, b
""",

        "history": ""
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(response.json()["response"])
        return response.json()["response"]
    else:
        print(f"Error: Received status code {response.status_code}")
        return None


def run_cypher_query(cypher_query, uri="bolt://localhost:7687", user="neo4j", password="00351385"):
    """
    Executes a Cypher query against a Neo4j database and returns the result.

    :param cypher_query: A string containing the Cypher query to execute.
    :param uri: The URI of the Neo4j instance.
    :param user: Username for authentication.
    :param password: Password for authentication.
    :return: Query result as a list of dictionaries.
    """
    # Initialize the driver
    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        with driver.session() as session:
            # Execute the Cypher query
            result = session.run(cypher_query)
            # Extract records into a list of dictionaries
            records = [record.data() for record in result]
            print(records)
            return records
    finally:
        # Ensure the driver is closed after executing the query
        driver.close()


def answer_question(kg_records,question):
    url = "http://172.19.7.73:43413"
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": f"""请结合以下信息，简洁和专业的来回答用户的问题，若信息与问题关联紧密，请尽量参考已知信息。
已知相关信息:\n{kg_records}
请回答以下问题:{question}    """,
        "history": ""
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(response.json()["response"])
        return response.json()["response"]
    else:
        print(f"Error: Received status code {response.status_code}")
        return None


question = "What are the applications of UiO-66?"
#query = get_query(question)
records = run_cypher_query(cypher_query="""MATCH (a:Node)-[r:DERIVED_FROM]-(b:Node)
WHERE a.name = "UiO-66"
RETURN a, r, b""")
records = str(records)[:1500]   
#answer_question(kg_records=records, question=question)
answer_question(kg_records=records, question="give me reference about UiO-66 application")