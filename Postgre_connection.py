import psycopg2


class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            # params = config()

            # connect to the PostgreSQL server
            # print('Connecting to the PostgreSQL database...')
            # conn = psycopg2.connect(**params)

            self.conn = psycopg2.connect(
                host="localhost",
                database="MYdb",
                user='postgres',
                password="julius"
            )
            self.conn.autocommit = True

            # create a cursor
            cur = self.conn.cursor()

            # execute a statement
            # print('PostgreSQL database version:')
            # cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            # db_version = cur.fetchone()
            # print(db_version)

            # close the communication with the PostgreSQL
            # cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close(self, ):
        if self.conn is not None:
            self.conn.close()
            # print('Database connection closed.')

    def insert_author(self, author_name, author_number, author_email):
        # create a cursor
        self.connect()
        cur = self.conn.cursor()

        # execute a statement
        # print('Inserting in the database')
        cur.execute("INSERT INTO author VALUES ({},'{}' ,'{}', '{}')".format("default", str(author_name),
                                                                                   str(author_number),
                                                                                   str(author_email)))
        # print("Successfully Inserted")
        # close the communication with the PostgreSQL
        cur.close()
        self.close()
        pass

    def insert_request_info(self, title, category, place, comment):
        self.connect()

        cur = self.conn.cursor()

        cur.execute("INSERT INTO request_info VALUES ({},'{}', '{}', '{}', '{}',(select max(author_id) from author))".format(
                                                                                                                            "default",
                                                                                                                            title,
                                                                                                                            category,
                                                                                                                            place,
                                                                                                                            comment))

        cur.close()
        self.close()
        pass

    def select_all_author(self):
        self.connect()
        cur = self.conn.cursor()

        cur.execute("SELECT * FROM author")
        author = cur.fetchone()

        print(author)


if __name__ == '__main__':
    db = Database()

    db.connect()

    db.insert_author("name","8225233","fhdjf@gmial.com")
    db.select_all_author()
