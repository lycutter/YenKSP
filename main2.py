import re, collections
from graph import DiGraph
import algorithms, time
import json
from datetime import datetime
from multiprocessing import Pool
from multiprocessing import Manager


def dataProcess(carPath, crossPath, roadPath):
    carData = []
    crossData = []
    roadData = []
    with open(carPath, 'r') as lines:
        for line in lines:
            line = line.split(',')
            if re.findall("\d+", line[0]) != []:
                line[0] = re.findall("\d+", line[0])[0]
            if re.findall("\d+", line[-1]) != []:
                line[-1] = re.findall("\d+", line[-1])[0]
            # for i in range(len(line)):
            #     line[i] = int(line[i].strip())
            carData.append(line)
    with open(roadPath, 'r') as lines:
        for line in lines:
            line = line.split(',')
            if re.findall("\d+", line[0]) != []:
                line[0] = re.findall("\d+", line[0])[0]
            if re.findall("\d+", line[-1]) != []:
                line[-1] = re.findall("\d+", line[-1])[0]
            roadData.append(line)
    with open(crossPath, 'r') as lines:
        for line in lines:
            line = line.split(',')
            if re.findall("\d+", line[0]) != []:
                line[0] = re.findall("\d+", line[0])[0]
            if re.findall("\d+", line[-1]) != []:
                line[-1] = re.findall("\d+", line[-1])[0]
            crossData.append(line)

    carData = carData[1:]
    for i in range(len(carData)):
        for j in range(len(carData[i])):
            carData[i][j] = int(carData[i][j].strip())
    roadData = roadData[1:]
    for i in range(len(roadData)):
        for j in range(len(roadData[i])):
            roadData[i][j] = int(roadData[i][j].strip())
    crossData = crossData[1:]
    for i in range(len(crossData)):
        for j in range(len(crossData[i])):
            crossData[i][j] = int(crossData[i][j].strip())
            if crossData[i][j] == 1:
                crossData[i][j] = -1
    return carData, crossData, roadData


def generateJson(edges, start, end):
    d = collections.defaultdict(dict)
    # _, *data = [re.findall('(?<=")\w+(?=")', i) for i in edges]
    # for a, b, c in data:
    #     d[a][b] = int(c)
    for i in range(len(edges)):
        a = edges[i][0]
        b = edges[i][1]
        c = edges[i][2]
        d[a][b] = int(c)

    test_json = json.dumps(d)
    with open('test.json', 'w') as f:
        f.write(test_json)


def thread1(G, carData, roadData, returndict1):
    finalPath = []
    for carNum in range(0, int(len(carData) / 2)):
        # items = algorithms.ksp_yen(G, '51', '3', 5)
        items = algorithms.ksp_yen(G, str(carData[carNum][1]), str(carData[carNum][2]), 3)
        for path in items:
            # print(str(carNum) + "Cost:%s\t%s" % (path['cost'], "->".join(path['path'])))
            carRoute = path['path']
            length = len(carRoute)
            carRoute.reverse()
            print("1111111111111111111111111")

            carRouteTmp = []
            for i in range(1, length):
                for j in range(len(roadData)):
                    if ((roadData[j][-3] == int(carRoute[length - i]) and roadData[j][-2] == int(
                            carRoute[length - i - 1])) or
                            (roadData[j][-2] == int(carRoute[length - i]) and roadData[j][-3] == int(
                                carRoute[length - i - 1]))):
                        carRouteTmp.append(roadData[j][0])
            finalPath.append(carRouteTmp)

    returndict1["result"] = finalPath


def thread2(G, carData, roadData, returndict2):
    finalPath = []
    for carNum in range(int(len(carData) / 2), len(carData)):
        # items = algorithms.ksp_yen(G, '51', '3', 5)
        items = algorithms.ksp_yen(G, str(carData[carNum][1]), str(carData[carNum][2]), 3)

        for path in items:
            carRoute = path['path']

            length = len(carRoute)
            carRoute.reverse()
            print("2222222222222222222222222")
            # for i in range(len(carRoute)):
            #     f.write(carRoute[i])
            #     if i != len(carRoute) - 1:
            #         f.write(',')
            # f.write('\n')

            carRouteTmp = []
            for i in range(1, length):
                for j in range(len(roadData)):
                    if ((roadData[j][-3] == int(carRoute[length - i]) and roadData[j][-2] == int(
                            carRoute[length - i - 1])) or
                            (roadData[j][-2] == int(carRoute[length - i]) and roadData[j][-3] == int(
                                carRoute[length - i - 1]))):
                        carRouteTmp.append(roadData[j][0])
            finalPath.append(carRouteTmp)
    returndict2["result"] = finalPath


def main(carData, roadData):
    G = DiGraph("net5")
    manager = Manager()
    return_dict1 = manager.dict()
    return_dict2 = manager.dict()

    start = datetime.now()
    p = Pool(2)
    p.apply_async(thread1, args=(G, carData, roadData, return_dict1))
    p.apply_async(thread2, args=(G, carData, roadData, return_dict2))
    p.close()
    p.join()

    # for carNum in range(int(len(carData) / 3), len(carData)):
    #     # items = algorithms.ksp_yen(G, '51', '3', 5)
    #     items = algorithms.ksp_yen(G, str(carData[carNum][1]), str(carData[carNum][2]), 2)
    #     finalPath = []
    #     for path in items:
    #         print("333333333333333333333")
    #         # print(str(carNum) + "Cost:%s\t%s" % (path['cost'], "->".join(path['path'])))

    end = datetime.now()
    print((end - start).seconds)

    subResult1 = return_dict1['result']
    subReuslt2 = return_dict2['result']

    allCarRoute = subResult1 + subReuslt2

    for i in range(len(allCarRoute)):
        for j in range(len(allCarRoute[i]) - 1):
            if allCarRoute[i][j] == allCarRoute[i][j+1]:
                print("car ===================== %d" % int(carData[int(i/3)][0]))


    with open('./answer.txt', 'w') as f:
        for i in range(len(carData)):
            f.write(str(carData[i][0]))
            f.write('\n')

            for pathNum in range(3):
                for j in range(len(allCarRoute[0])):
                    f.write(str(allCarRoute[0][j]))
                    if j != len(allCarRoute[0]) - 1:
                        f.write(',')
                f.write('\n')
                allCarRoute.pop(0)
        f.close()

    return 0


if __name__ == "__main__":

    car_path = 'D:/pythonWorkplace/SDK/SDK_python/CodeCraft-2019/train1/car.txt'
    road_path = 'D:/pythonWorkplace/SDK/SDK_python/CodeCraft-2019/train1/road.txt'
    cross_path = 'D:/pythonWorkplace/SDK/SDK_python/CodeCraft-2019/train1/cross.txt'

    carData, crossData, roadData = dataProcess(car_path, cross_path, road_path)

    edges = []

    # 生成地图（双向图）
    for i in range(len(roadData)):

        if (roadData[i][-1] == 1):
            edges.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))
            edges.append((str(roadData[i][-2]), str(roadData[i][-3]), roadData[i][1]))
        else:
            edges.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))
    # generateJson(edges, "1", "20")
    main(carData, roadData)
