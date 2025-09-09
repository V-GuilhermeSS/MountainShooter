import sqlite3

"""
Module responsible for persisting game data in an SQLite database.

Contains the DBProxy class that abstracts table creation, record insertion,
and retrieval of the top 10 results.
"""


class DBProxy:
    """
    Class that acts as a proxy for the SQLite database.

    Responsible for:
    - Creating the data table (if it doesn't exist).
    - Saving records containing name, score, and date.
    - Retrieving the top 10 scores.
    - Closing the database connection.
    """
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.connection.execute('''
                                   CREATE TABLE IF NOT EXISTS dados(
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   name TEXT NOT NULL,
                                   score INTEGER NOT NULL,
                                   date TEXT NOT NULL)
                                '''
                                )

    def save(self, score_dict: dict):
        """
        Initializes the database connection and ensures that the 'data' table exists.

        Args:
        db_name (str): SQLite database file name.
        """
        self.connection.execute('INSERT INTO dados (name, score, date) VALUES (:name, :score, :date)', score_dict)
        self.connection.commit()

    def retrieve_top10(self) -> list:
        """
        Retrieves the 10 highest scores stored in the database.

        Returns:
        list: List of tuples containing the records (id, name, score, date).
        """
        return self.connection.execute('SELECT * FROM dados ORDER BY score DESC LIMIT 10').fetchall()

    def close(self):
        """
        Closes the database connection.

        """
        return self.connection.close()
