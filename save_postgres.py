import os
import psycopg2
import pandas as pd


class DB:

    def __init__(self):
        self.conn = psycopg2.connect(host=os.environ['HOST'], database=os.environ['DATABASE'],
                                     user=os.environ['USER'], password=os.environ['PASSWORD'])
        self.cur = self.conn.cursor()

    def upload_data(self, name: str, review: str, n_rev: int, metadata: str):
        try:
            q = "INSERT INTO scifile (name, review, n_rev, metadata) VALUES (%s, %s, %s, %s)"
            self.cur.execute(q, (name, review, n_rev, metadata))
            self.conn.commit()
            print("Data upload OK")
            state = True

        except psycopg2.Error as e:
            print("Error to upload: ", e)
            self.conn.rollback()
            state = False

        self.cur.close()
        self.conn.close()

        return state

    def query_article(self, name: str):
        try:
            q = "SELECT * FROM scifile WHERE name = (%s)"
            self.cur.execute(q, (name, ))
            rows = self.cur.fetchall()
            df = pd.DataFrame(rows, columns=['name', 'review', 'n_rev', 'metadata'])
            print("Query OK")
            print(df)

        except psycopg2.Error as e:
            print("Error query: ", e)
            self.conn.rollback()
            df = None

        self.cur.close()
        self.conn.close()

        return df


if __name__ == "__main__":
    # DB().upload_data(article="Test from python",
    #                  review='Review from python',
    #                  n_rev=1,
    #                  metadata='{"data": "data python"}')

    DB().query_article(name='test')
