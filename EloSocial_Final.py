import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='02_elosocial'
)

cursor = conexao.cursor()


def menu_principal():
    print("""
### Bem Vindo ao Elo Social! ###
          
Selecione o Equipamento:
[1] RI (Residência Inclusiva)
[2] SAICA (Serviço de Acolhimento Institucional para Crianças e Adolescentes)
[3] CPA (Centro Provisório de Acolhimento)
[4] Controle de Medicação
[0] Sair""")
    while True:
        try:
            opcao = int(input("-> "))
            return opcao
        except ValueError:
            print("Opção inválida! Digite apenas números.")

def menu_medicacao():
    print("""\n### Medicação ###
O que deseja fazer?
[1] Listar
[2] Alterar
[3] Inserir
[4] Excluir
[0] Voltar""")
    while True:
        try:
            opcao = int(input("-> "))
            return opcao
        except ValueError:
            print("Opção inválida! Digite apenas números.")

def listar_medicacao():
    cursor.execute("SELECT id_med, nome_med FROM tbl_medicacao")
    resultado = cursor.fetchall()
    if not resultado:
        print("Nenhum registro encontrado.")
    else:
        for linha in resultado:
            print(f"[{linha[0]}] {linha[1]}")

def alterar_medicacao(id_med):
    print("""\nO que deseja alterar?
[1] Nome
[2] EAN
[0] Voltar""")
    while True:
        try:
            opcao = int(input("-> "))
            break
        except ValueError:
            print("Opção inválida! Digite apenas números.")

    if opcao == 0:
        return
    elif opcao == 1:
        novo_valor = input("Novo nome: ")
        campo = "nome_med"
    elif opcao == 2:
        novo_valor = input("Novo EAN: ")
        campo = "ean"
    else:
        print("Opção inválida!")
        return

    sql = f"UPDATE tbl_medicacao SET {campo} = %s WHERE id_med = %s"
    try:
        cursor.execute(sql, (novo_valor, id_med))
        conexao.commit()
        print(cursor.rowcount, "registro(s) alterado(s).")
    except mysql.connector.Error:
        print("Erro ao alterar! Verifique os dados e tente novamente.")

def inserir_medicacao():
    nome_med = input("Digite o nome: ")
    ean = input("Digite o ean: ")
    sql = "INSERT INTO tbl_medicacao (nome_med, ean) VALUES (%s,%s)"
    valores = (nome_med, ean)
    try:
        cursor.execute(sql, valores)
        conexao.commit()
        print(cursor.rowcount, "registro inserido.")
    except mysql.connector.Error:
        print("Erro ao inserir! EAN já cadastrado ou dados inválidos.")

def excluir_medicacao(id_med):
    cursor.execute("SELECT id_med FROM tbl_medicacao")
    if not cursor.fetchall():
        print("Nenhum registro encontrado. Impossível excluir.")
        return
    listar_medicacao()
    while True:
        try:
            cod = int(input("Digite o código do remédio a ser excluído: "))
            break
        except ValueError:
            print("Opção inválida! Digite apenas números.")
    confirma = input("""Você confirma a exclusão? [S/N] 
-> """).upper()
    if confirma == "S":
        try:
            sql = "DELETE FROM tbl_medicacao WHERE id_med = %s"
            valores = (cod,)
            cursor.execute(sql, valores)
            conexao.commit()
            print(cursor.rowcount, "registro(s) excluído(s).")
        except mysql.connector.Error:
            print("Erro ao excluir. Tente novamente!")
    else:
        print("Exclusão cancelada!")

def listar_estabelecimento():
    cursor.execute("SELECT id_esta, nome_esta FROM tbl_estabelecimento " \
    "WHERE tipo_esta NOT LIKE 'Residência de Acolhimento'")
    resultado = cursor.fetchall()
    if not resultado:
        print("Nenhum registro encontrado.")
    else:
        for linha in resultado:
            print(f"[{linha[0]}] {linha[1]}")

