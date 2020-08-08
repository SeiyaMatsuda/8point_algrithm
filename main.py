import numpy as np
import numpy.linalg as LA
import sympy as sy
import os
from PIL import Image
import cv2
#from pointget import mouseParam,get_point
from calc_Fmatrix import calc_Fmatrix, calc_epipole,calc_Fmatrix_by5points
from draw_image import draw_lines,draw_lines_show
from calc_camera_matrix import calc_inside_param
if __name__ == '__main__':
    #### 本当にしたい処理: 画像からFを求め、f, cを算出 ####

    width = 750
    height = 750
    #img,uvmat=get_point()
    img=[]
    file=["small_depth1.jpg","small_depth2.jpg"
                             ""]
    for f in file:
        #入力画像
        path=os.path.join(r'C:\Users\yaase\Desktop\eizou', f)
        read = cv2.imread(path)
        img.append(read)
    uvmat = [(501, 368, 322, 388), (707, 252, 641, 306), (368, 226, 241, 232), (597, 144, 543, 180), (86, 143, 91, 135),
             (296, 95, 303, 111), (312, 356, 170, 341), (51, 223, 52, 201)]
    img1,img2=img[0],img[1]
    #img1[:,:,0],img1[:,:,1]=img1[:,:,1],img1[:,:,0]
    #img2[:,:,0],img2[:,:,1]=img2[:,:,1],img2[:,:,0]
    uvmat=np.array(uvmat)
    mat=np.zeros((8,9))
    # 正解の中心座標ans_cを出しておく

    ans_c_v1, ans_c_u1, _ = np.array(img1.shape) / 2
    ans_c_v2, ans_c_u2, _ = np.array(img2.shape) / 2

    print(ans_c_u1, ans_c_v1, ans_c_u2, ans_c_v2)

    # Fを算出
    F = calc_Fmatrix(uvmat)

    # 2枚の画像にエピポーラ線を描画

    #draw_lines_show(img1, img2, uvmat, F)
    # エピポールe1を算出
    e1 = calc_epipole(F.T)
    print("e1: {}".format(e1))
    a = input()

    # 内部パラメータを算出
    ans = calc_inside_param(F, e1, ans_c_u1, ans_c_v1, ans_c_u2, ans_c_v2, calc_phase="f")
    #calc_inside_param(F, e1, f1, f2, ans_c_u2, ans_c_v2, calc_phase="c1")
    #calc_inside_param(F, e1, f1, f2, ans_c_u1, ans_c_v1, calc_phase="c2")

    #####################################################

    #### カメラ行列A1, A2から作ってFを算出し、f1=2.3, f2=3.4が一致するかテスト ####

    A1 = np.array([[2.3, 0, 0], [0, 2.3, 0], [0, 0, 1]])
    A2 = np.array([[3.4, 0, 0], [0, 3.4, 0], [0, 0, 1]])
    r1, r2, r3 = 0.1, 0.2, 0.1
    rot_x = np.array([[1, 0, 0], [0, np.cos(r1), -np.sin(r1)], [0, np.sin(r1), np.cos(r1)]])
    rot_y = np.array([[np.cos(r2), 0, np.sin(r2)], [0, 1, 0], [-np.sin(r2), 0, np.cos(r2)]])
    rot_z = np.array([[np.cos(r3), -np.sin(r3), 0], [np.sin(r3), np.cos(r3), 0], [0, 0, 1]])
    R = np.dot(np.dot(rot_x, rot_y), rot_z)
    T = np.array([0.5, 0.05, 0.03])
    r1, r2, r3 = R.T

    f1, f2 = 923.620025369579, 941.677220030127
    c1 = [480, 853]
    c2 = [480, 853]
    A1 = np.array([[f1, 0, c1[0]],
                   [0, f1, c1[1]],
                   [0, 0, 1]])
    A2 = np.array([[f2, 0, c2[0]],
                   [0, f2, c2[1]],
                   [0, 0, 1]])

    # 5pointアルゴリズムによりFを算出
    F = calc_Fmatrix_by5points(uvmat, A1, A2)
    print("F行列:{}".format(F))
    print("ランク:{}".format(np.linalg.matrix_rank(F,tol=None)))
    # エピポーラ線を描画
    draw_lines_show(img[0],img[1],uvmat,F)

