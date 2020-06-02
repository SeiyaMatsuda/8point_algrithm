# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
import sys
from typing import List, Tuple

import cv2
import os.path
class mouseParam:
    def __init__(self, input_img_name):
        #マウス入力用のパラメータ
        self.mouseEvent = {"x":None, "y":None, "event":None, "flags":None}
        #マウス入力の設定
        cv2.setMouseCallback(input_img_name, self.__CallBackFunc, None)

    #コールバック関数
    def __CallBackFunc(self, eventType, x, y, flags, userdata):

        self.mouseEvent["x"] = x
        self.mouseEvent["y"] = y
        self.mouseEvent["event"] = eventType
        self.mouseEvent["flags"] = flags

    #マウス入力用のパラメータを返すための関数
    def getData(self):
        return self.mouseEvent

    #マウスイベントを返す関数
    def getEvent(self):
        return self.mouseEvent["event"]

    #マウスフラグを返す関数
    def getFlags(self):
        return self.mouseEvent["flags"]

    #xの座標を返す関数
    def getX(self):
        return self.mouseEvent["x"]

    #yの座標を返す関数
    def getY(self):
        return self.mouseEvent["y"]

    #xとyの座標を返す関数
    def getPos(self):
        return (self.mouseEvent["x"], self.mouseEvent["y"])
if __name__ == "__main__":
    file1 = input("画像１のファイル名")
    file2 = input("画像2のファイル名")
    file=[file1,file2]
    coordinate_point = []
    for f in file:
        #入力画像
        path=os.path.join(r'C:\Users\yaase\Desktop\eizou', f)
        read = cv2.imread(path)

        #表示するWindow名
        window_name = "input window"

        #画像の表示
        cv2.imshow(window_name, read)

        #コールバックの設定
        mouseData = mouseParam(window_name)
        while 1:
            cv2.waitKey(20)
            #左クリックがあったら表示
            if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
                coordinate_point.append(mouseData.getPos())
                coordinate_point=list(dict.fromkeys(coordinate_point))
                print(coordinate_point)
            #右クリックがあったら終了

            elif mouseData.getEvent() == cv2.EVENT_RBUTTONDOWN:
                break;

        cv2.destroyAllWindows()
    uvmat=[coordinate_point[idx]+coordinate_point[idx+8] for idx in range(int(len(coordinate_point)/2))]

    print(uvmat)
    print("Finished")


