import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import threading
import wikipedia
import vkbd
from static_messages import STATIC_MESSAGES

authorize = vk_api.VkApi(token='ad6d1569fcd231ba7bb3af6d021144dc81a88d186f7b18b76fd5f0016a0ff5448c1ca33d649a2789b6975')
getting_api = authorize.get_api()
vk = authorize.get_api()
longpoll = VkBotLongPoll(authorize, group_id=206090038)
wikipedia.set_lang("Ru")

cooldown = 5
max_counts = 10
count = 1

print("██████╗░░█████╗░████████╗"
      "\n██╔══██╗██╔══██╗╚══██╔══╝"
      "\n██████╦╝██║░░██║░░░██║░░░"
      "\n██╔══██╗██║░░██║░░░██║░░░"
      "\n██████╦╝╚█████╔╝░░░██║░░░"
      "\n╝╚═╝░░╚═╝╚═════╝░░╚════╝░")



def get_name(from_id):
    if from_id > 0:
        sender_info = getting_api.users.get(user_ids=from_id)[0]
        first_name = sender_info.get('first_name')
        last_name = sender_info['last_name']
        full_name = first_name + ' ' + last_name
        return [full_name, first_name, last_name]


def get_gender(from_id):
    if from_id > 0:
        sinfo = vk.users.get(user_ids=from_id, fields='sex')[0]
        sex = sinfo.get('sex')
        if sex == 1:
            sex = "Женщина"
        elif sex == 2:
            sex = "Мужчина"
        else:
            sex = "Не указанно"
        return sex


def get_years(from_id):
    if from_id > 0:
        Yinfo = vk.users.get(user_ids=from_id, fields='bdate')[0]
        years = Yinfo.get('bdate')
        if years is None:
            return "Скрыта"
        else:
            return str(years)


def get_closed(from_id):
    if from_id > 0:
        close = vk.users.get(user_ids=from_id, fields='is_closed')[0]['is_closed']
        if close is False:
            return "Открытый"
        elif close is True:
            return "Закрытый"
        else:
            print("Опять все пошло по не тому месту....")


