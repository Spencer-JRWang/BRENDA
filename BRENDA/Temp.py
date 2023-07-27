#!/usr/bin/python
from zeep import Client
import hashlib
######################################################################################################
wsdl = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl"
email = '邮箱'
password = hashlib.sha256("注册的密码".encode("utf-8")).hexdigest()
client = Client(wsdl)

def average_values(key_value_pairs):
    # 创建一个空字典用于存储结果
    result = {}
    # 遍历键值对
    for key, value in key_value_pairs:
        # 如果键不在结果字典中，就将键和一个空列表添加到结果字典中
        if key not in result:
            result[key] = []
        # 将值添加到对应键的列表中
        result[key].append(value)
    # 计算每个键对应值的平均值，并更新结果字典
    for key in result:
        values = result[key]
        average = sum(values) / len(values)
        result[key] = average
    return result


def merge_key_value_pairs(pairs):
    result = {}

    for key, value in pairs:
        # 如果键不在结果字典中，就将键和一个空列表添加到结果字典中
        if key not in result:
            result[key] = []
        # 将值添加到对应键的列表中
        result[key].append(value)
    return result


parameters = (email,password)
list_resultString_pH = client.service.getEcNumbersFromPhOptimum(*parameters)
parameters = (email,password)
list_resultString_Cofactor = client.service.getEcNumbersFromCofactor(*parameters)
parameters = (email,password)
list_resultString_Temp = client.service.getEcNumbersFromTemperatureOptimum(*parameters)


for i in list_resultString_Temp:
    dict1 = {}
    parameters = (email,password,"ecNumber*" + i, "temperatureOptimum*", "temperatureOptimumMaximum*", "commentary*", "organism*", "literature*")
    resultString_Temp = client.service.getTemperatureOptimum(*parameters)
    dict1['ecNumber'] = i
    pairs = [(j['organism'], eval(j['temperatureOptimum'])) for j in resultString_Temp]
    dict1.update(average_values(pairs))
    print('ecNumber:' + i + 'Temp')
    f = open('brenda/Temp/' + i + '.txt', 'w')
    for m in list(dict1.keys()):
        if m == 'ecNumber':
            pass
        else:
            f.write(m + '\t')
            f.write(str(dict1[m]) + '\n')
    f.close()
    print('Done')
