def funcion_nota(nota):
    if nota > 5:
        return print( "Aprobado")
    else:
        return print ("reprobado")
    
nota = 5

while nota != 0:
    nota = int(input("ingrese el valor de la nota (o ingrese 0 para terminar): "))
    funcion_nota(nota)
