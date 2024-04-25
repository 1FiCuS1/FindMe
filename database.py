from typing import Union

import sqlalchemy as sq
from psycopg2 import errors
from sqlalchemy import exc, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from table_structure import create_tables
from table_structure import Genders, Cities, Users, Favorites


# Класс, отвечающий за работу с БД и ее таблицами
class Database:

    
    def __init__(self, db_name:str, 
                user:str, password:str, 
                host:str='localhost', 
                port:str='5432'):
        
        """
        Инициируемые параметры:
        - db_name: название БД
        - user: имя пользователя Postgres
        - password: пароль пользователя Postgres
        - host: хост (по умолчанию localhost)
        - port: порт (по умолчанию 5432)
        """
        
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
    
    
    def get_dns(self) -> str:
        
        """
        Назначение:
        - создание DNS ссылки
        
        Выводной параметр:
        - DNS ссылка
        """
        
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
    
    
    def create_db(self, engine:sq.Engine) -> None:
    
        """
        Назначение:
        - формирование БД в случае ее отсутствия
        
        Вводной параметр:
        - engine: движок, формируемый в результате 
        отработки функции sqlalchemy.create_engine()
        """
        
        if not database_exists(engine.url):
            create_database(engine.url)
            print('База данных создана')
        
        else:
            print('База данных уже имеется')
    
    
    def fill_genders_data(self, gender:str) -> dict:
        
        """
        Назначение:
        - заполняет данные таблицы genders в виде словаря
        
        Вводные параметры:
        - gender: наименование пола
        
        Выводной параметр:
        - словарь с данными для заполнения таблицы genders
        """
        
        return {
                'gender': gender
            }
    
    
    def fill_cities_data(self, name:str) -> dict:
        
        """
        Назначение:
        - заполняет данные таблицы cities в виде словаря
        
        Вводные параметры:
        - name: наименование города
        
        Выводной параметр:
        - словарь с данными для заполнения таблицы cities
        """
        
        return {
                'name': name
            }
    
    
    def fill_users_data(self, first_name:str, 
                        last_name:str, age:int, 
                        gender_id:int, city_id:int, 
                        about_me:str) -> dict:
        
        """
        Назначение:
        - заполняет данные таблицы users в виде словаря
        
        Вводные параметры:
        - first_name: имя пользователя
        - last_name: фамилия пользователя
        - age: возраст пользователя
        - gender_id: ID пола пользователя (FK1: genders.id)
        - city_id: ID города проживания пользователя (FK2: cities.id)
        - about_me: информация о пользователе

        Выводной параметр:
        - словарь с данными для заполнения таблицы users
        """
        
        return {
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'gender_id': gender_id,
                'city_id': city_id,
                'about_me': about_me
            }
        
        
    def fill_favorites_data(self, user_id:int, first_name:str,
                            last_name:str, age:int, gender_id:int,
                            profile:str, photo1:str, photo2:str,
                            photo3:str, city_id:int) -> dict:
        
        """
        Назначение:
        - заполняет данные таблицы favorites в виде словаря
        
        Вводные параметры:
        - user_id: уникальный ID пользователя приложения (FK1: users.id)
        - first_name: имя второй половинки
        - last_name: фамилия второй половинки
        - age: возраст второй половинки
        - gender_id: пол второй половинки (FK2: genders.id)
        - profile: наименование профиля второй половинки
        - photo1: ссылка на первый рисунок второй половинки
        - photo2: ссылка на второй рисунок второй половинки
        - photo3: ссылка на третий рисунок второй половинки
        - city_id: ID города проживания пользователя (FK3: cities.id)
        
        Выводной параметр:
        - словарь с данными для заполнения таблицы favorites
        """
        
        return {
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'gender_id': gender_id,
                'profile': profile,
                'photo1': photo1,
                'photo2': photo2,
                'photo3': photo3,
                'city_id': city_id
            }
    
    
    def fill_table(self, engine:sq.Engine, 
                    table_class:object, 
                    dict_table_data:dict) -> bool:

        """
        Назначение:
        - заполняет конкретную таблицу, включенную в БД
        
        Вводные параметры:
        - engine: движок, формируемый в результате 
        отработки функции sqlalchemy.create_engine()
        - table_class: объект класса, относительно 
        которого строится таблица
        - dict_table_data: данные таблицы в формате словаря

        Выводной параметр:
        - значение булева типа: 
            -- True - таблица заполнена
            -- False - таблица не заполнена
        """
        
        session_class = sessionmaker(bind=engine)
        session = session_class()

        try:
            model = table_class(**dict_table_data)
            session.add(model)
            session.commit()
            session.close()
            return True
        
        # max + 1
        except (exc.IntegrityError, errors.UniqueViolation) as err:
            err_text = str(err)
            idx_begin = err_text.find('DETAIL')
            idx_end = err_text.find('".')
            
            if idx_begin != -1 and idx_end != -1:
                detail = err_text[idx_begin:idx_end+1]
                print('IntegrityError', detail)
            return False

        except (exc.DataError, errors.InvalidTextRepresentation):
            print("InvalidTextRepresentation: введен некорректный тип данных")
            return False
    
    
    def fill_tables(self, engine:sq.Engine, gender:str=None, 
                    city_name:str=None, user_first_name:str=None, 
                    user_last_name:str=None, user_age:int=None, 
                    user_gender_id:int=None, user_city_id:int=None, 
                    about_user:str=None, user_id:int=None,
                    partner_first_name:str=None,
                    partner_last_name:str=None, partner_age:int=None, 
                    partner_gender_id:int=None,
                    partner_profile:str=None, photo1:str=None, 
                    photo2:str=None, photo3:str=None, 
                    partner_city_id:int=None) -> None:
        
        # 
        
        """
        Назначение:
        - заполняет таблицы, включенные в БД
        
        Вводные параметры:
        - engine: движок, формируемый в результате 
        отработки функции sqlalchemy.create_engine()
        - gender: наименование пола (таблица genders)
        - city_name: наименование города (таблица city_name)
        - user_first_name: имя пользователя (таблица users)
        - user_last_name: фамилия пользователя (таблица users)
        - user_age: возраст пользователя (таблица users)
        - user_gender_id: ID пола пользователя (таблица users)
        - user_city_id: ID места проживания пользователя (таблица users)
        - about_user: информация о пользователе (таблица users)
        - user_id: ID пользователя приложения (таблица favorites)
        - partner_first_name: имя второй половинки (таблица favorites)
        - partner_last_name: фамилия второй половинки (таблица favorites)
        - partner_age: возраст второй половинки (таблица favorites)
        - partner_gender_id: ID пола второй половинки (таблица favorites)
        - partner_profile: профиль второй половинки (таблица favorites)
        - photo1: первое фото второй половинки (таблица favorites)
        - photo2: второй фото второй половинки (таблица favorites)
        - photo3: третье фото второй половинки (таблица favorites)
        - partner_city_id: ID места проживания второй половинки (таблица favorites)
        """
        
        if gender:
            gender_dict = self.fill_genders_data(
                                                gender
                                            )
            
            if self.fill_table(engine, Genders, gender_dict):
                print(f'Пол {gender} заполнен в таблице genders')
        
        if city_name:
            city_dict = self.fill_cities_data(
                                            city_name
                                        )
        
            if self.fill_table(engine, Cities, city_dict):
                print(f'Город {city_name} заполнен в таблице cities')
        
        if user_first_name and user_last_name and\
            user_age and user_gender_id and\
            user_city_id and about_user:
                
            user_dict = self.fill_users_data(
                                            user_first_name, 
                                            user_last_name,
                                            user_age,
                                            user_gender_id,
                                            user_city_id,
                                            about_user
                                        )
            
            if self.fill_table(engine, Users, user_dict):
                print(f'Пользователь {user_first_name}  {user_last_name} заполнен в таблице cities')
    

                        # user_id = user_id,
                        # partner_first_name = partner_first_name,
                        # partner_last_name = partner_last_name,
                        # partner_age = partner_age,
                        # partner_gender_id = partner_gender_id,
                        # partner_profile = partner_profile,
                        # photo1 = photo1,
                        # photo2 = photo2,
                        # photo3 = photo3,
                        # partner_city_id = partner_city_id
    
        if user_id and partner_first_name and\
            partner_last_name and partner_age and\
            partner_gender_id and partner_profile and\
            photo1 and photo2 and photo3 and partner_city_id:
        
            favorite_dict = self.fill_favorites_data(
                                            user_id, 
                                            partner_first_name,
                                            partner_last_name,
                                            partner_age,
                                            partner_gender_id,
                                            partner_profile,
                                            photo1,
                                            photo2,
                                            photo3,
                                            partner_city_id
                                        )
            
            if self.fill_table(engine, Favorites, favorite_dict):
                print(f'Предпочтение пользователя №{user_id} учтено в таблице favorites')

    
    def start_database(self, gender:str=None,
        city_name:str=None, user_first_name:str=None, 
        user_last_name:str=None, user_age:int=None, 
        user_gender_id:int=None, user_city_id:int=None, 
        about_user:str=None, user_id:int=None,
        partner_first_name:str=None,
        partner_last_name:str=None, partner_age:int=None, 
        partner_gender_id:int=None,
        partner_profile:str=None, photo1:str=None, 
        photo2:str=None, photo3:str=None, 
        partner_city_id:int=None) -> None:

        """
        Назначение:
        - запуск БД и заполнение ее таблицами
        
        Вводные параметры:
        - gender: наименование пола (таблица genders)
        - city_name: наименование города (таблица city_name)
        - user_first_name: имя пользователя (таблица users)
        - user_last_name: фамилия пользователя (таблица users)
        - user_age: возраст пользователя (таблица users)
        - user_gender_id: ID пола пользователя (таблица users)
        - user_city_id: ID места проживания пользователя (таблица users)
        - about_user: информация о пользователе (таблица users)
        - user_id: ID пользователя приложения (таблица favorites)
        - partner_first_name: имя второй половинки (таблица favorites)
        - partner_last_name: фамилия второй половинки (таблица favorites)
        - partner_age: возраст второй половинки (таблица favorites)
        - partner_gender_id: ID пола второй половинки (таблица favorites)
        - partner_profile: профиль второй половинки (таблица favorites)
        - photo1: первое фото второй половинки (таблица favorites)
        - photo2: второй фото второй половинки (таблица favorites)
        - photo3: третье фото второй половинки (таблица favorites)
        - partner_city_id: ID места проживания второй половинки (таблица favorites)
        """
        
        dns_link = self.get_dns()
        engine = create_engine(dns_link)
        
        self.create_db(engine)
        create_tables(engine)
        
        self.fill_tables(
                        engine,
                        gender = gender,
                        city_name = city_name,
                        user_first_name = user_first_name,
                        user_last_name = user_last_name,
                        user_age = user_age,
                        user_gender_id = user_gender_id,
                        user_city_id = user_city_id,
                        about_user = about_user,
                        user_id = user_id,
                        partner_first_name = partner_first_name,
                        partner_last_name = partner_last_name,
                        partner_age = partner_age,
                        partner_gender_id = partner_gender_id,
                        partner_profile = partner_profile,
                        photo1 = photo1,
                        photo2 = photo2,
                        photo3 = photo3,
                        partner_city_id = partner_city_id)
    
    
    def get_db_table(self) -> Union[list, None]:

        """
        Назначение:
        - вывод объединенной таблицы с данными
        
        Выводные параметры:
        - Вариант 1: список с данными
        - Вариант 2: None (в случае отсутствия таблиц)
        """
        
        try:
            DSN = self.get_dns()
            engine = create_engine(DSN)
            
            session_class = sessionmaker(bind=engine)
            session = session_class()
            
            query = session.\
                    query(Users, Genders, Cities, Favorites).\
                    join(Genders, Genders.id == Users.gender_id).\
                    join(Cities, Cities.id == Users.city_id).\
                    outerjoin(Favorites, Favorites.user_id == Users.id)

            users_data = []
            
            for app_users, genders, cities, favorites in query:
                
                try:
                    user_id = favorites.user_id
                    favorite_first_name = favorites.first_name
                    favorite_last_name = favorites.last_name
                    favorite_age =  favorites.age
                    favorite_gender_id =  favorites.gender_id
                    favorite_profile =  favorites.profile
                    favorite_photo1 =  favorites.photo1
                    favorite_photo2 =  favorites.photo2
                    favorite_photo3 =  favorites.photo3
                    favorite_city_id =  favorites.city_id
                except AttributeError:
                    user_id = None
                    favorite_first_name = None
                    favorite_last_name = None
                    favorite_age =  None
                    favorite_gender_id =  None
                    favorite_profile = None
                    favorite_photo1 = None
                    favorite_photo2 = None
                    favorite_photo3 = None
                    favorite_city_id = None
                    
                try:
                    gender_name = genders.gender
                except AttributeError:
                    gender_name = None

                try:
                    city_name = cities.name
                except AttributeError:
                    city_name = None

                users_data.append({
                                'user_first_name': app_users.first_name,
                                'user_last_name': app_users.last_name,
                                'user_age': app_users.age,
                                'user_gender': gender_name,
                                'user_city': city_name,
                                'about_user': app_users.about_me,
                                'user_id': user_id,
                                'favorite_first_name':favorite_first_name,
                                'favorite_last_name': favorite_last_name,
                                'favorite_age': favorite_age,
                                'favorite_gender_id': favorite_gender_id,
                                'favorite_profile': favorite_profile,
                                'favorite_photo1': favorite_photo1,
                                'favorite_photo2': favorite_photo2,
                                'favorite_photo3': favorite_photo3,
                                'favorite_city_id': favorite_city_id
                                })

            session.commit()
            session.close()
            return users_data

        except (exc.ProgrammingError, errors.UndefinedTable) as err:
            err_text = str(err)
            idx_begin = err_text.find('"')
            idx_end = err_text.find('" does not exist')
            
            if idx_begin != -1 and idx_end != -1:
                table_name = err_text[idx_begin:idx_end+1]
                print(f'Таблица {table_name} не найдена в БД')


    def delete_user(self, my_class_object:object, 
                    col_name:str, col_value:any) -> None:
        
        """
        Назначение:
        - удаление строк таблиц, находящихся в БД
        
        Вводные параметры:
        - my_class_object: объект класса
        - col_name: название столбца в виде строки
        - col_value: значение столбца 
        
        Выводные параметры:
        - Вариант 1: список с данными
        - Вариант 2: None (в случае отсутствия таблиц)
        """

        DSN = self.get_dns()
        engine = sq.create_engine(DSN)

        session_class = sessionmaker(bind=engine)
        session = session_class()

        try:
            delete_query = session.\
                        query(my_class_object).\
                        where(getattr(my_class_object, col_name)==col_value).\
                        one()
            
            session.delete(delete_query)
            print(f'Данные пользователя столбца {col_name} со значением {col_value} удалены')
            session.commit()

        except exc.NoResultFound:
            print('NoResultFound: результат по запросу не найден')


