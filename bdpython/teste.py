import adivertencia 

cnn = adivertencia.conectar("bdpython/advertencia.db")
adivertencia.atualizar_user(cnn, 11, 9, 6353)
id_consultado = 9
consultar = adivertencia.consultar_user(cnn, id_consultado)
quantidade = 0
motivo = []
for qtd in consultar:
    quantidade +=1
    motivo.append(qtd[2])
print(quantidade)
print(f"numero da advertencia {quantidade}, id do aluno {id_consultado}, motivo {motivo}")
