from sympy import symbols
from .utils import sympify_expr


def regla_falsa(parameters):
    # Se crean las variables
    response = init_response()
    x = symbols("x")

    # Extracción de los parametros
    f = str(parameters["funcion"])
    xa = float(parameters["xa"])
    xb = float(parameters["xb"])
    n_iter = int(parameters["n_iter"])
    tol = eval(parameters["tol"])

    # Transformar f a sympy
    f = sympify_expr(f)
    response["funcion_in"] = str(f)

    fxa = f.evalf(subs={x: xa})
    fxb = f.evalf(subs={x: xb})

    if abs(fxa) == 0:
        response["raices"].append(xa)
        # print(xa, "es raíz")

    if abs(fxb) == 0:
        response["raices"].append(xb)
        # print(xb, "es raíz")

    if fxa * fxb > 0:
        # print("El intervalo es inadecuado")
        response["error"] = "El intervalo es inadecuado"
        return response

    xm = xa - ((fxa*(xb-xa))/(fxb - fxa))  # Ecuación 15, regla falsa
    fxm = f.evalf(subs={x: xm})
    contador = 1
    error = tol + 1

    while error > tol and fxm != 0 and contador < n_iter:
        iteracion = [contador, str(xa), str(xb), str(xm), str(fxm), str(error)]
        response["iteraciones"].append(iteracion)

        if fxa * fxm < 0:
            xb = xm
            fxb = fxm
        elif fxm * fxb < 0:
            xa = xm
            fxa = fxm
        else:
            # print("error")
            response["error"] = "Se ha encontrado un error, intente de nuevo"

        x_ant = xm
        xm = (xa+xb)/2
        fxm = f.evalf(subs={x: xm})
        error = abs(xm - x_ant)
        contador = contador + 1

    iteracion = [contador, str(xa), str(xb), str(xm), str(fxm), str(error)]
    response["iteraciones"].append(iteracion)

    if fxm == 0:
        response["raices"].append(str(xm))
        # print(xm, "es raiz")

    elif error < tol:
        response["aproximados"].append(str(xm))
        # print(xm, "es aproximación a una raíz con una tolerancia =", tol)

    else:
        response["error"] = "El algoritmo fracasó despues de {} iteraciones".\
            format(n_iter)
        # print("Algoritmo fracasó despues de {} iteraciones".format(n_iter))
    return response


def descripcion_regla_falsa():
    return "Este metodo se encarga de encontrar una raíz dado un rango donde \
        haya un cambio de signo, aplicando el metodo de regla falsa"


def init_response():
    response = dict()
    response["raices"] = []
    response["iteraciones"] = []
    response["aproximados"] = []
    # response["error"] = ""

    return response
