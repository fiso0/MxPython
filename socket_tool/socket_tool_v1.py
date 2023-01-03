import time
import sys

# server
MX_SERVER_DOMAIN = 'agnss-server-2.wh-mx.com'
MX_SERVER_PORT_A = 6000
MX_SERVER_PORT_D = 6001

WNLBS_SERVER_DOMAIN = 'agnss-server-1.wh-mx.com'
WNLBS_SERVER_PORT_A = 32101
WNLBS_SERVER_PORT_D = 2101

AGNSS_GET_DATA = b'GET /v1/device/agnss?client_id=cmcc-mxt535&device_id=356674060511518&protocol=whmx&data_type=eph&gnss=gps%2Cbds&pos=30.50%2C114.39 HTTP/1.1\r\n\r\n'
DGNSS_GET_DATA = b''

BUF_LEN = 1024


# 检查是否接收完整
def check_len(data):
	import re

	# 分离HTTP头和内容
	header, content=data.split(b'\r\n\r\n', 1)

	# 检查实际内容长度
	content_actual_len = len(content)

	# 获取应得内容长度
	try:
		content_desire_len = int(re.search(r'(content-length: )(\d*)',header.decode('utf-8')).group(2))
		# print('content-length: ',str(content_desire_len),', received: ',str(content_actual_len))
		if content_actual_len == content_desire_len:
			cmp_res = True
		else:
			cmp_res = False
	except Exception as e:
		cmp_res = False
		# logging.warning(str(e)+' [in check_len]')

	return cmp_res


# 输出“[时间]接受内容：***”
def print_recv(bytes):
	print("%s 接收%d字节:\n%s\n"%(time.strftime('%H:%M:%S', time.localtime()),len(bytes),bytes.decode('utf-8')))


def delay(sec):
	print("等待%ds..."%(sec))
	time.sleep(sec)

# 从给定的地址和端口接收（广播）内容
def recv_from(addr, port):
	import socket

	# 创建一个socket 使用IPv4 TCP
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# 建立连接
	s.connect((addr, port))

	while True:
		# 每次最多接收BUF_LEN字节
		try:
			d = s.recv(BUF_LEN)
			if d:
				print_recv(d)

			else:
				break
		except Exception as e:
			print("发生错误："+e)
			break
	# 关闭连接
	s.close()
	print("关闭连接")


# 向给定的地址和端口发送请求，并接收（响应）内容，从响应中解析长度，若接收正确则主动断开连接
def send_recv(addr, port, send=None):
	import socket

	# 创建一个socket 使用IPv4 TCP
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# 建立连接
	s.connect((addr, port))

	if send is not None:
		# 发送数据 获取内容
		s.send(send)

	buffer = []
	while True:
		# 每次最多接收BUF_LEN字节
		try:
			d = s.recv(BUF_LEN)
			if d:
				print_recv(d)
				buffer.append(d)
				data=b''.join(buffer)
				# 检查是否接收完整
				same_len = check_len(data)
				if same_len: # 已接收完整
					print("接收完成")
					break
			# 反复接收直到返回空 表示接收完毕
			else:
				break
		except Exception as e:
			print("发生错误："+e)
			break
	# 关闭连接
	s.close()
	print("关闭连接")


HOW_TO = '''
1.梦芯AGNSS服务器测试
2.梦芯DGNSS服务器测试
3.导航院AGNSS服务器测试(单次)
4.导航院DGNSS服务器测试(单次)
5.导航院AGNSS服务器测试(多次)
6.导航院DGNSS服务器测试(多次)
请输入数字：
'''

if len(sys.argv) >= 2:
	instruction = sys.argv[1]
else:
	instruction = input(HOW_TO)
if instruction == '5' or instruction == '6':
	if len(sys.argv) >= 3:
		second = int(sys.argv[2])
	else:
		second = int(input("间隔时间(s):"))

if instruction == '1':
	recv_from(MX_SERVER_DOMAIN, MX_SERVER_PORT_A)
elif instruction == '2':
	recv_from(MX_SERVER_DOMAIN, MX_SERVER_PORT_D)
elif instruction == '3':
	send_recv(WNLBS_SERVER_DOMAIN, WNLBS_SERVER_PORT_A, AGNSS_GET_DATA)
elif instruction == '4':
	send_recv(WNLBS_SERVER_DOMAIN, WNLBS_SERVER_PORT_D, DGNSS_GET_DATA)
elif instruction == '5':
	while True:
		send_recv(WNLBS_SERVER_DOMAIN, WNLBS_SERVER_PORT_A, AGNSS_GET_DATA)
		delay(second)
elif instruction == '6':
	while True:
		send_recv(WNLBS_SERVER_DOMAIN, WNLBS_SERVER_PORT_D, DGNSS_GET_DATA)
		delay(second)
