import mysql.connector
import Variables
def conecta():
    return mysql.connector.connect(
        host=Variables.host,
        port=Variables.port,
        user=Variables.user,
        password=Variables.password,
        database=Variables.database
    )


def delete_duplicate(conexao, data):
    cursor = conexao.cursor()
    try:
        data_str = data.strftime("%Y-%m-%d")
        sql1 = "DELETE FROM venda_clientes WHERE data = %s"
        sql2 = "DELETE FROM venda_dia WHERE data = %s"
        cursor.execute(sql1, (data_str,))
        cursor.execute(sql2, (data_str,))
        conexao.commit()
        return True
    except mysql.connector.Error as error:
        print(f"Erro ao deletar duplicatas: {error}")
        return False
    finally:
        cursor.close()

def insere_venda(conexao,venda,data):
    query = "INSERT INTO venda_clientes(idloja, data, clientes, ticket_med, bruta, markup) VALUES (%s,%s,%s,%s,%s,%s)"
    dados = (venda['nome'].split('-')[0].strip(),data,venda['quantidade'],venda['ticketMedio'],venda['venda'],venda['margemMarkup'])
    cursor = conexao.cursor()
    cursor.execute(query, dados)
    conexao.commit()
    cursor.close()


def insere_produto(conexao, venda, dia_anterior, i):
    query = "INSERT INTO venda_dia(codloja, data, codprod, qtde, tktmed, venda, part, mkp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    dados = (i,dia_anterior,int(venda['nome'].split("(")[-1].replace(")","")),format(float(venda["quantidade"]), '.2f'),format(float(venda["ticketMedio"]), '.2f'),format(float(venda["venda"]), '.2f'),format(float(venda["participacao"]), '.2f'), format(float(venda["margemMarkup"]), '.2f'))
    cursor = conexao.cursor()
    cursor.execute(query, dados)
    conexao.commit()
    cursor.close()
    cursor.close()