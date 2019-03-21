import re, collections
from graph import DiGraph
import algorithms_transport
import json
from datetime import datetime
import math


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


def main(carData, roadData):


    start = datetime.now()

    with open('./answer.txt', 'w') as f:
        G = DiGraph("net5")

        # 5道，4道，3道，2道，1道
        channelCoefficient = [0.9, 0.8, 0.7, 0.6, 0.5]
        # 9, 8, 7, 6, 5, 4, 3, 2, 1
        speedCoefficient = [1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1]

        finalPath = []

        for carNum in range(len(carData)):
            # items = algorithms.ksp_yen(G, '51', '3', 5)
            pathDict = G._data


            items = algorithms_transport.ksp_yen(G, str(carData[carNum][1]), str(carData[carNum][2]), 2)

            for path in items:
                print(str(carNum) + "Cost:%s\t%s" % (path['cost'], "->".join(path['path'])))
                carRoute = path['path']

                length = len(carRoute)
                carRoute.reverse()

                # for i in range(len(carRoute)):
                #     f.write(carRoute[i])
                #     if i != len(carRoute) - 1:
                #         f.write(',')
                # f.write('\n')

                carRouteTmp = []
                carRouteTmp.append(carData[carNum][0])
                carRouteTmp.append(carData[carNum][-1])
                for i in range(1, length):
                    for j in range(len(roadData)):
                        if ((roadData[j][-3] == int(carRoute[length - i]) and roadData[j][-2] == int(
                                carRoute[length - i - 1])) or
                                (roadData[j][-2] == int(carRoute[length - i]) and roadData[j][-3] == int(
                                    carRoute[length - i - 1]))):
                            carRouteTmp.append(roadData[j][0])
                finalPath.append(carRouteTmp)


                carRoute.reverse()

                for i in range(len(carRoute) - 1):

                    currentRoad = finalPath[carNum][i]
                    startPoint = carRoute[i]
                    endPoint = carRoute[i+1]

                    oldRoadLength = 0
                    speed = 0
                    channel = 0

                    for roadNum in range(len(roadData)):
                        if roadData[roadNum][0] == currentRoad:
                            oldRoadLength = roadData[roadNum][1]
                            speed = roadData[roadNum][2]
                            channel = roadData[roadNum][3]

                    newRoadLength = math.ceil(oldRoadLength * channelCoefficient[channel - 1] * speedCoefficient[speed - 1])



                    for p in G._data:
                        if p == startPoint:
                            pathDict[startPoint][endPoint] = newRoadLength

                print("debug")
                break


        f.write('#(carId,StartTime,RoadId...)')
        f.write('\n')

        for i in range(len(finalPath)):
            for j in range(len(finalPath[i])):
                if j == 0:
                    f.write('(')
                f.write(str(finalPath[i][j]))
                if j != len(finalPath[i]) - 1:
                    f.write(',')
                else:
                    f.write(')')
            if i != len(finalPath) - 1:
                f.write('\n')

        f.close()

    end = datetime.now()
    print((end - start).seconds)
    return 0


if __name__ == "__main__":

    car_path = 'D:/pythonWorkPlace/YenKSP-master/train1/car.txt'
    road_path = 'D:/pythonWorkPlace/YenKSP-master/train1/road.txt'
    cross_path = 'D:/pythonWorkPlace/YenKSP-master/train1/cross.txt'
    # answer_path = 'D:/PythonWorkPlace/YenKSP-master/train1/answer.txt'

    carData, crossData, roadData = dataProcess(car_path, cross_path, road_path)

    edges = []

    # 生成地图（双向图）
    for i in range(len(roadData)):

        if (roadData[i][-1] == 1):
            edges.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))
            edges.append((str(roadData[i][-2]), str(roadData[i][-3]), roadData[i][1]))
        else:
            edges.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))
    generateJson(edges, "1", "20")
    main(carData, roadData)
