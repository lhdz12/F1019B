
# Authors: 
# Laurie Camila Hernández Pacheco A01286569
# Emilio Alejandro González Huerta A01286440
# Fernando Álvarez Ruiz A01286754
# Ángel Darío Marroquín Escobedo A01286669

# Codigo de simulación para RETO: Simulación del Experimento de la Gota de Millikan


import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


# Valores planteados para los parámetros importantes del experimento
rho_g = 919.9      # kg/m³ (densidad del aceite)
vi = 0             # m/s (velocidad inicial de la gota)
r = 2.76e-6        # m (radio de la gota)
g = (9.81)          # m/s^2
q = 1.6e-19        # C
s= 16e-3           # m (distancia entre las placas)
phi = 5300        # V (voltaje aplicado)
rho_a = 1.2        # kg/m³ (densidad del aire)
eta = 1.8e-5       # Pa·s (viscosidad del aire)
rA = [2.76e-6]
rho_aA = [1.2]
etaA = [1.8e-5]
qA = [1.6e-19]

# Función para validar el ingreso de los datos: que sean valores numéricos
def validarDatos(x):
    x= input("Ingresar el valor deseado. Valor actual: " + str(x) + ": ")
    validData = False
    while(validData == False):
        if x.strip() != "":
            # Try / except: Ayuda a validar errores. Si no hay valor o valor numérico, pide el dato again hasta que funcione.
            try:
                x = float(x)
                print("Nuevo valor de la variable: " + str(x))
                validData = True
            except ValueError:
                print("\nValor inválido. Intente de nuevo.")
                x = input("Ingresar el valor deseado. Valor actual: " + str(x) + ": ")
    return x
# Función para ingresar los valores de estas variables para el cálculo de q
def ingresarValores(): 
    global rho_a, rho_g, vi, r,eta, s, phi, q
    print("Ingrese los valores para la simulación del experimento: \n")
    print("Densidad del aire (kg/m³):")
    rho_a = validarDatos(rho_a)
    print("Densidad de la gota de aceite (kg/m³):")
    rho_g = validarDatos(rho_g)
    print("Radio de la gota (m):")
    r = validarDatos(r)
    print("Viscosidad del aire (Pas):")
    eta = validarDatos(eta)
    print("Distancia entre las placas (m):")
    s = validarDatos(s)
    print("Voltaje inducido (V): ")
    phi = validarDatos(phi)
    print("Carga (C): ")
    q = validarDatos(q)

    # Imprime al final todas las variables
    print("\nNuevos valores para las variables: ")
    print("Densidad del aire: "+str(rho_a)+" kg/m³")
    print("Densidad de la gota: "+str(rho_g) + " kg/m³")
    print("Radio de la gota: " + str(r) + " m")
    print("Viscosidad del aire: "+ str(eta) + " Pas")
    print("Distancia entre las placas: " + str(s) + " m")
    print("Voltaje inducido: " + str(phi) + " V")

# Definimos las funciones caso1 y caso2 para las eq. diferenciales a tratar. 
# Modelo sin campo eléctrico
def caso1(t, y):
    v = y[0]  # Velocidad
    vol = (4/3) * np.pi * r**3 # Calculo de volumen con los valores ingresados
    m = rho_g * vol # Masa de la gota
    dvdt = g * (1 - (rho_a / rho_g)) - ((9 * eta) / (2 * rho_g * r*r)) * v # Diferencial CASO 1.1 (EL BUENO)
    dxdt = v #dx/dt es lo mismo que v(t)
    return [dvdt,dxdt]  # Nos regresa ambas dv/dt y dx/dt para resolver de una.
    # Se repite todo esto para el caso 2
# Modelo con campo eléctrico
def caso2(t, y):
    global rho_a, rho_g, vi, r,eta,q, phi, s
    v = y[0]  # Velocidad
    dvdt = (((3*q*phi)/(4*np.pi*rho_g*s*(r**3)))-g*(1-(rho_a/rho_g)))-(9*eta)/(2*rho_g*(r**2)) * v
    dxdt = v 
    return [dvdt,dxdt]