def menu_equipamento(id_esta):
    cursor.execute(
        "SELECT nome_esta FROM tbl_estabelecimento WHERE id_esta = %s", (id_esta,))
    resultado = cursor.fetchone()
    nome_esta = resultado[0]
    print(f"""\n### {nome_esta} ###
O que deseja fazer?
[1] Acolhidos
[2] Próximos Exames e Consultas
[3] Relatório de Medicações dos Acolhidos
[0] Voltar""")
    while True:
        try:
            opcao = int(input("-> "))
            return opcao
        except ValueError:
            print("Opção inválida! Digite apenas números.")

def menu_acolhidos(id_esta):
    print("""\n### Acolhidos ###
O que deseja fazer?
[1] Listar          
[2] Selecionar
[3] Inserir
[4] Excluir
[0] Voltar""")
    while True:
        try:
            opcao = int(input("-> "))
            return opcao
        except ValueError:
            print("Opção inválida! Digite apenas números.")

def menu_acolhido_unico(id_acolhido):
    cursor.execute(
        "SELECT nome_acolhido FROM tbl_acolhido WHERE id_acolhido = %s", (id_acolhido,))
    resultado = cursor.fetchone()
    nome_acolhido = resultado[0]
    print(f"""\n### {nome_acolhido} ###
O que deseja fazer?
[1] Informações Cadastrais
[2] Alteração de Dados
[3] Medicação
[4] Exames e Consultas
[0] Sair""")
    while True:
        try:
            opcao = int(input("-> "))
            return opcao
        except ValueError:
            print("Opção inválida! Digite apenas números.")

def informacoes_cadastrais(id_acolhido):
    cursor.execute(
        "SELECT nome_acolhido, cpf, data_nasc, cid FROM tbl_acolhido WHERE id_acolhido = %s", (id_acolhido,))
    resultado = cursor.fetchone()
    print(f"""
Nome: {resultado[0]}
CPF: {resultado[1]}
Data de Nascimento: {resultado[2].strftime('%d/%m/%Y')}
CID: {resultado[3]}
    """)

def alterar_acolhido(id_acolhido):
    informacoes_cadastrais(id_acolhido)
    print("""\nO que deseja alterar?
[1] Nome
[2] CPF
[3] Data de Nascimento
[4] CID
[0] Voltar""")
    while True:
        try:
            opcao = int(input("-> "))
            break
        except ValueError:
            print("Opção inválida! Digite apenas números.")

    if opcao == 0:
        return
    elif opcao == 1:
        novo_valor = input("Novo nome: ")
        campo = "nome_acolhido"
    elif opcao == 2:
        novo_valor = input("Novo CPF: ")
        campo = "cpf"
    elif opcao == 3:
        data = input("Nova data de nascimento dd/mm/aaaa: ")
        novo_valor = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
        campo = "data_nasc"
    elif opcao == 4:
        novo_valor = input("Novo CID: ")
        campo = "cid"
    else:
        print("Opção inválida!")
        return

    sql = f"UPDATE tbl_acolhido SET {campo} = %s WHERE id_acolhido = %s"
    try:
        cursor.execute(sql, (novo_valor, id_acolhido))
        conexao.commit()
        print(cursor.rowcount, "registro(s) alterado(s).")
    except mysql.connector.Error:
        print("Erro ao alterar! Verifique os dados e tente novamente.")

def listar_acolhidos(id_esta):
    cursor.execute(
        "SELECT id_acolhido, nome_acolhido FROM tbl_acolhido WHERE fk_nome_esta = %s", (id_esta,))
    resultado = cursor.fetchall()
    if not resultado:
        print("Nenhum registro encontrado.")
    else:
        for linha in resultado:
            print(f"[{linha[0]}] {linha[1]}")

