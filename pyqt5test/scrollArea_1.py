import sys
from PyQt5.QtWidgets import *


class MainWindow(QWidget):
	def __init__(self, ):
		super().__init__()

		# 创建顶层widget，比滚动条widget小
		topWidget = QWidget(self)  # self是QWidget时，注意QWidget(self) 内的self!!
		topWidget.setGeometry(0,0,300,500)  # self是QMainWindow时不需要这句
		# self.setCentralWidget(topWidget)  # self是QMainWindow才可以setCentralWidget

		# 创建滚动条widget，比顶层widget大
		self.scrollWidget = QWidget()
		self.scrollWidget.setMinimumSize(250, 2000)  # 设置滚动条的尺寸

		# 在滚动条widget内添加20个按键
		for filename in range(20):
			self.MapButton = QPushButton(self.scrollWidget)
			self.MapButton.setText(str(filename))
			self.MapButton.move(10, filename * 40+10)

		# 创建一个滚动条，添加滚动条widget
		self.scroll = QScrollArea()
		self.scroll.setWidget(self.scrollWidget)

		# 创建一个layout，添加滚动条
		self.vbox = QVBoxLayout()
		self.vbox.addWidget(self.scroll)

		# 设置顶层widget的layout
		topWidget.setLayout(self.vbox)
		topWidget.show()

		# self.statusBar().showMessage("底部信息栏")  # self是QWidget时，无状态栏
		self.resize(300, 500)
		self.show()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWindow = MainWindow()
	# mainWindow.show()
	sys.exit(app.exec_())