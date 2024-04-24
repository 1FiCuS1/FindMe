import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api import VkUpload
import os
from dotenv import load_dotenv

load_dotenv()

def write_msg(sender, message):
    authorize.method('messages.send', {'user_id': sender, 'message': message, 'random_id': get_random_id()})
# image = open('image.png', 'rb') # будем брать топ фото из png файла для анкеты человека
token = os.getenv(key='ACCESS_TOKEN')
authorize = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorize)
upload = VkUpload(authorize)


def create_user_profile(user_id, vk_session):
    user_info = {}
    # Запрос имени
    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': 'Привет! Я бот для знакомств. Давай создадим твою анкету) Как тебя зовут?',
        'random_id': get_random_id()
    })
    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.text == 'привет':
                write_msg(user_id, '! Я бот для знакомств. Давай создадим твою анкету) Как тебя зовут?')
            else:
                user_info['first_name'] = event.text
                break

    # Запрос фамилии
    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': 'Отлично! А какая у тебя фамилия?',
        'random_id': get_random_id()
    })
    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_info['last_name'] = event.text
            break

    # Запрос возраста
    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': 'Прекрасно! Сколько тебе лет?',
        'random_id': get_random_id()
    })
    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_info['age'] = event.text
            break

    # Запрос города
    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': 'Хорошо, мы почти закончили! В каком городе ты живешь? ',
        'random_id': get_random_id()
    })
    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_info['city'] = event.text
            break
    # Запрос увлечений и хобби
    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': 'Прекрасно! Какие у тебя увлечения или хобби?',
        'random_id': get_random_id()
    })
    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_info['hobbies'] = event.text
            break
    # Запрос фото ИЗМЕНИТЬ
    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': 'Отлично! Добавь своё фотографийку, чтобы мы могли узнать тебя лучше',
        'attachment': 'photo',
        'random_id': get_random_id()
    })
    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.attachments:
            user_info['photo'] = event.attachments[0]['photo']['photo_130']
            break
    # Вывод анкеты
    print(f'Анкета пользователя {user_id}: {user_info}')
    for key, value in user_info.items():
        print(f'{key}: {value}')
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        reseived_message = event.text
        if reseived_message == 'привет':
            create_user_profile(user_id=event.user_id, vk_session=authorize)



