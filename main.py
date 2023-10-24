import pandas as pd
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus, value, LpBinary

# Cargar los datos desde el archivo "features.csv"
data = pd.read_csv("C:/Users/USUARIO/Downloads/features.csv")  # Reemplaza la ruta con la correcta

# Crear un problema de programación lineal
prob = LpProblem("Optimizacion_Cadena_Suministro", LpMaximize)

# Variables de decisión: Asignación de tiendas
stores = data["Store"].unique()
x = LpVariable.dicts("Asignacion", stores, 0, 1, LpBinary)

# Función objetivo: Maximizar el beneficio total (usando MarkDown1 y MarkDown2 como beneficio)
beneficio_markdown1 = {}
beneficio_markdown2 = {}
costo_de_transporte = {}

for store in stores:
    beneficio_markdown1[store] = data.loc[data["Store"] == store, "MarkDown1"].sum()
    beneficio_markdown2[store] = data.loc[data["Store"] == store, "MarkDown2"].sum()
    costo_de_transporte[store] = data.loc[data["Store"] == store, "Fuel_Price"].sum()

prob += lpSum((beneficio_markdown1[store] + beneficio_markdown2[store] - costo_de_transporte[store]) * x[store] for store in stores)

# Restricción: Cada tienda debe recibir al menos un producto
for store in stores:
    prob += x[store] >= 1

# Resolvemos el problema
prob.solve()

# Mostrar resultados
print("Estado:", LpStatus[prob.status])
for store in stores:
    if x[store].varValue == 1:
        print(f"Tienda {store} asignada")

# Valor de la función objetivo (beneficio total)
print("Beneficio total:", value(prob.objective))
