Para los Precios, en el excel vienen en formato ancho, es decir, las columnas son cada activo, y tienen filas por cada fecha.
Pandas tiene una funcion pd.melt(), con melt lo paso a fromato largo para que tenga concordancia con la tabla en la base de datos (Precio: activo, fecha, valor)

