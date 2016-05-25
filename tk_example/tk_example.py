from tkinter import *
import logging

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.helloLabel = Label(self, text='Hello, world!')
		self.helloLabel.pack()
		self.quitButton = Button(self, text='Quit', command=self.quit)
		self.quitButton.pack()

try:
	app = Application()
	# 设置窗口标题:
	app.master.title('Hello World'+b'123') # 这会产生logging：ERROR:root:Can't convert 'bytes' object to str implicitly
	# app.master.title('Hello World')
	# 主消息循环:
	app.mainloop()
except Exception as e:
	logging.basicConfig(filename='tk_example.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	logging.error(str(e))
	
# app = Application()
# # 设置窗口标题:
# app.master.title('Hello World')
# # 主消息循环:
# app.mainloop()