def selecionar_acolhidos(id_esta):
    cursor.execute(
        "SELECT id_acolhido, nome_acolhido FROM tbl_acolhido WHERE fk_nome_esta = %s", (id_esta,))
    resultado = cursor.fetchall()
    for linha in resultado:
        print(f"[{linha[0]}] {linha[1]}")
    while True:
        try:
            id_acolhido = int(input("Digite o código do acolhido: "))
            return id_acolhido
        except ValueError:
            print("Opção inválida! Digite apenas números.")

def inserir_acolhido(id_esta):
    nome_acolhido = input("Digite o nome: ")
    cpf = input("Digite CPF: ")
    cpf = cpf.replace(".", "").replace("-", "")
    if len(cpf) != 11 or not cpf.isdigit():
        print("CPF inválido! Digite exatamente 11 números.")
        return
    while True:
        try:
            data_nasc = input("Digite a data de nascimento dd/mm/aaaa: ")
            data = datetime.strptime(data_nasc, "%d/%m/%Y")
            data_BD = data.strftime("%Y-%m-%d")
            break
        except ValueError:
            print("Data inválida! Use o formato dd/mm/aaaa.")
    cid = input("Digite seu CID[Deixe vazio se não tiver]: ")
    sql = "INSERT INTO tbl_acolhido (nome_acolhido, cpf, data_nasc, cid, fk_nome_esta) VALUES (%s,%s,%s,%s,%s)"
    valores = (nome_acolhido, cpf, data_BD, cid, id_esta)
    try:
        cursor.execute(sql, valores)
        conexao.commit()
        print(cursor.rowcount, "registro inserido.")
    except mysql.connector.Error:
        print("Erro ao inserir! CPF já cadastrado ou dados inválidos.")

def excluir_acolhido(id_esta):
    cursor.execute("SELECT id_acolhido FROM tbl_acolhido WHERE fk_nome_esta = %s", (id_esta,))
    if not cursor.fetchall():
        print("Nenhum registro encontrado. Impossível excluir.")
        return
    listar_acolhidos(id_esta)
    while True:
        try:
            cod = int(input("Digite o código do usuário a ser excluído: "))
            break
        except ValueError:
            print("Opção inválida! Digite apenas números.")
    confirma = input("""Você confirma a exclusão? [S/N] 
-> """).upper()
    if confirma == "S":
        try:
            sql = "DELETE FROM tbl_acolhido WHERE id_acolhido = %s"
            valores = (cod,)
            cursor.execute(sql, valores)
            conexao.commit()
            print(cursor.rowcount, "registro(s) excluído(s).")
        except mysql.connector.Error:
            print("Erro ao excluir. Tente novamente!")
    else:
        print("Exclusão cancelada!")

def menu_acolhido_medicacao(id_acolhido):
    print("""\n### Controle de Medicação do Acolhido ###
O que deseja fazer?
[1] Listar medicações do acolhido
[2] Inserir medicação
[3] Excluir medicação
[0] Voltar""")
    while True:
        try:
            opcao = int(input("-> "))
            return opcao
        except ValueError:
            print("Opção inválida! Digite apenas números.")

def listar_acolhido_medicacao(id_acolhido):
    cursor.execute("SELECT tbl_medicacao.nome_med, tbl_acolhido_medicacao.frequencia, tbl_acolhido_medicacao.observacao "
                   "FROM tbl_acolhido_medicacao "
                   "INNER JOIN tbl_medicacao ON tbl_acolhido_medicacao.fk_med = tbl_medicacao.id_med "
                   "WHERE tbl_acolhido_medicacao.fk_acolhido = %s ", (id_acolhido,))
    resultado = cursor.fetchall()
    if not resultado:
        print("Nenhum registro encontrado.")
    else:
        for linha in resultado:
            print(f"[{linha[0]}] {linha[1]}")

