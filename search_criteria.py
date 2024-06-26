import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import json
token = "vk1.a.BIz9EanDLhQLtuSTT5mVGSTvU7mIycKbGSzDDIVisPwVFO7VwFuglk4c8Z87XC1M0dS_fkkVsCll42WTCH5toPeEabcYTxCz6C7gqoLgTEKd6DrSD9uU0tofY8S3AhXZp_1Ln18-CKTWtrRn81IG18MBY2KAMrAIE3L_DuKKkNiW3sKzPQkdScH722rzshSP5asvFd_daoETjY_-2CzvSg"
authorize = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorize)

def create_search_criteria(user_id, vk_session):
    criteria = {}
    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': 'Теперь давай создадим критерий поиска. Пол человека? (1 - мужской, 2 - женский)',
        'random_id': get_random_id()
    })

    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.text == '1':
                criteria['sex'] = 2
            elif event.text == '2':
                criteria['sex'] = 1
            elif event.text == '0':
                criteria['sex'] = 0

            break

    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': 'Возраст от кого?',
        'random_id': get_random_id()
    })

    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            criteria['age_from'] = event.text
            break

    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': 'Возраст до кого?',
        'random_id': get_random_id()
    })

    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            criteria['age_to'] = event.text
            break

    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': 'В каком городе будем искать?',
        'random_id': get_random_id()
    })

    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            criteria['city'] = event.text

            break

    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': 'Какое семейное положение должно быть у человека?(1 - не женат(не замужем)б 2 - встречается, 3 - помолвлен(помолвлена), 4 - женат(замужем), 5 - все сложно, 6 - в активном поске, 7 - влюблен(-а), 8 - в гражданском браке )',
        'random_id': get_random_id()
    })

    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.text == '1':
                criteria['relation'] = 1
            elif event.text == '2':
                criteria['relation'] = 2
            elif event.text == '3':
                criteria['relation'] = 3
            elif event.text == '4':
                criteria['relation'] = 4
            elif event.text == '5':
                criteria['relation'] = 5
            elif event.text == '6':
                criteria['relation'] = 6
            elif event.text == '7':
                criteria['relation'] = 7
            elif event.text == '8':
                criteria['relation'] = 8
            break



 def save_criteria_to_json(criteria,criteria1):
    with open(criteria1, 'w') as f:
        json.dump(criteria, f)

def criteria_from_json(criteria1):
    with open(criteria1, 'r') as f:
        criteria = json.load(f)
        return criteria




for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.text == 'критерии':
            create_search_criteria(user_id=event.user_id, vk_session=authorize)

        break




