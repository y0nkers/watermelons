import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from config import api_token, group_id
from files import arkadiy, watermelons

session = vk_api.VkApi(token = api_token)
longpoll = VkBotLongPoll(session, group_id)
isScheduled = False
chat_id = -1


def get_name(uid: int) -> str:
    data = session.method("users.get", {"user_ids": uid})[0]
    return "{} {}".format(data["first_name"], data["last_name"])


def sendMsg(id, text):
    session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})


def sendWatermelon(id, text, watermelon_to_send):
    session.method('messages.send', {'chat_id': id, 'message': text, 'attachment': watermelon_to_send, "random_id": 0})


def listenForEvents():
    global isScheduled, chat_id
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.from_chat:
                        chat_id = event.chat_id
                        user = event.object.message['from_id']
                        msg = event.object.message['text'].lower()
                        if "алим" in msg:
                            sendMsg(chat_id, 'Алим - хороший человек.')
                        elif "аркадий" in msg:
                            sendMsg(chat_id, 'бебра')
                        elif msg == 'хочу арбуз' or msg == 'хачу арбуз' or msg == 'хачю арбуз':
                            if user == 143409911:
                                sendWatermelon(chat_id, 'Перехочешь, Аркадий', arkadiy)
                            else:
                                watermelon = random.randint(0, len(watermelons) - 1)
                                sendWatermelon(chat_id, f'Держи арбуз, [id{user}|{get_name(user)}]',
                                               watermelons[watermelon])
                        elif msg == '!арбуз' and not isScheduled:
                            isScheduled = True
        except Exception as e:
            pass


def jobMorning():
    global chat_id
    arbuz = random.randint(0, len(watermelons) - 1)
    if chat_id != -1:
        sendWatermelon(chat_id, 'Доброе утро! 🍉', watermelons[arbuz])


def jobDay():
    global chat_id
    arbuz = random.randint(0, len(watermelons) - 1)
    if chat_id != -1:
        sendWatermelon(chat_id, 'Добрый день! 🍉', watermelons[arbuz])


def jobEvening():
    global chat_id
    arbuz = random.randint(0, len(watermelons) - 1)
    if chat_id != -1:
        sendWatermelon(chat_id, 'Добрый вечер! 🍉', watermelons[arbuz])

def main():
    today = datetime.today()
    newTime = today.replace(day = today.day, hour = 10, minute = 0, second = 0, microsecond = 0) + timedelta(days = 1)
    delta = newTime - today
    secs = delta.total_seconds()
    scheduler1 = BackgroundScheduler()
    scheduler1.add_job(jobMorning, 'interval', seconds = secs)
    scheduler1.start()
    newTime = today.replace(day = today.day, hour = 14, minute = 0, second = 0, microsecond = 0) + timedelta(days = 1)
    delta = newTime - today
    secs = delta.total_seconds()
    scheduler2 = BackgroundScheduler()
    scheduler2.add_job(jobDay, 'interval', seconds = secs)
    scheduler2.start()
    newTime = today.replace(day = today.day, hour = 18, minute = 0, second = 0, microsecond = 0) + timedelta(days = 1)
    delta = newTime - today
    secs = delta.total_seconds()
    scheduler3 = BackgroundScheduler()
    scheduler3.add_job(jobEvening, 'interval', seconds = secs)
    scheduler3.start()

    listenForEvents()


if __name__ == '__main__':
    main()
