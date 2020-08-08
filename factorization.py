import numpy as np
import numpy.linalg as LA
import scipy.linalg


def factorization(D):
    # フレーム数*2, 特徴点の数
    frame_2n, point_n = D.shape

    # 各フレームでの特徴点の重心ベクトル
    G = np.mean(D, axis=1).reshape(frame_2n, 1)

    # D^ = D - G
    D_var = D - G
    print(D_var.shape)

    # D^を特異値分解する
    U, S, V = LA.svd(D_var)

    print(np.diag(S[:3]))
    print(U.shape, S.shape, V.shape)

    S_sqrt = scipy.linalg.sqrtm(np.diag(S[:3]))

    A = np.dot(U[:, :3], S_sqrt)
    X = np.dot(S_sqrt, V[:3, :])
    print(A.shape)
    print(X.shape)
    return A, X