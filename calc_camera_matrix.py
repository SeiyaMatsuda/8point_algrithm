import sympy as sy
import numpy as np


def calc_inside_param(F, e, p11, p12, p21, p22, calc_phase="f"):
    """
    F行列と画像のエピポールeからkruppa方程式よりカメラ内部パラメータ行列Aを算出する
    ただし内部パラメータの未知の変数は2個という制限があるため、
    A1 = [[f_u1,  0, c_u1],
          [0,  f_v1, c_v1],
          [0,     0,    1]]
    A2 = [[f_u2,  0, c_u2],
          [0,  f_v2, c_v2],
          [0,     0,    1]]
    のf, cのうち2つしか変数にすることができず、その他の6つの値は埋める必要がある
    今回、f_u1 = f_v1 = f1, f_u2 = f_v2 = f2と仮定して
    与える値を(p11, p12, p21, p22)の4つとしている
    <calc_phase>
    f: f1, f2を求める
    c1: c_u1, c_v1を求める
    c2: c_u2, c_v2を求める
    """

    # a1, a2を求める
    sy.var('a1, a2')

    if calc_phase == "f":

        A1 = sy.Matrix([[a1, 0, p11],
                        [0, a1, p12],
                        [0, 0, 1]])

        A2 = sy.Matrix([[a2, 0, p21],
                        [0, a2, p22],
                        [0, 0, 1]])

    elif calc_phase == "c1":
        A1 = sy.Matrix([[p11, 0, a1],
                        [0, p11, a2],
                        [0, 0, 1]])

        A2 = sy.Matrix([[p12, 0, p21],
                        [0, p12, p22],
                        [0, 0, 1]])

    elif calc_phase == "c2":
        A1 = sy.Matrix([[p11, 0, p21],
                        [0, p11, p22],
                        [0, 0, 1]])

        A2 = sy.Matrix([[p12, 0, a1],
                        [0, p12, a2],
                        [0, 0, 1]])

    # t
    sy.var('t')
    vec_t = sy.Matrix([1, t, 0])

    # e, Fをsympyに変換
    e = sy.Matrix([e[0], e[1], e[2]])
    F = sy.Matrix([[F[0, 0], F[0, 1], F[0, 2]],
                   [F[1, 0], F[1, 1], F[1, 2]],
                   [F[2, 0], F[2, 1], F[2, 2]]])

    # eq1 = (e × t)^T * A1 * A1^T * (e1 × t) = 0
    tmp1 = A1.transpose() * e.cross(vec_t)
    eq1 = sy.expand((tmp1.transpose() * tmp1)[0])

    # eq1からt^0, t^1, t^2の係数を取り出す
    k10 = eq1.coeff(t, 0)
    k11 = eq1.coeff(t, 1)
    k12 = eq1.coeff(t, 2)

    # eq2 = (F^T × t)^T * A2 * A2^T * (F^T × t) = 0
    tmp2 = A2.transpose() * F.transpose() * vec_t
    eq2 = sy.expand((tmp2.transpose() * tmp2)[0])

    # eq2からt^0, t^1, t^2の係数を取り出す
    k20 = eq2.coeff(t, 0)
    k21 = eq2.coeff(t, 1)
    k22 = eq2.coeff(t, 2)

    # expr1 = k10*k21 - k11*k20
    expr1 = sy.expand(k10 * k21 - k11 * k20)
    # expr2 = k11*k22 - k21*k12
    expr2 = sy.expand(k11 * k22 - k21 * k12)
    print("expr1 = {}".format(expr1))
    print("expr2 = {}".format(expr2))

    # expr1 = expr2 = 0を解く(解はa1, a2)
    ans = sy.solve([expr1, expr2], [a1, a2])
    print("(a1, a2)=\n{}".format(ans))

    return ans