def inserir_acolhido_medicacao(id_acolhido):
    listar_medicacao()
    while True:
        try:
            fk_med = int(input("Digite o código da medicação: "))
            break
        except ValueError:
            print("Opção inválida! Digite apenas números.")
    while True:
        try:
            data_inicio = input("Data de início em dd/mm/aaaa: ")
            data = datetime.strptime(data_inicio, "%d/%m/%Y")
            data_inicio_BD = data.strftime("%Y-%m-%d")
            break
        except ValueError:
            print("Data inválida! Use o formato dd/mm/aaaa.")
    while True:
        try:
            data_fim = input("Data de fim em dd/mm/aaaa(Deixe vazio se for continuo): ")
            if data_fim == "":
                data_fim_DB = None
                break
            else:
                data = datetime.strptime(data_fim, "%d/%m/%Y")
                data_fim_DB = data.strftime("%Y-%m-%d")
                break
        except ValueError:
            print("Data inválida! Use o formato dd/mm/aaaa.")
    frequencia = input("Insira o horário ou as vezes que se toma por dia: ")
    observacao = input("""Observações?
-> """)
    sql = "INSERT INTO tbl_acolhido_medicacao (fk_acolhido, fk_med, data_inicio, data_fim, frequencia, observacao) VALUES (%s,%s,%s,%s,%s,%s)"
    valores = (id_acolhido, fk_med, data_inicio_BD, data_fim_DB, frequencia, observacao)
    try:
        cursor.execute(sql, valores)
        conexao.commit()
        print(cursor.rowcount, "registro inserido.")
    except mysql.connector.Error:
        print("Erro ao inserir! Verifique os dados e tente novamente.")

def excluir_acolhido_medicacao(id_acolhido):
    cursor.execute("SELECT id_acol_med FROM tbl_acolhido_medicacao WHERE fk_acolhido = %s", (id_acolhido,))
    if not cursor.fetchall():
        print("Nenhum registro encontrado. Impossível excluir.")
        return
    listar_acolhido_medicacao(id_acolhido)
    while True:
        try:
            cod = int(input("Digite o código do remédio a ser excluído: "))
            break
        except ValueError:
            print("Opção inválida! Digite apenas números.")
    confirma = input("""Você confirma a exclusão? [S/N] 
-> """).upper()
    if confirma == "S":
        try:
            sql = "DELETE FROM tbl_acolhido_medicacao WHERE id_acol_med = %s"
            valores = (cod,)
            cursor.execute(sql, valores)
            conexao.commit()
            print(cursor.rowcount, "registro(s) excluído(s).")
        except mysql.connector.Error:
            print("Erro ao excluir. Tente novamente!")
    else:
        print("Exclusão cancelada!")

def menu_consulta_exame(id_acolhido):
    print("""\n### Exames e Consultas ###
O que deseja fazer?
[1] Listar Exames e Consultas do Acolhido
[2] Inserir Exames e Consultas
[3] Excluir Exames e Consultas
[0] Voltar""")
    while True:
        try:
            opcao = int(input("-> "))
            return opcao
        except ValueError:
            print("Opção inválida! Digite apenas números.")

def listar_consulta_exame(id_acolhido):
    cursor.execute("SELECT tbl_consulta_exame.id_cons, tbl_estabelecimento.nome_esta, tbl_consulta_exame.data_cons, tbl_consulta_exame.hora_cons, tbl_consulta_exame.tipo_cons "
                   "FROM tbl_consulta_exame "
                   "INNER JOIN tbl_estabelecimento ON tbl_consulta_exame.fk_nome_esta = tbl_estabelecimento.id_esta "
                   "WHERE tbl_consulta_exame.fk_acolhido = %s ", (id_acolhido,))
    resultado = cursor.fetchall()
    if not resultado:
        print("Nenhum registro encontrado.")
    else:
        for linha in resultado:
            print(f"[{linha[0]}] Local: {linha[1]} | Data: {linha[2].strftime('%d/%m/%Y')} | Hora: {linha[3]} | Tipo: {linha[4]}")

