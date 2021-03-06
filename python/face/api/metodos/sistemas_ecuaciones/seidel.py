import numpy as np

from ..numeric_method import NumericMethod
from .matrix_utils import process_params, ceros_en_diagonal, radio_espectral


class Seidel(NumericMethod):
    def calculate(self, parameters):
        A = parameters["A"]
        b = parameters["b"]
        x0 = parameters["x0"]
        tol = parameters["tole"]
        iteraciones = parameters["niter"]

        A, b, x0 = process_params(A, b, x0)
        b = b[0]
        tol = eval(tol)
        iteraciones = int(iteraciones)

        response = self.init_response()

        if ceros_en_diagonal(A):
            response["error"] = "La matriz contiene ceros en la diagonal"
            return response

        contador = 0
        dispersion = tol + 1

        T, C = self.hallar_T_C(A, b)

        if radio_espectral(T) >= 1:
            response["error"] = "El radio espectral de la matriz T es mayor  1, reorganice la matriz"
            return response

        while dispersion > tol and contador < iteraciones:
            x1 = np.matmul(T, x0) + C

            disp_fmt = "{e:.2e}".format(e=dispersion) if contador != 0 else ""
            iteracion = [contador, x0.tolist(), disp_fmt]
            response["iteraciones"].append(iteracion)

            dispersion = np.linalg.norm(x1 - x0, 2)
            x0 = x1.copy()
            contador = contador + 1

        disp_fmt = "{e:.2e}".format(e=dispersion) if contador != 0 else ""
        iteracion = [contador, x0.tolist(), disp_fmt]
        response["iteraciones"].append(iteracion)

        if dispersion < tol:
            response["aproximados"].append(x1.tolist())
            # print(x1, "es una aproximación inicial con una toleracia de {}".format(tol))
        else:
            response["error"] = "El algoritmo fracasó despues de {} \
                iteraciones".format(iteraciones)
            # print("El método fracasó en {} iteraciones".format(iteraciones))

        return response

    def hallar_T_C(self, A, b):
        D = np.diag(np.diag(A))
        U = -1 * (np.triu(A) - D)
        L = -1 * (np.tril(A) - D)

        D_L_inv = np.linalg.inv(D-L)
        T = np.matmul(D_L_inv, U)
        C = np.matmul(D_L_inv, b)

        return T, C

    def error(self, x):
        return np.amax(np.absolute(x))

    def get_description(self):
        return "Metodo iterativo Jacobi"

    def init_response(self):
        response = dict()
        response["iteraciones"] = []
        response["aproximados"] = []

        return response
