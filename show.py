import time
import pygame
import tkinter as tk


class WhiteBoard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pygame Text Example")
        self.font = pygame.font.Font(None, 36)  # 使用默认字体，字号为 36

    def show(self, text):
        text = self.font.render(text, True, (255, 255, 255))  # 渲染文字，颜色为白色
        text_rect = text.get_rect(center=(400, 300))  # 获取文字矩形，并居中
        # 填充背景颜色
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, text_rect)
        # 更新屏幕显示
        pygame.display.flip()


# 创建一个窗口
root = tk.Tk()
root.title("Text Box Example")

# 设置窗口大小
root.geometry("400x300")

# 创建一个文本框
text_box = tk.Text(root, height=10, width=50)
text_box.pack(pady=20)

# 在文本框中插入文字
text_box.insert(tk.END, "在Python中，弹出一个文本框展示文字可以通过多种方式实现，具体取决于你的需求和使用的库。以下是一些常见的方法：")

time.sleep(5)

text_box.insert(tk.END, "在Python中，xxxxxxxxxxxxxxxxxxxxxx")

# root.quit()
# 运行主循环

root.mainloop()


