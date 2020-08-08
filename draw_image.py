import cv2
import numpy as np
import matplotlib.pyplot as plt


def draw_lines(img1, img2, lines, pts1, pts2):
    ''' img1 - img2上の点に対応するエピポーラ線を描画する画像
        lines - 対応するエピポーラ線 '''
    r, c,_ = img1.shape
    #img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    #img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2] / r[1]])
        x1, y1 = map(int, [c, -(r[2] + r[0] * c) / r[1]])
        img1 = cv2.line(img1, (x0, y0), (x1, y1), color, 1)
        img1 = cv2.circle(img1, tuple(pt1), 5, color, -1)
        img2 = cv2.circle(img2, tuple(pt2), 5, color, -1)
    return img1, img2

def draw_lines_show(img1,img2,uvmat,F):

    # 右画像(二番目の画像)中の点に対応するエピポーラ線の計算
    # 計算したエピポーラ線を左画像に描画
    pts1 = np.array([[i[0], i[1]] for i in uvmat])

    pts2 = np.array([[i[2], i[3]] for i in uvmat])
    lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
    lines1 = lines1.reshape(-1, 3)
    img5, img6 = draw_lines(img1, img2, lines1, pts1, pts2)

    # 左画像(一番目の画像)中の点に対応するエピポーラ線の計算
    # 計算したエピポーラ線を右画像に描画
    lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
    lines2 = lines2.reshape(-1, 3)
    img3, img4 = draw_lines(img2, img1, lines2, pts2, pts1)

    # 結果の表示
    #plt.subplot(121), plt.imshow(img5)
    #plt.subplot(122), plt.imshow(img3)
    #plt.savefig("epipolar.jpg")
    plt.imshow(img5)
    plt.savefig("epipolar_img1.jpg")
    plt.imshow(img3)
    plt.savefig("epipolar_img2.jpg")