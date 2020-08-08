import cv2
import numpy as np
from PIL import Image

def cut_movie(path):
    """ 動画をフレームごとにわけて配列に格納する """

    # ビデオ読み込み
    cap = cv2.VideoCapture(path)
    W=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    H=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    count=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print("高さ：{} 幅：{} 全フレーム数:{}".format(W,H,count))
    pictures = []

    while True:
        # 1フレーム分読み込み
        ret, frame = cap.read()

        if ret:
            # BGR -> RGB
            frame = frame[:, :, [2, 1, 0]]
            # 1フレームずつappend
            pictures.append(frame)

        else:
            break

    pictures = np.array(pictures)
    print(pictures.shape)
    return pictures

if __name__ == '__main__':

    # 動画を画像に分解
    pictures = cut_movie("movie/target.mp4")
    # 欲しいフレームを選択して保存
    idx= np.random.choice(len(pictures),5)
    print(idx)
    pictures=[pictures[idx[i]] for i in range(len(idx))]
    for i, pic in enumerate(pictures):
        im = Image.fromarray(pic)
        im.save('movie/'+str(i)+'.jpg')