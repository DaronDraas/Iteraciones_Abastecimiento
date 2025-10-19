import pandas as pd
import numpy as np
 
# === 1. Ruta del archivo === 
ruta = r""
# === 2. Cargar archivo Excel === 
df = pd.read_excel(ruta)
# === 3. Mostrar columnas reales (para debug) ===
print("Columnas encontradas")
for col in df.columns:
    print(f"[{col}]")
# === 4. Nombres de columnas ===
col_id = "ID"
col_venta = "% venta" # porcentaje de venta dentro del ID
col_tienda = "Código ERP"
col_producto = "Código producto"
col_capacidad = "CantidadCubicaciónReal"
col_jimena = "JimenaSum"

# === 5. Limpieza: convertir a numéricos ===
for col in [col_venta, col_capacidad, col_jimena]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# === 6. Calcular capacidad total por Tienda ===
# Sumamos todas las cubicaciones por tienda para no perder SKUs con misma cubicación
df_capacidad_tienda = df.groupby(col_tienda, as_index=False)[col_capacidad].sum()
print(df_capacidad_tienda[df_capacidad_tienda[col_tienda] == "Tienda 1"])

# === 7. Unir capacidades y Jimena por ID ===
# Sumamos Jimena por tienda
df_jimena_tienda = df.groupby(col_tienda, as_index=False)[col_jimena].sum()
df_tienda = pd.merge(df_capacidad_tienda, df_jimena_tienda, on=col_tienda, how="left")
df_tienda["capacidad_disponible"] = (df_tienda[col_capacidad] - df_tienda[col_jimena]).clip(lower=0)

# === X. Reemplazar NaN en % venta por reparto uniforme dentro del ID ===
# 1.1: Contar cuántos SKUs hay por ID
conteo_skus_por_id = df.groupby(col_id)[col_id].transform("count")

# 1.2. Rellenar NaN en % venta con 1 / cantidad de SKUs
df[col_venta] = df[col_venta].fillna(1 / conteo_skus_por_id)

# === 8. Merge con SKUs para asignar proporcionalmente ===
df = pd.merge(df, df_tienda[[col_tienda, "capacidad_disponible"]], on=col_tienda, how="left")
df["capacidad_asignada"] = df["capacidad_disponible"] * df[col_venta]

# === 9. Limpiar: quitar negativos y ceros ===
df["capacidad_asignada"] = df["capacidad_asignada"].clip(lower=0)
df = df[df["capacidad_asignada"] > 0]

# === 10. Exportar resultado ===
# modificar esta ruta para exportar el archivo cada vez que se itere
salida = r""
df.to_excel(salida, index=False)
print(f"\n✅ Archivo exportado con reparto proporcional por SKU a: {salida}")