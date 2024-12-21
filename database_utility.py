import sqlite3
from typing import Any, Dict, List, Optional, Tuple, Union


class DatabaseError(Exception):
    """Custom exception for database-related errors"""

    pass


class DataBase:
    """Abstract base class defining the database interface"""

    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def execute_query(self, query: str, params: Tuple = ()) -> None:
        raise NotImplementedError

    def insert(self, table: str, data: Dict[str, Any]) -> None:
        raise NotImplementedError

    def delete(self, table: str, condition: str, params: Tuple = ()) -> None:
        raise NotImplementedError

    def update(
        self, table: str, updates: Dict[str, Any], condition: str, params: Tuple = ()
    ) -> None:
        raise NotImplementedError

    def select(
        self, table: str, condition: Optional[str] = None, params: Tuple = ()
    ) -> List[Tuple]:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError


class SQLite(DataBase):
    def __init__(self, database: str):
        self.database = database
        self._connection = None
        self._cursor = None

    def open(self):
        """Open the database connection"""
        self._connection = sqlite3.connect(self.database)
        self._cursor = self._connection.cursor()

    def close(self):
        """Close the database connection"""
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()

    @property
    def cursor(self):
        """Property to ensure cursor is available"""
        if self._cursor is None:
            raise DatabaseError("Database connection not established")
        return self._cursor

    def fixData(self, db_fetch : list[dict], db_disc : list) -> list[dict]:
        cols_disc = [col[0] for col in db_disc]
        rows = [dict(zip(cols_disc, row)) for row in db_fetch]
        return rows
    
    def free_execute(self, quary_text="", *args):
        if len(tuple(args)) == 0:
            try:
                self.cursor.execute(quary_text)
                data = self.fixData(self.cursor.fetchall(), self.cursor.description)
            except:
                return []
        else:
            try:
                self.cursor.execute(quary_text, args)
                data = self.fixData(self.cursor.fetchall(), self.cursor.description)
            except:
                return []
        return data

    def execute_query(self, query: str, params: Tuple = ()) -> None:
        try:
            self.cursor.execute(query, params)
        except sqlite3.Error as e:
            raise DatabaseError(f"Query execution failed: {str(e)}")

    def insert(self, table: str, data: Dict[str, Any]) -> None:
        """Insert data using dictionary format"""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))

    def delete(self, table: str, condition: str, params: Tuple = ()) -> None:
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_query(query, params)

    def update(
        self, table: str, updates: Dict[str, Any], condition: str, params: Tuple = ()
    ) -> None:
        """Update data using dictionary format"""
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        self.execute_query(query, tuple(updates.values()) + params)

    def select(
        self, table: str, condition: Optional[str] = None, params: Tuple = ()
    ) -> List[Tuple]:
        query = f"SELECT * FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        self.execute_query(query, params)
        return self.cursor.fetchall()
    
    

    def commit(self) -> None:
        if self._connection:
            self._connection.commit()

    def rollback(self) -> None:
        if self._connection:
            self._connection.rollback()


if __name__ == "__main__":
    database = "skills.db"
    db = SQLite(database)
    db.open()

    def add_skill(id, name, progress):
        db.insert("skills", {"id": id, "name": name, "progress": progress})
        db.commit()

    def update_skill(id, progress):
        db.update("skills", {"progress": progress}, "id = ?", (id,))
        db.commit()

    update_skill(1, 95)

    db.close()