# El proceso de graficar y solucionar la diferencial
def resolucionYGraficas(): 
    global q, s, eta, phi, rho_g, rho_a, vi, r, g
    # Tiempo para visualizar sim.
    t = 5.5e-4

    # CASO 1 - Sin campo eléctrico
    t_span = (0, t) # Lapso de tiempo a graficar
    condicion_inicial = [vi,0]  # Velocidad inicial = 0, y Pos. inicial = 0
    t_eval = np.linspace(0, t, 500) # Separamos en espacios
    
    # Obtenemos la solución de la diferencial con solve_ivp
    # El Python resuelve para las variables vi & 0 respecetivamente lo que ocupan. Podemos decir que estamos resolviendo una diferencial 
    # en cada uno de los slots de dos vectores. Planteamos vectores y se resuelve en cada cuadrito jiji. 
    sol = solve_ivp(caso1, t_span, condicion_inicial, t_eval=t_eval)

    # Calculamos la V terminal teórica para poder graficarla 
    v_terminal1 = (2/9) * (rho_g - rho_a) * g * r**2 / eta

    # CASO 2 - Con campo eléctrico

    # A partir de aquí se repite lo de arriba
    sol2 = solve_ivp(caso2, t_span, condicion_inicial, t_eval=t_eval)

    v_terminal2 = (2*rho_g*r**2)/(9*eta) * ( (3*q*phi)/(4*np.pi*rho_g*s*r**3) - g*(1 - (rho_a/rho_g)))
    
    # Ahora graficamos todo
    plt.figure(figsize=(10, 6))

    # Recordamos que puedo ponerle colores personalizados a los gráficos y i'm just a girl entonces tocó 
    
    # CASO 1: SIN CAMPO ELÉCTRICO
    plt.plot(sol.t, sol.y[0], color='#ac5ad1', label="Sin campo eléctrico") # El índice [0] indica que estamos con dv/dt
    plt.axhline(y=v_terminal1, color='#c589e0', linestyle=':', linewidth=1.5, label=f'$v_{{t1}}$ = {v_terminal1:.2e} m/s')

    # CASO 2: CON CAMPO ELÉCTRICO
    plt.plot(sol2.t, sol2.y[0], color = '#f562dc', label="Con campo eléctrico")
    plt.axhline(y=v_terminal2, color='#f78fe6', linestyle=':', linewidth=1.5, label=f'$v_{{t2}}$ = {v_terminal2:.2e} m/s')

    # Ahora sí las generalidades de la gráfica
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Velocidad (m/s)")
    plt.title("Comparación de velocidades terminales (Con/sin campo eléctrico)")
    plt.grid(True)
    plt.legend()
    plt.show()

    # Ahora las gráficas de la posición (por eso índice [1], porque dx/dt está en la posición 1 del valor de retorno de caso1 y caso2)
    plt.figure()
    plt.plot(sol.t, sol.y[1], color='#ac5ad1',label="Posición (sin campo eléctrico)")
    plt.plot(sol2.t,sol2.y[1], color = '#f562dc',label="Posición (con campo eléctrico)")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Posición (m)")
    plt.title("Posición de la gota en caída libre")
    plt.grid()
    plt.legend()
    plt.show()
    
    q_estimada2 = estimarCargaEuler(0,0.00001,t)
    print("La carga real para el caso 2 es:", q, "Coulombs")
    print(f"La carga estimada para el caso 2 es: {q_estimada2:.1e}Coulombs")
    error2 = abs(q-q_estimada2)/q * 100
    print(f"El error entre la carga parámetro y la carga experimental es: {error2:.2e}%")


    print("Gracias por correr la grafiquita :D")
