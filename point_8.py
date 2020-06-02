# -*- coding: utf-8 -*-
"""
Created on Thu May 28 18:17:45 2020

@author: yaase
"""
# F行列を求める過程
import pointget as pg
import numpy as np
import numpy.linalg as LA

width = 768
height = 432

uvmat = np.array([(329, 280, 508, 289), (457, 209, 548, 166), (289, 188, 452, 205), (438, 146, 521, 103), (272, 134, 332, 156), (385, 111, 405, 83), (249, 279, 433, 328), (208, 196, 313, 257)])

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
print(V.shape)
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

print("Fの固有値=", value)

# F = value.reshape((3, 3))
# F = []
# values = []
# for i in range(9):
#     F.append(vec[i].reshape((3, 3)))
#     values.append(value[i])
# print(F)

# F = vec[8].reshape((3, 3))
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

