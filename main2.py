import numpy as np
from factorization import factorization
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn

if __name__ == '__main__':
    # getpoint.pyにより取り出した対応点を読み込み
    uv_mat = np.load("movie/uv_mat.npy")
    D = uv_mat.T

    print(D.shape)

    A, X = factorization(D)

    print(A)
    print(X)

    x, y, z = X

    #グラフの枠を作っていく
    fig = plt.figure()
    ax = Axes3D(fig)

    #軸にラベルを付けたいときは書く
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # プロット
    ax.plot(x,y,z,marker="o",linestyle='None',color="green")

    # 軸を等間隔にする処理
    max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max() * 0.5
    mid_x = (x.max()+x.min()) * 0.5
    mid_y = (y.max()+y.min()) * 0.5
    mid_z = (z.max()+z.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.show()