def inserir_consulta_exame(id_acolhido):
    listar_estabelecimento()
    while True:
        try:
            fk_nome_esta = int(input("Digite o código do estabelecimento: "))
            break
        except ValueError:
            print("Opção inválida! Digite apenas números.")
    while True:
        try:
            data = input("Data em dd/mm/aaaa: ")
            data = datetime.strptime(data, "%d/%m/%Y")
            data_BD = data.strftime("%Y-%m-%d")
            break
        except ValueError:
            print("Data inválida! Use o formato dd/mm/aaaa.")
    while True:
        try:
            hora = input("Hora(ex: 14:30): ")
            hora = datetime.strptime(hora, "%H:%M")
            hora_BD = hora.strftime("%H:%M")
            break
        except ValueError:
            print("Hora inválida! Use o formato HH:MM.")
    tipo = input("Escreva se é consulta ou exame: ")
    sql = "INSERT INTO tbl_consulta_exame (fk_acolhido, fk_nome_esta, data_cons, hora_cons, tipo_cons) VALUES (%s,%s,%s,%s,%s)"
    valores = (id_acolhido, fk_nome_esta, data_BD, hora_BD, tipo)
    try:
        cursor.execute(sql, valores)
        conexao.commit()
        print(cursor.rowcount, "registro inserido.")
    except mysql.connector.Error:
        print("Erro ao inserir! Verifique os dados e tente novamente.")

def excluir_consulta_exame(id_acolhido):
    cursor.execute("SELECT id_cons FROM tbl_consulta_exame WHERE fk_acolhido = %s", (id_acolhido,))
    if not cursor.fetchall():
        print("Nenhum registro encontrado. Impossível excluir.")
        return
    listar_consulta_exame(id_acolhido)
    while True:
        try:
            cod = int(input("Digite o código do exame/consulta a ser excluído: "))
            break
        except ValueError:
            print("Opção inválida! Digite apenas números.")
    confirma = input("""Você confirma a exclusão? [S/N] 
-> """).upper()
    if confirma == "S":
        try:
            sql = "DELETE FROM tbl_consulta_exame WHERE id_cons = %s"
            valores = (cod,)
            cursor.execute(sql, valores)
            conexao.commit()
            print(cursor.rowcount, "registro(s) excluído(s).")
        except mysql.connector.Error:
            print("Erro ao excluir. Tente novamente!")
    else:
        print("Exclusão cancelada!")

def listar_proximos_exames_consultas(id_esta):
    cursor.execute("SELECT tbl_acolhido.nome_acolhido, tbl_estabelecimento.nome_esta, tbl_consulta_exame.data_cons, tbl_consulta_exame.hora_cons, tbl_consulta_exame.tipo_cons "
                   "FROM tbl_consulta_exame "
                   "INNER JOIN tbl_acolhido ON tbl_consulta_exame.fk_acolhido = tbl_acolhido.id_acolhido "
                   "INNER JOIN tbl_estabelecimento ON tbl_consulta_exame.fk_nome_esta = tbl_estabelecimento.id_esta "
                   "WHERE tbl_acolhido.fk_nome_esta = %s AND tbl_consulta_exame.data_cons >= CURDATE() "
                   "ORDER BY tbl_consulta_exame.data_cons, tbl_consulta_exame.hora_cons", (id_esta,))
    resultado = cursor.fetchall()
    print("\n=== Próximos Exames e Consultas ===")
    if not resultado:
        print("Nenhum registro encontrado.")
    else:
        for linha in resultado:
            print(
                f"{linha[0]} | Local: {linha[1]} | Data: {linha[2].strftime('%d/%m/%Y')} | Hora: {linha[3]} | Tipo: {linha[4]}")

