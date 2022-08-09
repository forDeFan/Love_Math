import sqlite3
from typing import List, Tuple

from src.abstract.db_connection_abstract import Abstract_db


class Db_Connection(Abstract_db):
    """
    Sqlite3 database service class.
    Implementation of Abstract_db class.
    """

    def __init__(self, db_name: str, categories: List[str]) -> None:
        """
        Initialization with:

        Args:
            db_name (str): database filename.
            categories (List[str]): from constants - to automatically fill out db columns.
        """
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS results(
            category text,
            result integer,
            qst_no integer,
            percentage integer,
            UNIQUE(category))"""
        )
        # Add categories from list.
        for c in categories:
            self.cur.execute(
                f"INSERT OR IGNORE INTO results(category,result,qst_no,percentage) VALUES ('{c}','0','0','0')"
            )

        self.conn.commit()

    def __del__(self) -> None:
        """
        Remove database at exit from app.
        """
        self.conn.close()

    def update_result(self, category_name: str) -> None:
        """
        Update point result for specified category.

        Args:
            category_name (str): specified category.
        """
        self.cur.execute(
            f"UPDATE results SET result=result+1 WHERE category='{category_name}'"
        )
        self.conn.commit()

    def get_result(self, category_name: str) -> str:
        """
        Get point result from database for specified category.

        Args:
            category_name (str): specified category.

        Returns:
            str: points for specified category.
        """
        res = self.cur.execute(
            f"SELECT result FROM results WHERE category='{category_name}'"
        )
        return res.fetchone()[0]

    def get_results(self) -> List[Tuple[str, str]]:
        """
        Get point result from database for all categories.

        Returns:
            List[Tuple[str, str]]: List of Tuples[category, points]
        """
        res = self.cur.execute("SELECT * FROM results")
        return res.fetchall()

    def update_question_no(self, category_name: str) -> None:
        """
        Update number of asked questions in database in specified category - for percentage calculation.

        Args:
            category_name (str): specified category.
        """
        self.cur.execute(
            f"UPDATE results SET qst_no=qst_no+1 WHERE category='{category_name}'"
        )
        self.conn.commit()

    def get_question_no(self, category_name: str) -> str:
        """
        Get number of asked questions from database in specified category - for percentage calculation.

        Args:
            category_name (str): specified category.

        Returns:
            str: number of asked questions in specified category.
        """
        res = self.cur.execute(
            f"SELECT qst_no FROM results WHERE category='{category_name}'"
        )
        return res.fetchone()[0]

    def update_percent(self, category_name: str) -> None:
        """
        Update percenatge of answered questions in database for spefied category.

        Args:
            category_name (str): specified category.
        """
        q_no = self.get_question_no(category_name=category_name)
        res = self.get_result(category_name=category_name)

        if q_no and res > 0:
            per = (res / q_no) * 100
        else:
            per = -1
        self.cur.execute(
            f"UPDATE results SET percentage='{per}' WHERE category='{category_name}'"
        )
        self.conn.commit()

    def get_percent(self, category_name: str) -> str:
        """
        Get percentage of properly answered questions from database in spefied catgeory.

        Args:
            category_name (str): specified category.

        Returns:
            str: percentage of correct answers.
        """
        res = self.cur.execute(
            f"SELECT percentage FROM results WHERE category='{category_name}'"
        )
        return str(int(res.fetchone()[0]))
