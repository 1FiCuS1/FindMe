from typing import Union
from datetime import datetime

import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from dateutil.relativedelta import relativedelta

# Чат бот в отдельный класс
# БД в отдельный класс (весь ВК запихать)
# Запрос в интернет (поиск по )

def write_message(sender:int, message:str) -> None:
    
    authorize.method(
                    'messages.send', 
                    {'user_id': sender,
                    'message': message,
                    'random_id': get_random_id()}
                )

def get_user_info(sender_id:int, fields:str) -> list:
    
    return authorize.method(
                            'users.get',
                            {'user_ids': sender_id,
                            'fields': ','.join(fields)}
                        )

def determine_age(bdate:str) -> int:
    
    birth_date = datetime.strptime(bdate, "%d.%m.%Y")
    
    return relativedelta(datetime.now(), birth_date).years

def determine_sex(sex_int:int) -> Union[str, None]:
    
    sex_dict = {
                1: 'женкский', 
                2: 'мужской', 
                0: 'пол не указан'
            }
    
    return sex_dict.get(sex_int, None)

# Привет, Вася
# Хочешь зарегистрироваться?))))))
# Выбор: автомат vs анкета

token = "vk1.a.bcavVJC5a-2QnUtlEwgEWsJeddHVlHbm6K7DMJ81l4Y7Y_4TBB3TXFF4VJL1MOW5Yi24gPZScWcXPBz1AuAwXofCiLPJ_odkAP-DeKGmt0tBKGuTENri_oMgTC8B8dLu9ZMmHT2i_E0vxCTduKCyPl8YycsPatzGBoOtutf0SKdb-Afs8khMttSMvnZOOHAe5xaX6AY3C8EFpdk3acMjuA"

authorize = vk_api.VkApi(token = token)
longpoll = VkLongPoll(authorize)

for event in longpoll.listen():
    
    if event.type == VkEventType.MESSAGE_NEW and\
        event.to_me and\
        event.text:
            
            reseived_message = event.text
            sender_id = event.user_id
            
            fields = ["bdate", "city", "sex"]
            sender_info = get_user_info(sender_id, fields)[0]
            
            bdate, city_dict, sex_int = (
                                        sender_info.get(f, None) 
                                        for f in fields
                                )
            
            if city_dict:
                city_name = city_dict.get('title', None)
            
            if bdate and city_name and sex_int:
                
                age = determine_age(bdate)
                sex_name = determine_sex(sex_int)
                
                if reseived_message == "Привет":
                    write_message(sender_id, "Добрый день!")
                    write_message(sender_id, f"{age}, {sex_name}, {city_name}")
                
                elif reseived_message == "Пока":
                    write_message(sender_id, "До свидания")
                
                else:
                    write_message(sender_id, "Я вас не понимаю...")