# Aquí estimamos la carga mediante el método de euler
def estimarCargaEuler(v0, dt, T): # v0 = vel. inicial, dt = pasos, T = tiempo final
    global rho_a, rho_g, r, eta, g, phi, s
    # Condiciones iniciales
    v = v0
    t = 0
    x = 0

    while t < T:
        # Calcula dv/dt (SIN q)
        # Pero como no conocemos q, vamos a plantearlo como:
        # dv/dt = A - B*v
        # donde:
        A = (((3)/(4*np.pi*rho_g*s*r**3)) * q * phi) - g*(1 - (rho_a/rho_g))
        B = (9*eta)/(2*rho_g*r**2)

        dvdt = A - B*v
        
        # Actualiza velocidad y posición
        v = v + dvdt * dt
        x = x + v * dt
        t = t + dt

    # Ahora usamos que a velocidad final, dv/dt ≈ 0
    # Entonces despejamos q de:
    # 0 = ((3*q*phi)/(4πρg s r³)) - g(1-ρa/ρg) - (9η)/(2ρg r²) * vf
    # de donde:
    q_estimada = (4*np.pi*rho_g*s*r**3)/(3*phi) * ( g*(1 - (rho_a/rho_g)) + (9*eta/(2*rho_g*r**2))*v )

    return q_estimada

# Función main
def main(): 
    global rho_a, rho_g, vi, r,eta,q,g,phi,s

    menuOn = True

    # Abrimos un pequeño menú para opciones para el usuario
    while(menuOn):
        # Permitimos que el usuario ingrese valores
        print("\n---------------Simulación del experimento de la gota de Millikan---------------")
        print("Los valores ya registrados son los parámetros comunes, se muestran a continuación: ")
        print("\nDensidad del aire: "+str(rho_a)+" kg/m³")
        print("Densidad de la gota: "+str(rho_g) + " kg/m³")
        print("Radio de la gota: " + str(r) + " m")
        print("Viscosidad del aire: "+ str(eta) + " Pas")
        print("Velocidad de la gota: " + str(vi) + " m/s")
        print("Distancia entre las placas: " + str(s) + " m")
        print("Voltaje aplicado: " + str(phi) + " V")
        print("Carga: " + str(q) + " C")

        # Opciones del menú
        print("\nSeleccione alguna de las opciones")
        print("0) Dejar los valores iguales y correr la simulación")
        print("1) Cambiar todos los valores y correr la simulación")
        print("2) Regresar todos los valores a predeterminados y correr el programa")
        print("3) Cerrar el programa")
        option = input("Ingrese su elección (0, 1, 2, 3): ")

        # Validación
        while option not in ['0', '1', '2','3']:
            print("El valor ingresado no es válido. Intente nuevamente: ")
            print("0) Dejar los valores iguales")
            print("1) Cambiar todos los valores")
            print("2) Regresar todos los valores a predeterminados y correr el programa")
            print("3) Cerrar el programa")
            option = input("Ingrese su selección (0, 1, 2, 3): ")
        # Directamente grafica
        if option == '0': 
            resolucionYGraficas()
        # Permite al usuario cambiar valores
        if option == '1':
            ingresarValores()
            resolucionYGraficas()
        # Reinicia los valores y corre el programa
        if option == '2': 
            rho_g = 919.9      # kg/m³ (densidad del aceite)
            vi = 0             # m/s (velocidad inicial de la gota)
            r = 2.76e-6      # m (radio de la gota)
            g = 9.81           # m/s^2
            q = 1.6e-19        # C
            s= 16e-3           # m (distancia entre las placas)
            phi = 5300         # V (voltaje aplicado)
            rho_a = 1.2        # kg/m³ (densidad del aire)
            eta = 1.8e-5       # Pa·s (viscosidad del aire)
            resolucionYGraficas()
        # Cierra el programa cambiando el menuOn a falso.
        if option == '3': 
            print("¡Gracias por correr el programa! <3")
            menuOn = False
        
main()