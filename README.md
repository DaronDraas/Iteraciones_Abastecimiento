# Iteraciones_Abastecimiento
Different python codes to make my work easier

Para variación de duplicados en tienda & código
df_unicos = df.drop_duplicates(subset=["Tienda", "Código"])

# === 6. Calcular capacidad total por Tienda ===
# Eliminamos duplicados considerando la combinación Tienda + Código producto
df_capacidad_unica = df.drop_duplicates(subset=[col_tienda, col_producto])

# Sumamos todas las cubicaciones por tienda (ya sin duplicados por producto)
df_capacidad_tienda = df_capacidad_unica.groupby(col_tienda, as_index=False)[col_capacidad].sum()

print(df_capacidad_tienda[df_capacidad_tienda[col_tienda] == "Tienda 1"])

