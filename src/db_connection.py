import sqlite3
from typing import List, Tuple


class Db_Connection:
    def __init__(self, db_name: str, categories: List[str]) -> None:
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS results(
            category text,
            result integer,
            questions_no integer,
            UNIQUE(category))"""
        )
        # Add categories from list.
        for c in categories:
            self.cur.execute(
                f"INSERT OR IGNORE INTO results(category,result,questions_no) VALUES ('{c}','0','0')"
            )

        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def update_result(self, category_name: str):
        self.cur.execute(
            f"UPDATE results SET result=result+1 WHERE category='{category_name}'"
        )
        self.conn.commit()

    def get_result(self, category_name: str) -> str:
        res = self.cur.execute(
            f"SELECT result FROM results WHERE category='{category_name}'"
        )
        return res.fetchone()

    def get_results(self) -> List[Tuple[str, str]]:
        res = self.cur.execute("SELECT * FROM results")
        return res.fetchall()

    def update_question_no(self, category_name: str) -> None:
        self.cur.execute(
            f"UPDATE results SET questions_no=questions_no+1 WHERE category='{category_name}'"
        )
        self.conn.commit()

    def get_question_no(self, category_name: str) -> str:
        res = self.cur.execute(
            f"SELECT questions_no FROM results WHERE category='{category_name}'"
        )
        return res.fetchone()

    def get_percent(self, category_name):
        q_no = self.get_question_no(category_name=category_name)[0]
        res = self.get_result(category_name=category_name)[0]
        if q_no and res != 0:
            per = (res / q_no) * 100
            return str(int(per))
        else:
            return "0"
