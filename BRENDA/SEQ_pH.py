import time
from zeep import Client
import hashlib
######################################################################################################
wsdl = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl"
email = '邮箱'
password = hashlib.sha256("注册的密码".encode("utf-8")).hexdigest()
client = Client(wsdl)
import os

def get_all_files(folder_path):
    file_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_names.append(file.strip('.txt'))
    return file_names
def find_different_elements(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    different_elements = list(set1 - set2)
    return different_elements
def merge_key_value_pairs(pairs):
    result = {}

    for key, value in pairs:
        # 如果键不在结果字典中，就将键和一个空列表添加到结果字典中
        if key not in result:
            result[key] = []
        # 将值添加到对应键的列表中
        result[key].append(value)
    return result
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

folder_path_pH = r"sequence\pH"
file_names_pH = get_all_files(folder_path_pH)

parameters = (email,password)
list_resultString_pH = client.service.getEcNumbersFromPhOptimum(*parameters)
parameters = (email,password)
list_resultString_Cofactor = client.service.getEcNumbersFromCofactor(*parameters)
parameters = (email,password)
list_resultString_Temp = client.service.getEcNumbersFromTemperatureOptimum(*parameters)

list_fail_pH = find_different_elements(list_resultString_pH, file_names_pH)
for i in list_fail_pH:
    a = 1
    while a <= 10:
        try:
            dict1 = {}
            parameters = (
            email, password, "ecNumber*" + i, "sequence*", "noOfAminoAcids*", "firstAccessionCode*",
            "source*", "id*", "organism*")
            resultString_pH = client.service.getSequence(*parameters)
            dict1['ecNumber'] = i
            pairs = [(j['organism'], j['sequence']) for j in resultString_pH]
            dict1.update(merge_key_value_pairs(pairs))
            print('ecNumber:' + i + 'pH')
            f = open('sequence/pH/' + i + '.txt', 'w')
            for m in list(dict1.keys()):
                if m == 'ecNumber':
                    pass
                else:
                    f.write(m + '\t')
                    for n in list(set(dict1[m])):
                        f.write(n + '\t')
                    f.write('\n')
            f.close()
            print('Done')
            break
        except:
            print('!!!!!!!!!!!!!!!!!!ecNumer' + i + 'trying for ' + str(a))
            time.sleep(1)
            a = a + 1
