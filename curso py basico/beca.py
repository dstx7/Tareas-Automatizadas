distancia = int(input("Ingrese la distancia a la cual vive en km: "))
num_herm = int(input("numero de hermanos: "))
ingre_fam = int(input("ingresos familiares en euros: "))

if distancia > 40 and num_herm >2 or ingre_fam <= 20000:
    print("aplica para beca")
else:
    print("no aplica beca")