def relatorio_medicacao(id_esta):
    cursor.execute("SELECT tbl_acolhido.nome_acolhido, tbl_medicacao.nome_med, tbl_acolhido_medicacao.frequencia "
                   "FROM tbl_acolhido_medicacao "
                   "INNER JOIN tbl_acolhido ON tbl_acolhido_medicacao.fk_acolhido = tbl_acolhido.id_acolhido "
                   "INNER JOIN tbl_medicacao ON tbl_acolhido_medicacao.fk_med = tbl_medicacao.id_med "
                   "WHERE tbl_acolhido.fk_nome_esta = %s", (id_esta,))
    resultado = cursor.fetchall()
    print("\n=== Relatório de Medicações ===")
    if not resultado:
        print("Nenhum registro encontrado.")
    else:
        for linha in resultado:
            print(f"{linha[0]}:")
            print(f"  - {linha[1]} → {linha[2]}")

while True:
    opcao = menu_principal()
    if (opcao == 0):
        print("\n### Obrigado por usar o Elo Social! ###")
        break

    elif (opcao == 1):
        while True:
            opcao2 = menu_equipamento(1)
            if opcao2 == 0:
                break
            elif opcao2 == 1:
                while True:
                    opcao3 = menu_acolhidos(1)
                    if opcao3 == 0:
                        break
                    elif opcao3 == 1:
                        listar_acolhidos(1)
                    elif opcao3 == 2:
                        id_acolhido = selecionar_acolhidos(1)
                        while True:
                            opcao4 = menu_acolhido_unico(id_acolhido)
                            if opcao4 == 0:
                                break
                            elif opcao4 == 1:
                                informacoes_cadastrais(id_acolhido)
                            elif opcao4 == 2:
                                alterar_acolhido(id_acolhido)
                            elif opcao4 == 3:
                                while True:
                                    opcao5 = menu_acolhido_medicacao(
                                        id_acolhido)
                                    if opcao5 == 0:
                                        break
                                    elif opcao5 == 1:
                                        listar_acolhido_medicacao(id_acolhido)
                                    elif opcao5 == 2:
                                        inserir_acolhido_medicacao(id_acolhido)
                                    elif opcao5 == 3:
                                        excluir_acolhido_medicacao(id_acolhido)
                            elif opcao4 == 4:
                                while True:
                                    opcao5 = menu_consulta_exame(id_acolhido)
                                    if opcao5 == 0:
                                        break
                                    elif opcao5 == 1:
                                        listar_consulta_exame(id_acolhido)
                                    elif opcao5 == 2:
                                        inserir_consulta_exame(id_acolhido)
                                    elif opcao5 == 3:
                                        excluir_consulta_exame(id_acolhido)
                    elif opcao3 == 3:
                        inserir_acolhido(1)
                    elif opcao3 == 4:
                        excluir_acolhido(1)
            elif opcao2 == 2:
                listar_proximos_exames_consultas(1)
            elif opcao2 == 3:
                relatorio_medicacao(1)
            else:
                print("Opção Inválida.")

    elif (opcao == 2):
        while True:
            opcao2 = menu_equipamento(2)
            if opcao2 == 0:
                break
            elif opcao2 == 1:
                while True:
                    opcao3 = menu_acolhidos(2)
                    if opcao3 == 0:
                        break
                    elif opcao3 == 1:
                        listar_acolhidos(2)
                    elif opcao3 == 2:
                        id_acolhido = selecionar_acolhidos(2)
                        while True:
                            opcao4 = menu_acolhido_unico(id_acolhido)
                            if opcao4 == 0:
                                break
                            elif opcao4 == 1:
                                informacoes_cadastrais(id_acolhido)
                            elif opcao4 == 2:
                                alterar_acolhido(id_acolhido)
                            elif opcao4 == 3:
                                while True:
                                    opcao5 = menu_acolhido_medicacao(
                                        id_acolhido)
                                    if opcao5 == 0:
                                        break
                                    elif opcao5 == 1:
                                        listar_acolhido_medicacao(id_acolhido)
                                    elif opcao5 == 2:
                                        inserir_acolhido_medicacao(id_acolhido)
                                    elif opcao5 == 3:
                                        excluir_acolhido_medicacao(id_acolhido)
                            elif opcao4 == 4:
                                while True:
                                    opcao5 = menu_consulta_exame(id_acolhido)
                                    if opcao5 == 0:
                                        break
                                    elif opcao5 == 1:
                                        listar_consulta_exame(id_acolhido)
                                    elif opcao5 == 2:
                                        inserir_consulta_exame(id_acolhido)
                                    elif opcao5 == 3:
                                        excluir_consulta_exame(id_acolhido)

                    elif opcao3 == 3:
                        inserir_acolhido(2)
                    elif opcao3 == 4:
                        excluir_acolhido(2)
                    else:
                        print("Opção Inválida.")
            elif opcao2 == 2:
                listar_proximos_exames_consultas(2)
            elif opcao2 == 3:
                relatorio_medicacao(2)
            else:
                print("Opcao Invalida")
    elif (opcao == 3):
        while True:
            opcao2 = menu_equipamento(3)
            if opcao2 == 0:
                break
            elif opcao2 == 1:
                while True:
                    opcao3 = menu_acolhidos(3)
                    if opcao3 == 0:
                        break
                    elif opcao3 == 1:
                        listar_acolhidos(3)
                    elif opcao3 == 2:
                        id_acolhido = selecionar_acolhidos(3)
                        while True:
                            opcao4 = menu_acolhido_unico(id_acolhido)
                            if opcao4 == 0:
                                break
                            elif opcao4 == 1:
                                informacoes_cadastrais(id_acolhido)
                            elif opcao4 == 2:
                                alterar_acolhido(id_acolhido)
                            elif opcao4 == 3:
                                while True:
                                    opcao5 = menu_acolhido_medicacao(
                                        id_acolhido)
                                    if opcao5 == 0:
                                        break
                                    elif opcao5 == 1:
                                        listar_acolhido_medicacao(id_acolhido)
                                    elif opcao5 == 2:
                                        inserir_acolhido_medicacao(id_acolhido)
                                    elif opcao5 == 3:
                                        excluir_acolhido_medicacao(id_acolhido)
                            elif opcao4 == 4:
                                while True:
                                    opcao5 = menu_consulta_exame(id_acolhido)
                                    if opcao5 == 0:
                                        break
                                    elif opcao5 == 1:
                                        listar_consulta_exame(id_acolhido)
                                    elif opcao5 == 2:
                                        inserir_consulta_exame(id_acolhido)
                                    elif opcao5 == 3:
                                        excluir_consulta_exame(id_acolhido)
                    elif opcao3 == 3:
                        inserir_acolhido(3)
                    elif opcao3 == 4:
                        excluir_acolhido(3)
                    else:
                        print("Opção Inválida.")
            elif opcao2 == 2:
                listar_proximos_exames_consultas(3)
            elif opcao2 == 3:
                relatorio_medicacao(3)
            else:
                print("Opcao Invalida")

    elif opcao == 4:
        while True:
            opcao2 = menu_medicacao()
            if opcao2 == 0:
                break
            elif opcao2 == 1:
                listar_medicacao()
            elif opcao2 == 2:
                while True:
                    try:
                        id_med = int(input("Digite o código da medicação: "))
                        break
                    except ValueError:
                        print("Opção inválida! Digite apenas números.")
                alterar_medicacao(id_med)
            elif opcao2 == 3:
                inserir_medicacao()
            elif opcao2 == 4:
                while True:
                    try:
                        id_med = int(input("Digite o código da medicação: "))
                        break
                    except ValueError:
                        print("Opção inválida! Digite apenas números.")
                excluir_medicacao(id_med)
            else:
                print("Opção Inválida.")
    else:
        print("Opção Inválida. Insira novamente. \n")
