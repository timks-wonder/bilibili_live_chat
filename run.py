import time
import pygame
from chat import Chatter
from text2voice import Speaker
from show import WhiteBoard
from bilibili_api import Credential, sync, Danmaku
from bilibili_api.live import LiveDanmaku, LiveRoom
import live2d.v3.live2d as live2d
import pygame
from zimu import *

# 自己直播间号
ROOMID = 1982822476
# 凭证 根据回复弹幕的账号填写
credential = Credential(
    sessdata="5613caf2%2C1752583820%2C6e5e0%2A11CjCmhtlrFOfMo9Q3ZV90CLPxfawLb4ASsV4WNU2dg2aPB3LkbQUNOq5nwTv1rko_aH8SVmNwa2pzY3h3OHBMVVpLQVJWUHpNSEUxM2NSLVh4NnZzeXBaMXFJMDF6aGVPMDlDV2ZkbFZtaXJrUFJlaTRsbU9YZGdLeVRCLS1LaHJrdC1EcHl3ZFRBIIEC",
    bili_jct="c43cf2cc3bbbc04d5c77b425775b1efa"
)
# 监听直播间弹幕
monitor = LiveDanmaku(ROOMID, credential=credential)
# 用来发送弹幕
sender = LiveRoom(ROOMID, credential=credential)
# 自己的UID 可以手动填写也可以根据直播间号获取
UID = sync(sender.get_room_info())["room_info"]["uid"]

xxc = Chatter()
xxc_speaker = Speaker()


# 初始化Pygame和OpenGL
pygame.init()
live2d.init()
display = (800, 600)
screen = pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
live2d.glewInit()

# 加载Live2D模型
model = live2d.LAppModel()
model.LoadModelJson(r"C:\Users\jinch\Desktop\try_LLM\Hiyori\Hiyori.model3.json")
model.Resize(800, 600)


# 设置交互回调函数
def onStartCallback(group: str, no: int):
    print(f"Motion [{group}_{no}] started")

def onFinishCallback():
    print("Motion finished")


# 主循环
running = True
a = 0

app = QApplication(sys.argv)
window = DesktopLyrics()
window.lyrics = 'Hello World !'
window.show()

sync(monitor.connect())


@monitor.on("DANMU_MSG")
async def recv(event):
    uid = event["data"]["info"][2][0]

    content = event["data"]["info"][1]
    print(content)
    answer = xxc.chat(content)
    if answer is not None:
        # xxc_speaker.speak(answer)
        board = WhiteBoard()
        board.show(answer)
        print(answer)
        time.sleep(5)

        pygame.quit()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            window.lyrics = words[a]
            window.show()
            x, y = pygame.mouse.get_pos()
            model.ResetPose()
            model.StartMotion('Idle', a, 1)
            model.Touch(x, y, onStartCallback, onFinishCallback)
            a += 1
    if a == 9:
        model.ResetPose()
        a = 0
    live2d.clearBuffer()
    model.Update()
    model.Draw()
    pygame.display.flip()

pygame.quit()





# 启动监听

sys.exit(app.exec_())