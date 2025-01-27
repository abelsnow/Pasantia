class Parabola:#clase parabola que recibe 3 argumentos
    def __init__(self, a, b, c):
        self.a =float( a)#lo pongo de tipo float porque no siempre son enteros
        self.b = float(b)
        self.c = float(c)

    #funcion que calcula el foco
    def calcular_foco(self):
        x_foco = -self.b / (2 * self.a)
        y_foco = (4 * self.a * self.c - self.b**2) / (4 * self.a)#dicha formula matematica sirve para ambos casos  (verticales u horinzontales)
        return x_foco, y_foco

#clase recta 
class Recta:
    def __init__(self, ecuacion):#recibe una ecuacion
        self.ecuacion = ecuacion
        self.a, self.b, self.c = self.extraerComponentes()

    def extraerComponentes(self):
        partes = self.ecuacion.split()#split separa la cadena en partes segun el argumento ingresado
        a, b, c = 0.0, 0.0, 0.0#al no tener argumentos separa segun espacios en blanco
        for i in range(len(partes)):#ejeplo en 3x2 + 2y el elemento[0] es 3x2
            if "X" in partes[i]:#por eso pregunta si dicho elemento se encuentra dentro 
                a_str = partes[i].replace("X", "")#replaza la letra por un espacio en blanco
                if a_str == "":#en caso de que sea solamente x entonces le pondra valor 1.0
                    a = 1.0
                elif a_str == "-":#si tiene un signo - multiplicara por menos 1
                    a = -1.0
                else:
                    a = float(a_str)#convierte a float
            elif "Y" in partes[i]:
                b_str = partes[i].replace("Y", "")
                if b_str == "":
                    b = 1.0
                elif b_str == "-":#lo mismo pasa aca
                    b = -1.0
                else:
                    b = float(b_str)
            elif "=" in partes[i]:#practicamente lo mismo
                c = float(partes[i - 1])
        return a, b, c

# Ingresar la ecuación por teclado
ecuacion = input("Ingrese la ecuación: ")

# Crear una instancia de la clase Recta
recta = Recta(ecuacion)

# Creo un objeto parabola que recibe como argumentos los valores a,b y c de la recta
parabola = Parabola(recta.a, recta.b, recta.c)

# una impresion dde verificacion
print(f"A = {recta.a}")
print(f"B = {recta.b}")
print(f"C = {recta.c}")

# Calcula y muestra las coordenadas del foco
foco = parabola.calcular_foco()
print("Las coordenadas del foco son:", foco)




