#!/usr/bin/python
from zeep import Client
import hashlib
######################################################################################################
wsdl = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl"
password = hashlib.sha256("VTR!xk5H_!HjP9J".encode("utf-8")).hexdigest()
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


parameters = ("3338561620@qq.com",password)
list_resultString_pH = client.service.getEcNumbersFromPhOptimum(*parameters)
parameters = ("3338561620@qq.com",password)
list_resultString_Cofactor = client.service.getEcNumbersFromCofactor(*parameters)
parameters = ("3338561620@qq.com",password)
list_resultString_Temp = client.service.getEcNumbersFromTemperatureOptimum(*parameters)

try:
    for i in list_resultString_pH:
        dict1 = {}
        parameters = ("3338561620@qq.com", password, "ecNumber*" + i, "phOptimum*", "phOptimumMaximum*", "commentary*", "organism*","literature*")
        resultString_pH = client.service.getPhOptimum(*parameters)
        dict1['ecNumber'] = i
        pairs = [(j['organism'], eval(j['phOptimum'])) for j in resultString_pH if j['phOptimum'] != '-999']
        dict1.update(average_values(pairs))
        print('ecNumber:' + i + 'Ph')
        f = open('brenda/Ph/' + i + '.txt', 'w')
        for m in list(dict1.keys()):
            if m == 'ecNumber':
                pass
            else:
                f.write(m + '\t')
                f.write(str(dict1[m]) + '\n')
        f.close()
        print('Done')
except:
    pass


# parameters = ("3338561620@qq.com",password,"ecNumber*", "cofactor*", "commentary*", "organism*", "ligandStructureId*", "literature*")
# resultString_Cofactor = client.service.getCofactor(*parameters)
# parameters = ("3338561620@qq.com",password,"ecNumber*", "temperatureOptimum*", "temperatureOptimumMaximum*", "commentary*", "organism*", "literature*")
# resultString_Temp = client.service.getTemperatureOptimum(*parameters)


