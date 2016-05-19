# 导入socket库
import socket
import re
import time

'''
域名	agnss-server-1.wh-mx.com
IP	27.17.32.34
端口	32101

GET /v1/device/agnss?client_id=cmcc-mxt535&device_id=356674060511518&protocol=whmx&data_type=eph&gnss=gps%2Cbds&pos=30.50%2C114.39 HTTP/1.1
'''

SERVER_DOMAIN = 'agnss-server-1.wh-mx.com'
SERVER_PORT = 32101
GET_DATA = b'GET /v1/device/agnss?client_id=cmcc-mxt535&device_id=356674060511518&protocol=whmx&data_type=eph&gnss=gps%2Cbds&pos=30.50%2C114.39 HTTP/1.1\r\n\r\n'


def one_try(try_cnt):
	print('start one try...')

	# 设置超时时间
	socket.setdefaulttimeout(10)

	# 创建一个socket 使用IPv4 TCP
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# 建立连接
	s.connect((SERVER_DOMAIN,SERVER_PORT))

	# 发送数据 获取内容
	s.send(GET_DATA)

	buffer=[]
	while True:
		# 每次最多接收1024字节
		try:
			d=s.recv(1024)
			if d:
				buffer.append(d)
			# 反复接收直到返回空 表示接收完毕
			else:
				# 关闭连接
				s.close()
		except:
			break

	data=b''.join(buffer)

	# 分离HTTP头和内容
	header, content=data.split(b'\r\n\r\n', 1)
	# print(header.decode('utf-8'))


	# 检查实际内容长度
	content_actual_len = len(content)

	# 获取应得内容长度
	try:
		content_desire_len = int(re.search(r'(content-length: )(\d*)',header.decode('utf-8')).group(2))
		print('content-length: ',str(content_desire_len),', received: ',str(content_actual_len))
		if content_actual_len == content_desire_len:
			cmp_res = True
		else:
			cmp_res = False
	except:
		cmp_res = False

	if not cmp_res:
		# 失败时，把内容写入文件
		filename = 'agnss_test'+str(try_cnt)+'.txt'
		with open(filename,'wb') as f:
			f.write(data)

	return cmp_res


try_cnt = 0
success_cnt = 0
fail_cnt = 0

while(True):
	try_cnt += 1
	try:
		if(one_try(try_cnt)):
			success_cnt += 1
		else:
			fail_cnt += 1
		print('>>> Total: ',str(try_cnt),', Success: ',str(success_cnt),', Fail: ',str(fail_cnt))
	except exception as e:
		print(e)
	finally:
		print('sleep 2s...')
		time.sleep(2)
