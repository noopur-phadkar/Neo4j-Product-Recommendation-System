from neo4j import GraphDatabase


class DatabaseSetup:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_constraints(self):
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT ON (u:User) ASSERT u.id IS UNIQUE")
            session.run("CREATE CONSTRAINT ON (p:Product) ASSERT p.id IS UNIQUE")
            session.run("CREATE CONSTRAINT ON (c:Category) ASSERT c.name IS UNIQUE")

    def load_initial_data(self):
        # Method to load initial data into the database
        pass


if __name__ == "__main__":
    db_setup = DatabaseSetup("bolt://localhost:7687", "neo4j", "password")
    db_setup.create_constraints()
    db_setup.load_initial_data()
    db_setup.close()
