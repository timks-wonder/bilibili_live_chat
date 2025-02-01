import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer, QPoint, QRect
from PyQt5.QtGui import QPainter, QFont, QPen, QColor, QPainterPath, QFontMetrics


class DesktopSubtitle(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dragging = False
        self.offset = QPoint()

        # 新增动画相关属性
        self.full_text = ""  # 完整字幕文本
        self.display_text = ""  # 当前显示文本
        self.current_index = 0  # 当前显示字符索引
        self.line_width = 800  # 单行最大宽度（像素）
        self.line_height = 60  # 行高
        self.line_spacing = 10  # 行间距

    def initUI(self):
        # 设置窗口属性：无边框、透明背景、置顶
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 初始位置和大小
        self.setGeometry(300, 300, 900, 300)

        # 字体设置
        self.font = QFont("微软雅黑", 16, QFont.Bold)
        self.metrics = QFontMetrics(self.font)

        # 动画定时器
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_text)
        self.animation_timer.start(150)  # 每个字符显示间隔（毫秒）

    def set_text(self, text):
        """设置新字幕文本并重置状态"""
        self.full_text = text
        self.current_index = 0
        self.display_text = ""
        self.update()

    def update_text(self):
        """逐字更新显示文本"""
        if self.current_index < len(self.full_text):
            self.display_text += self.full_text[self.current_index]
            self.current_index += 1
            self.update()

    def wrap_text(self):
        """自动换行处理"""
        lines = []
        current_line = ""
        current_width = 0

        for char in self.display_text:
            char_width = self.metrics.width(char)

            # 换行条件：当前行宽+新字符宽超过限制 或 遇到换行符
            if current_width + char_width > self.line_width or char == '\n':
                lines.append(current_line.strip())
                current_line = ""
                current_width = 0

            if char != '\n':
                current_line += char
                current_width += char_width

        lines.append(current_line)  # 添加最后一行
        return lines

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.font)

        # 自动换行处理
        wrapped_lines = self.wrap_text()

        # 计算总高度
        total_height = len(wrapped_lines) * (self.line_height + self.line_spacing)
        self.setFixedHeight(total_height + 20)

        # 绘制每行文字
        for i, line in enumerate(wrapped_lines):
            y_pos = 40 + i * (self.line_height + self.line_spacing)
            self.draw_stroked_text(painter, line, 50, y_pos)

    def draw_stroked_text(self, painter, text, x, y):
        """带描边的文字绘制"""
        path = QPainterPath()
        path.addText(x, y, self.font, text)

        # 先画黑色描边
        painter.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine, Qt.RoundCap))
        painter.drawPath(path)

        # 再填充白色
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawPath(path)

    # 保持原有的拖动功能
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopSubtitle()

    # 设置长文本示例（自动换行测试）
    sample_text = "这是一个桌面字幕示例，当文本超过设定的行宽时会自动换行。"
    sample_text += "支持逐字显示效果，并且可以拖动窗口位置。"

    window.set_text(sample_text)
    window.show()
    sys.exit(app.exec_())
