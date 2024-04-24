import psycopg2
from Repository import Repository


class SQLRepository(Repository):

    def __init__(self, connect):
        self.connect = connect

    def create_db(self):
        with self.connect.cursor() as cursor:
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS genders(
                        id PRIMARY KEY,
                        gender VARCHAR(10)
                    );
                    """)

            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cities(
                        id PRIMARY KEY,
                        city VARCHAR(50)
                    );
                    """)

            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users(
                        id PRIMARY KEY,
                        first_name VARCHAR(50),
                        last_name VARCHAR(50),
                        age int(3),
                        FOREIGN KEY (gender_id) REFERENCES genders(id),
                        FOREIGN KEY (city_id) REFERENCES cities(id),
                        about_me VARCHAR(200)
                    );
                    """)

            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS favorites(
                                id SERIAL PRIMARY KEY,
                                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                                first_name VARCHAR(50),
                                last_name VARCHAR(50),
                                age int(3),
                                FOREIGN KEY (gender_id) REFERENCES genders(id),
                                profile VARCHAR(50),
                                photo1 VARCHAR(50),
                                photo2 VARCHAR(50),
                                photo3 VARCHAR(50),
                                FOREIGN KEY (city_id) REFERENCES cities(id),
                            );
                            """)

            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS exceptions(
                                id SERIAL PRIMARY KEY,
                                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                                first_name VARCHAR(50),
                                last_name VARCHAR(50),
                                age int(3),
                                FOREIGN KEY (gender_id) REFERENCES genders(id),
                                profile VARCHAR(50),
                                photo1 VARCHAR(50),
                                photo2 VARCHAR(50),
                                photo3 VARCHAR(50),
                                FOREIGN KEY (city_id) REFERENCES cities(id),
                            );
                            """)

    def get_favorites(self, user_id):
        with self.connect.cursor() as cursor:
            select_dict = []
            data = []

            select_dict.append('user_id=%s')
            data.append(str(user_id))

            select_stmt = ("SELECT first_name, last_name, age, genders.gender, profile, "
                           "photo1, photo2, photo3, cities.city"
                        " FROM favorites "
                        " INNER JOIN genders"
                        " ON favorites.user_id = genders.id"
                        " INNER JOIN cities"
                        " ON favorites.city_id = cities.id"
                        " WHERE user_id=%s")

            cursor.execute(select_stmt, tuple(data))

    def get_exceptions(self, user_id):
        with self.connect.cursor() as cursor:
            select_dict = []
            data = []

            select_dict.append('user_id=%s')
            data.append(str(user_id))

            select_stmt = ("SELECT first_name, last_name, age, genders.gender, profile, "
                           "photo1, photo2, photo3, cities.city"
                        " FROM exceptions "
                        " INNER JOIN genders"
                        " ON exceptions.user_id = genders.id"
                        " INNER JOIN cities"
                        " ON exceptions.city_id = cities.id"
                        " WHERE user_id=%s")

            cursor.execute(select_stmt, tuple(data))