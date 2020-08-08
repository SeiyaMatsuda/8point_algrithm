# -*- coding: utf-8 -*-
"""
Created on Thu May 28 18:17:45 2020

@author: yaase
"""
# F行列を求める過程
import numpy as np
import numpy.linalg as LA
import cv2
def calc_Fmatrix(uvmat):
    mat = np.zeros((8, 9))
    for i in range(8):
          mat[i, 0] = uvmat[i, 0] * uvmat[i, 2]
          mat[i, 1] = uvmat[i, 1] * uvmat[i, 2]
          mat[i, 2] = uvmat[i, 2]
          mat[i, 3] = uvmat[i, 0] * uvmat[i, 3]
          mat[i, 4] = uvmat[i, 1] * uvmat[i, 3]
          mat[i, 5] = uvmat[i, 3]
          mat[i, 6] = uvmat[i, 0]
          mat[i, 7] = uvmat[i, 1]
          mat[i, 8] = 1.0

    # mattmat = np.dot(mat.T, mat)
    # value, vec = LA.eig(mattmat)

    # matを特異値分解
    U, D, V = LA.svd(mat)
    # 最小の固有値を探す
    print("D=", D)
    print("V=", V)
    print(V[8])
    # Vから固有値最小の固有ベクトルを取り出してFにする
    F = V[8].reshape((3, 3))
    print("F=", F)

    ### 以下の処理はコメントにしても大丈夫、あると精度がよくなる
    # Fのランクを2にする
    '''
    U, D, V = LA.svd(F)
    F = np.dot(U, np.diag([D[0], D[1], 0]))
    F = np.dot(F, V.T)
    print("F'=",F)
    print("F_rank=",LA.matrix_rank(F))
    ### おわり
    
    # Nにより正規化
    N = np.array([[2/width, 0, -1],
                [0, 2/height, -1],
                [0, 0, 1]])
    F = np.dot(N.T, F)
    F = np.dot(F, N)
    print(F)
    '''
    # Fの固有値は[1,0,0]になる
    value, vec = LA.eig(F)
    rank=np.linalg.matrix_rank(F)
    print("Fの固有値=", value)
    print("Fのrank=", rank)

    for i in range(8):
      # x1 = [u1, u2, 1], x2 = [u2, v2, 1]
      x1 = np.array([uvmat[i, 0], uvmat[i, 1], 1.0])
      x2 = np.array([uvmat[i, 2], uvmat[i, 3], 1.0])

      # Nにより正規化
      '''
      x1 = np.dot(N, x1.T)
      x2 = np.dot(N, x2.T)
      '''
      # x2^T * F * x1 = 0 のチェック
      a = np.dot(x2.T, F)
      print(np.dot(a, x1))
    return F
def calc_epipole(F):
    # F^Tを特異値分解
    U, D, V = LA.svd(F)
    # Vから固有値最小の固有ベクトルを取り出す
    fvec = V[2]

    # こっちだとやっぱりできない
    # value, vec = LA.eig(np.dot(F, F.T))
    # fvec = vec[2]
    # print(fvec / fvec[2])

    return fvec / fvec[2]
def calc_Fmatrix_by5points(uvmat, A1, A2):
    x1 = uvmat[:, :2].astype('float32')
    x2 = uvmat[:, 2:4].astype('float32')
    print(A1.shape)
    x1_norm = cv2.undistortPoints(np.expand_dims(x1, axis=1), cameraMatrix=A1, distCoeffs=None)
    x2_norm = cv2.undistortPoints(np.expand_dims(x2, axis=1), cameraMatrix=A2, distCoeffs=None)
    # print(x1_norm.shape)
    # x1_norm = x1.reshape(5, 2)
    # x2_norm = x2.reshape(5, 2)
    E, mask = cv2.findEssentialMat(x1_norm, x2_norm, focal=1, pp=(480, 853), method=cv2.RANSAC, prob=0.999, threshold=3.0)
    # E, mask = cv2.findEssentialMat(x1, x2, cameraMatrix=A1, #focal=1.0, pp=(0., 0.),
    #                                 method=cv2.RANSAC, prob=0.999, threshold=3.0
    #                                 )
    print(E.shape, mask)
    print(E)
    A1_inv = LA.inv(A1)
    A2_inv = LA.inv(A2)
    F = np.multiply(A1_inv.T, E, A2_inv)
    return F
