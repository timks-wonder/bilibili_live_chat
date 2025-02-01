import multiprocessing
import live2d.v3.live2d as live2d
import pygame

from chat import Chatter
from text2voice import Speaker
from zimu import *
from bilibili_api import Credential, Danmaku, sync
from bilibili_api.live import LiveDanmaku, LiveRoom


def onStartCallback(group: str, no: int):
    print(f"Motion [{group}_{no}] started")


def onFinishCallback():
    print("Motion finished")


# 皮套人
def function1(data):
    pygame.init()
    live2d.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    live2d.glewInit()

    # 加载Live2D模型
    model = live2d.LAppModel()
    model.LoadModelJson(r"D:\pythonProject\Live2D-Python-master\resources\Hiyori\Hiyori.model3.json")
    model.Resize(800, 600)

    app = QApplication(sys.argv)
    window = DesktopLyrics()
    window.lyrics = 'Hello!'
    window.show()

    while data['running']:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                model.ResetPose()
                model.Touch(x, y, onStartCallback, onFinishCallback)
        if data['motion'] == 1:
            data['motion'] = 0
            window.lyrics = data['answer']
            window.show()
            model.ResetPose()
            model.StartMotion('Idle', data['m_idx'], 1)
            data['m_idx'] += 1
        if data['m_idx'] == 9:
            model.ResetPose()
            data['m_idx'] = 0
        live2d.clearBuffer()
        model.Update()
        model.Draw()
        pygame.display.flip()


# 弹幕监听
def function2(data, message):
    ROOMID = 1982822476
    credential = Credential(
        sessdata="5613caf2%2C1752583820%2C6e5e0%2A11CjCmhtlrFOfMo9Q3ZV90CLPxfawLb4ASsV4WNU2dg2aPB3LkbQUNOq5nwTv1rko_aH8SVmNwa2pzY3h3OHBMVVpLQVJWUHpNSEUxM2NSLVh4NnZzeXBaMXFJMDF6aGVPMDlDV2ZkbFZtaXJrUFJlaTRsbU9YZGdLeVRCLS1LaHJrdC1EcHl3ZFRBIIEC",
        bili_jct="c43cf2cc3bbbc04d5c77b425775b1efa"
    )
    monitor = LiveDanmaku(ROOMID, credential=credential)
    # 启动监听
    @monitor.on("DANMU_MSG")
    async def recv(event):
        # 发送者UID
        uid = event["data"]["info"][2][0]
        # 弹幕文本
        content = event["data"]["info"][1]
        name = event["data"]["info"][0][15]['user']['base']['name']
        m = f'{name}: {content}'
        print(m)

        if content.startswith('@小香橙'):
            message.put(m)
            if message.qsize() >= data['max_len']:
                message.get()
    sync(monitor.connect())


# 大模型
def function3(data, message):
    xxc = Chatter()
    xxc_speaker = Speaker()
    while data['running']:
        if not message.empty():
            msg = message.get()
            data['answer'] = xxc.chat(msg)
            data['motion'] = 1


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    data = manager.dict()
    data['running'] = True
    data['m_idx'] = 0
    data['motion'] = 0
    data['max_len'] = 4
    data['answer'] = None

    message = multiprocessing.Queue()

    # 皮套人
    p_func1 = multiprocessing.Process(target=function1, args=(data,))
    p_func1.start()

    # p_func2 = multiprocessing.Process(target=function2, args=(data, message))
    # p_func2.start()
    #
    # p_func3 = multiprocessing.Process(target=function3, args=(data, message))
    # p_func3.start()

    p_func1.join()
