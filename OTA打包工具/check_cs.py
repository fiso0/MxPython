with open('ota','rb') as f:
    data_ota = f.read()
    cs = 0
    for data in data_ota:
        cs = cs ^ data

print(cs)
