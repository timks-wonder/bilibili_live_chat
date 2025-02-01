import live2d.v3.live2d as live2d
import pygame
from zimu import *

# 初始化Pygame和OpenGL
pygame.init()
live2d.init()
display = (800, 600)
screen = pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
live2d.glewInit()

# 加载Live2D模型
model = live2d.LAppModel()
model.LoadModelJson(r"D:\pythonProject\Live2D-Python-master\resources\Hiyori\Hiyori.model3.json")
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
window = DesktopSubtitle()
window.full_text = 'Hello World !'
window.show()
words = ['你好', '你是谁？', '嗒嘀嗒', 'momo', '呱唧', '857857', '啦啦啦啦啦', '哈喽，三库', '三库very much']


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            window.full_text = words[a]
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

sys.exit(app.exec_())
