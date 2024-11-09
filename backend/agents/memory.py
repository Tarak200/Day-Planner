# /backend/agents/memory.py
from neo4j import GraphDatabase

class MemoryAgent:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def remember_preferences(self, user_id, preferences):
        with self.driver.session() as session:
            session.run("MERGE (user:User {id: $id}) SET user.preferences = $preferences", id=user_id, preferences=preferences)

    def fetch_preferences(self, user_id):
        with self.driver.session() as session:
            result = session.run("MATCH (user:User {id: $id}) RETURN user.preferences", id=user_id)
            return result.single()[0]
