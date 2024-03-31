from neo4j import GraphDatabase


class DatabaseSetup:
    def __init__(self):
        uri = "bolt://localhost:7687"
        user = "neo4j"
        password = "password"
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_constraints(self):
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT ON (u:User) ASSERT u.id IS UNIQUE")
            session.run("CREATE CONSTRAINT ON (p:Product) ASSERT p.id IS UNIQUE")
            session.run("CREATE CONSTRAINT ON (c:Category) ASSERT c.name IS UNIQUE")