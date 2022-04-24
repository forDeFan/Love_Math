import sqlite3


class Db_Connection:
    def __init__(self, db_name: str, *categories: str) -> None:
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS results(
            category text,
            result integer,
            UNIQUE(category))"""
        )

        for c in categories:
            self.cur.execute(
                f"INSERT OR IGNORE INTO results VALUES ('{c}','0')"
            )
        """for row in self.cur.execute("SELECT * FROM results"):
            print(row)"""

        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def update_result(self, category_name: str):
        self.cur.execute(
            f"UPDATE results SET result=result+1 WHERE category='{category_name}'"
        )
        self.conn.commit()

    def get_result(self, category_name: str):
        res = self.cur.execute(
            f"SELECT result FROM results WHERE category='{category_name}'"
        )
        return res.fetchone()
