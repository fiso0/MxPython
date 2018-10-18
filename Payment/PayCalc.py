#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 社保和公积金基数（每年7月更新）
SB = 10400
# 社保和公积金
S = SB * (0.08 + 0.02 + 0.003 + 0.08) + 7
# 缴税基数
T = 5000
# 税率参数表
K = [(0, 0, 3000), (0.10, 210, 12000), (0.20, 1410, 25000), (0.25, 2660, 35000), (0.30, 4410, 55000),
     (0.35, 7160, 80000), (0.45, 15160, 0)]


# 输入：应发工资
# 输出：实发薪资
def calc_payment(I):
	# 实发薪资y(应发工资x,参数k1,参数k2)公式：
	# y(x,k1,k2)=(x-1910.2)-((x-1910.2-5000)*k1-k2)
	# x                             y
	# 9910.2=3000+1910.2+5000       7910
	# 18910.2=12000+1910.2+5000     16010
	# 31910.2=25000+1910.2+5000     26410
	# 41910.2=35000+1910.2+5000     33910
	# 61910.2=55000+1910.2+5000     47910
	# 86910.2=80000+1910.2+5000     64160

	# 参数
	for n in range(0, 7):
		if (n == 6):
			break
		if (I < S + T + K[n][2]):
			break
	k1, k2 = K[n][0:2]

	P = (I - S) - ((I - S - T) * k1 - k2)
	return P

def calc_tax(I):
	# 参数
	for n in range(0, 7):
		if (n == 6):
			break
		if (I < S + T + K[n][2]):
			break
	k1, k2 = K[n][0:2]

	tax = ((I - S - T) * k1 - k2)
	return tax

def calc_income(P):
	# 参数
	for n in range(0, 7):
		if (n == 6):
			break
		if (P < calc_payment(S + T + K[n][2])):
			break
	k1, k2 = K[n][0:2]

	I = (P - k1 * T - k2) / (1 - k1) + S
	return I


if __name__ == '__main__':
	I = 11280  # 应发工资（包括出勤薪资+奖金+福利）
	P = calc_payment(I)  # 税后实发
	print("税前=%d,税后=%d" % (I, P))

	P1 = P - 200
	I1 = calc_income(P1)
	print("税后=%d,税前=%d" % (P1, I1))

	# 收入取整十倍
	I2 = int(I1 / 10) * 10
	P2 = calc_payment(I2)
	print("税前=%d,税后=%d" % (I2, P2))

	input()