if __name__ == '__main__':
    
    # Supermethod (отдельно заполнять ###)
    
    ###
    database = Database('database_test', 'postgres', 'postgres')
    
    ###
    database.start_database(gender = 'Женщина')
    database.start_database(gender = 'Мужчина')
    
    ###
    database.start_database(city_name = 'Москва')
    database.start_database(city_name = 'Питер')
    database.start_database(city_name = 'Казань')
    
    #### 
    database.start_database(
                            user_first_name = 'Максим',
                            user_last_name = 'Терлецкий',
                            user_age = 28,
                            user_gender_id = 2,
                            user_city_id = 1,
                            about_user = 'Прогер мэн!'
                            )

    database.start_database(
                            user_first_name = 'Мария',
                            user_last_name = 'Ивановна',
                            user_age = 35,
                            user_gender_id = 1,
                            user_city_id = 2,
                            about_user = 'Бизнес вумен!'
                            )

    database.start_database(
                            user_first_name = 'Борис',
                            user_last_name = 'Борисович',
                            user_age = 55,
                            user_gender_id = 2,
                            user_city_id = 3,
                            about_user = 'Мачо мэн!'
                            )

    ### Учесть photo1 NOT NULL
    ### Учесть photo2, photo3
    database.start_database(
                            user_id = 1,
                            partner_first_name = 'Аня',
                            partner_last_name = 'Ивановна',
                            partner_age = 26,
                            partner_gender_id = 1,
                            partner_profile = 'SexyAnyka',
                            photo1 = 'photo1',
                            photo2 = 'photo2',
                            photo3 = 'photo3',
                            partner_city_id = 1
                            )
    
    def drop_duplicates(data):
        result = {}
        for d in data:
            name = d['user_first_name']
            if name not in result:
                result[name] = {}
            for key, value in d.items():
                if key != 'user_first_name' and value is not None:
                    result[name][key] = value
    
    ### Пересмотреть джойны
    ### ЕСТЬ ДУБЛИКАТЫ((( => нужна функция drop_duplicates
    print(database.get_db_table())
    print(drop_duplicates(database.get_db_table()))
    
    ### Удаление
    # database.delete_user(Users, 'id', 1)
    # database.delete_user(Users, 'id', 2)
    # gitflow (посмотреть)
    # SOLID
    
    # Gitflow (в main ветку)
    # Поправить таблички (добавить поля) + о
    
    # Придумать интерфейс (регистрация)
    
    
    