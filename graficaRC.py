
# Authors: 
# Laurie Camila Hernández Pacheco A01286569
# Emilio Alejandro González Huerta A01286440
# Fernando Álvarez Ruiz A01286754
# Ángel Darío Marroquín Escobedo A01286669

# Código para los gráficos RC del RETO: Gota de Millikan

import numpy as np
import matplotlib.pyplot as plt

# Parámetros del circuito
fem = 5300         # Voltaje de la fuente de alimentación (en volts)
R = 1e6            # Resistencia en el circuito (en ohms)
C = 1.107e-9       # Capacitancia del capacitor (en faradios)
s = 16e-3          # Distancia entre las placas del capacitor (en metros)
RC = R * C         # Constante de tiempo del circuito RC (en segundos)

# Generación del vector de tiempo, t, de 0 a 1 segundo con 3500 puntos
t = np.linspace(0, 1, 3500)

# Cálculo del voltaje en el capacitor (Ecuación 57) usando la fórmula V(t) = Vmax * (1 - exp(-t / (R * C)))
Vc = fem * (1 - np.exp(-t / RC))

# Gráfico del voltaje en el capacitor con respecto al tiempo
line1, = plt.plot(t, Vc, color='#8ab2f2', label="Voltaje del capacitor")  # Curva Vc(t) en azul claro
line2 = plt.axhline(y=5300, color='#7aa7f0', linestyle=':', linewidth=1.5, label="V máx (5300 V)")  # Línea horizontal del voltaje máximo
plt.legend()  # Mostrar leyenda
plt.xlim([0, 0.008])  # Limitar el eje X a un rango de 0 a 0.008 segundos
plt.ylim([0, 5500])  # Limitar el eje Y a un rango de 0 a 5500 V
plt.xlabel("Tiempo (s)")  # Etiqueta del eje X
plt.ylabel("Voltaje del capacitor (V) con respecto al tiempo")  # Etiqueta del eje Y
plt.title("Carga de un capacitor en un circuito RC")  # Título del gráfico
plt.grid(True)  # Activar la cuadrícula en el gráfico
plt.show()  # Mostrar el gráfico

# Cálculo del campo eléctrico entre las placas del capacitor (Ecuación 58)
Et = (fem / s) * (1 - np.exp(-t / RC))  # Fórmula del campo eléctrico E(t)
E_max = fem / s  # Valor máximo del campo eléctrico

# Gráfico del campo eléctrico con respecto al tiempo
line3, = plt.plot(t, Et, color='#a5f2dc', label="E(t)")  # Curva del campo eléctrico en verde claro
line4 = plt.axhline(y=E_max, color='#7cebcb', linestyle=':', linewidth=1.5, label=f"E max ({E_max} N/C)")  # Línea horizontal del campo máximo
plt.legend()  # Mostrar leyenda
plt.xlim([0, 0.006])  # Limitar el eje X a un rango de 0 a 0.006 segundos
plt.ylim([0, 350000])  # Limitar el eje Y a un rango de 0 a 350,000 N/C
plt.xlabel("Tiempo (s)")  # Etiqueta del eje X
plt.ylabel("E(t)")  # Etiqueta del eje Y
plt.title("Campo eléctrico con respecto al tiempo")  # Título del gráfico
plt.grid()  # Activar la cuadrícula en el gráfico
plt.show()  # Mostrar el gráfico

# Importar herramientas 3D para graficar la carga del capacitor en diferentes posiciones
from mpl_toolkits.mplot3d import Axes3D

# Generación del vector de tiempo, t, de 0 a 0.005 segundos con 1000 puntos
t = np.linspace(0, 0.005, 1000)

# Definir varias posiciones x en metros (distancia entre las placas)
x_vals = [1e-3, 2e-3, 4e-3, 8e-3, 12e-3, 16e-3]
legends = ["1 mm", "2 mm", "4 mm", "8 mm", "12 mm", "16 mm"]  # Leyendas para cada posición

# Crear la figura 3D
fig = plt.figure(figsize=(10, 7))  # Tamaño de la figura
ax = fig.add_subplot(111, projection='3d')  # Crear el eje 3D
colors = ["#eba39b", "#f1f28f", "#9bf28f", "#8fc4f2", "#c79beb", "#eb9bd6"]  # Colores para las curvas

# Graficar el voltaje del capacitor para cada posición x a lo largo del tiempo
for i, x_val in enumerate(x_vals):
    t_plot = t  # Usar el mismo vector de tiempo
    x_plot = np.full_like(t_plot, x_val)  # Mantener la posición x constante para cada curva
    z_plot = fem * (x_val / s) * (1 - np.exp(-t_plot / RC))  # Cálculo del voltaje en función de x y t
    ax.plot(x_plot, t_plot, z_plot, label=legends[i], color=colors[i])  # Graficar cada curva con su respectivo color y leyenda

# Etiquetas y leyenda para el gráfico 3D
ax.set_ylim([0, 0.005])  # Limitar el eje Y (tiempo) a 0 a 0.005 segundos
ax.set_xlabel('x (m)')  # Etiqueta del eje X (distancia entre placas)
ax.set_ylabel('t (s)')  # Etiqueta del eje Y (tiempo)
ax.set_zlabel('Vc(x,t) (V)')  # Etiqueta del eje Z (voltaje)
ax.set_title('Carga del capacitor a diferentes posiciones x')  # Título del gráfico 3D
ax.legend()  # Mostrar la leyenda
plt.tight_layout()  # Ajustar el diseño del gráfico para que todo quede visible
plt.show()  # Mostrar el gráfico


