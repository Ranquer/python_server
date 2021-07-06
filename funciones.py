from petl import *

tabla1 = fromcsv("./uploads/heart.csv")
print(tabla1)

tabla2 = convert(tabla1, "cp", int)
tabla3 = convert(tabla2, "oldpeak", float)
tabla4 = convert(tabla3, 'opc', 'upper')

tojson(tabla4, "archivo.json")