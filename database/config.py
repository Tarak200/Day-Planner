# /database/config.py
import os

class Neo4jConfig:
    URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")  # Default DB name, adjust as necessary

    @staticmethod
    def get_neo4j_credentials():
        """Utility function to fetch Neo4j database credentials."""
        return {
            "uri": Neo4jConfig.URI,
            "username": Neo4jConfig.USERNAME,
            "password": Neo4jConfig.PASSWORD,
            "database": Neo4jConfig.DATABASE
        }