def talking():
    for event in longpoll.listen():
        fwd = event.object.message
        td = event.object.message['from_id']
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text') != "":
            sender = event.chat_id
            msg = event.message.text
            is_new = vkbd.check_is_new(td)
            if is_new is None:
                vkbd.add_new_user(td)



        kd_info = VkKeyboard(one_time=False, inline=True)
        kd_info.get_empty_keyboard()
        kd_info.add_button('♦Информация о боте♦', color=VkKeyboardColor.POSITIVE)
        kd_info.add_button('♦info об игре "bones"♦', color=VkKeyboardColor.POSITIVE)

        shop = VkKeyboard(one_time=False, inline=True)
        shop.get_empty_keyboard()
        shop.add_button('♦Автомобили♦', color=VkKeyboardColor.POSITIVE)
        shop.add_button('♦Питомцы♦', color=VkKeyboardColor.POSITIVE)
        shop.add_button('♦Дома-Квартиры♦', color=VkKeyboardColor.POSITIVE)
        shop.add_line()
        shop.add_button('♦Бизнесы♦', color=VkKeyboardColor.POSITIVE)

        kd_games = VkKeyboard(one_time=False, inline=True)
        kd_games.get_empty_keyboard()
        kd_games.add_button('♦Кости♦', color=VkKeyboardColor.POSITIVE)

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('♦Игры♦', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('♦Баланс♦', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('♦Профиль♦', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('♦Информация♦', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('♦Магазин♦', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('♦Работы♦', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('♦Википедия♦', color=VkKeyboardColor.PRIMARY)

        job = VkKeyboard(inline=True, one_time=False)
        job.get_empty_keyboard()
        job.add_button('♦Уборщик♦', color=VkKeyboardColor.POSITIVE)

        avto = VkKeyboard(inline=True, one_time=False)
        avto.get_empty_keyboard()
        avto.add_button('♦Жигули♦', color=VkKeyboardColor.POSITIVE)

        yes_no = VkKeyboard(inline=True, one_time=False)
        yes_no.get_empty_keyboard()
        yes_no.add_button('♦Купить жигули♦', VkKeyboardColor.POSITIVE)
        yes_no.add_button('♦Отказаться♦', VkKeyboardColor.NEGATIVE)

        def roll_50():
            c1 = 0.5
            curent = vkbd.get_row(td, "money")
            bet = curent * c1
            dice = random.randrange(1, 14)
            vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message=f"Выпало {str(dice)}")

            if dice in [4, 7, 11]:
                vkbd.change_row(td, "money", curent+bet)
                vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message=f"{get_name(from_id=td)[1]} Победа!")
            elif dice in [2, 3, 12, 5]:
                vkbd.change_row(td, "money", curent-bet)
                vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message=f"{get_name(from_id=td)[1]} Проигрыш!")
            else:
                vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message=f"{get_name(from_id=td)[1]} Уходим в ноль!")
            vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message=f"{get_name(from_id=td)[1]} Баланс: {str(vkbd.get_row(td, 'money'))}")

        def null_count():
            vkbd.change_row(td, "job_status", 1)
            vkbd.change_row(td, "is_on_rest", 0)
            vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                message=STATIC_MESSAGES["work_access"]
            )

        def job_get_money(from_id):
            if from_id > 0:

                if vkbd.get_row(td, "job_status") == 10:
                    if vkbd.get_row(td, "is_on_rest") == 0:
                        vkbd.change_row(td, "is_on_rest", 1)
                        t = threading.Timer(300.0, null_count)
                        t.start()
                    else:
                        print("Еще нет!")
                    return STATIC_MESSAGES["rest_needed"]
                else:
                    salary = 35000
                    new_money = salary + vkbd.get_row(td, "money")
                    new_job_status = vkbd.get_row(td, "job_status") + 1
                    vkbd.change_row(td, "money", new_money)
                    vkbd.change_row(td, "job_status", new_job_status)
                    return f"На баланс зачисленно: {salary} \n Баланс: {vkbd.get_row(td, 'money')}"

        def minus_money_car(from_id):
            global uns
            if from_id > 0:
                if "♦Купить жигули♦" in str(event):
                    if event.from_chat:
                        car = "lada"
                        if car == "lada":
                            price = 300000
                            if uns == 0 or uns < price:
                                return STATIC_MESSAGES['not_enought_money']
                            else:
                                uns -= price
                                return "\n -" + str(price) + " uns \n Баланс: " + str(uns)

        if "!kick" in str(event):
            if event.from_chat:
                if getting_api.users.get(user_ids=td).is_admin:
                    vk.messages.removeChatUser(chat_id=event.chat_id,
                                               user_id=event.message.reply_message['from_id'])
                else:
                    continue

        if 'reply_message' in fwd:
            continue
        else:
            if "!Клавиатура" in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=keyboard.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=STATIC_MESSAGES['kb_active'],
                        chat_id=event.chat_id
                    )

            if "♦Профиль♦" in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=keyboard.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=get_name(from_id=td)[1] + ' - ваш профиль: '
                                                                   '\n Полное имя: ' + get_name(from_id=td)[0] +
                                '\n id: ' + str(td) + "\n Пол: " + get_gender(
                            from_id=td) + '\n Дата рождения: ' + get_years(
                            from_id=td) + "\n Состояние профиля: " + get_closed(from_id=td),
                        chat_id=event.chat_id
                    )

            if "♦Википедия♦" in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=keyboard.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=STATIC_MESSAGES['wiki'],
                        chat_id=event.chat_id
                    )

            if '♦Информация♦' in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=kd_info.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=STATIC_MESSAGES['info'],
                        chat_id=event.chat_id
                    )

            if '♦Баланс♦' in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=keyboard.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=f'Баланс: {vkbd.get_row(td, "money")}',
                        chat_id=event.chat_id
                    )

            if '♦Игры♦' in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=kd_games.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=STATIC_MESSAGES["games"],
                        chat_id=event.chat_id
                    )

            if '♦Кости♦' in str(event):
                if event.from_chat:
                    roll_50()

            try:
                if "!Википедия" in str(event):
                    if event.from_chat:
                        wiki = msg.replace('.', '').split()
                        query = wiki[1]
                        vk.messages.send(
                            key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                            server=('https://lp.vk.com/wh206090038'),
                            ts=('64'),
                            random_id=get_random_id(),
                            message=wikipedia.summary(query, sentences=0, chars=0, auto_suggest=True,
                                                      redirect=True) + "\n" + str(
                                wikipedia.page(query).references[0]),
                            chat_id=event.chat_id
                        )
            except vk_api.exceptions.ApiError:
                vk.messages.send(
                    key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                    server=('https://lp.vk.com/wh206090038'),
                    ts=('64'),
                    random_id=get_random_id(),
                    message=STATIC_MESSAGES["too_much_words"],
                    chat_id=event.chat_id
                )
            if "♦Информация о боте♦" in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=kd_info.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=STATIC_MESSAGES['bot_info'],
                        chat_id=event.chat_id
                    )

            if '♦info об игре "bones"♦' in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=kd_info.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=STATIC_MESSAGES['bones'],
                        chat_id=event.chat_id
                    )

            if '♦Магазин♦' in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=shop.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=STATIC_MESSAGES['shop'],
                        chat_id=event.chat_id
                    )

            if "♦Работы♦" in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=job.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=STATIC_MESSAGES['job_start'],
                        chat_id=event.chat_id
                    )

            if "♦Уборщик♦" in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=job.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message="Пол помыт! " + str(vkbd.get_row(td, "job_status")) + "/10 \n " + job_get_money(from_id=td),
                        chat_id=event.chat_id
                    )

            if "♦Отказаться♦" in str(event):
                if event.from_chat:
                    vk.messages.send(
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=STATIC_MESSAGES["reject"],
                        chat_id=event.chat_id
                    )

            if "♦Купить жигули♦" in str(event):
                if event.from_chat:
                    vk.messages.send(
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message="На данный момент автомобилей нет ;(",
                        chat_id=event.chat_id
                    )

            if "♦Автомобили♦" in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=avto.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=STATIC_MESSAGES["avto_shop"],
                        chat_id=event.chat_id
                    )
            if "♦Жигули♦" in str(event):
                if event.from_chat:
                    vk.messages.send(
                        keyboard=yes_no.get_keyboard(),
                        key=('0a9252b579c0fdd123198f6070832ebb34f16f38'),
                        server=('https://lp.vk.com/wh206090038'),
                        ts=('64'),
                        random_id=get_random_id(),
                        message=STATIC_MESSAGES["cars__lada"],
                        chat_id=event.chat_id
                    )
#
talking()
