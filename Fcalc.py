#!/usr/bin/python3
# -*- coding: utf-8 -*-

F1 = list(range(1580064, 1585000, 96)) # 1580000 len=52
F2 = list(range(1215072, 1230000, 96)) # 1215000 len=156
F_min = 52000-0.026
F_max = 52000+0.026

F_set_1 = set()
F_N1 = []
for f1 in F1:
	N1_min = 131072*f1/F_max
	N1_max = 131072*f1/F_min
	N1 = list(range(int(N1_min)+1, int(N1_max)+1)) # len=4
	for n1 in N1:
		F = f1*131072/n1
		F_set_1.add(F) # len=207
		F_N1.append((F,n1,f1))
		# print('F=%f,N1=%d,F1=%d'%(F,n1,f1))

F_set_2 = set()
F_N2 = []
for f2 in F2:
	N2_min = 131072*f2/F_max
	N2_max = 131072*f2/F_min
	N2 = list(range(int(N2_min)+1, int(N2_max)+1)) # len=3
	for n2 in N2:
		F = f2*131072/n2
		F_set_2.add(F) # len=479
		F_N2.append((F,n2,f2))
		# print('F=%f,N2=%d,F2=%d'%(F,n2,f2))

F_set = F_set_1&F_set_2
for F in F_set:
	for f,n1,f1 in F_N1:
		if(f == F):
			for f,n2,f2 in F_N2:
				if(f == F):
					print('F=%f,N1=%d,F1=%d,N2=%d,F2=%d'%(F,n1,f1,n2,f2))
# F=51999.980715,N1=3983945,F1=1580544,N2=3066360,F2=1216512
# F=51999.980715,N1=3983945,F1=1580544,N2=3077975,F2=1221120
# F=51999.980715,N1=3983945,F1=1580544,N2=3089590,F2=1225728
# F=51999.999447,N1=3990477,F1=1583136,N2=3065149,F2=1216032
input()