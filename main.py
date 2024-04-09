import json

from fake_headers import Headers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from utils import salvar_json, pegar_json
from datetime import datetime, timedelta
import time
import banco
import Variables
import calendar

def log(msg):
    print("[BOT] " + msg)
def initialze_driver(generateFakeHeaders=True,incognito=True):
    chrome_options = Options()

    if incognito:
        chrome_options.add_argument("incognito")
        chrome_options.add_argument("−−incognito")

    if generateFakeHeaders:
        header = Headers(
            browser="chrome",  # Generate only Chrome UA
            os="lin",  # Generate only Windows platform
            headers=False  # generate misc headers
        )
        customUserAgent = header.generate()['User-Agent']
        chrome_options.add_argument(f"user-agent={customUserAgent}")

    # Configurando driver
    servico = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=servico, options=chrome_options)

def login(driver):
    # logando
    try:
        driver.get("https://rmb.varejofacil.com/app/#/login")
        time.sleep(30)
    except:
        return False

    driver.save_screenshot('screenshot.png')

def atualizar_venda_loja(driver,conexao,data):

    log("Deletando duplicatas de vendas clientes")
    if not banco.delete_duplicate_clientes(conexao, data):
        raise Exception("Falha ao deletar duplicatas")

    log("Atualizando vendas de vendas clientes")
    data_formatada = data.strftime('%d/%m/%Y')
    url = f'https://rmb.varejofacil.com/vendaConsolidada/porLoja?=&filtro.dataInicial={data_formatada}&filtro.dataFinal={data_formatada}&filtro.itemMenuSelecionado=loja&filtro.tipoDeGrafico=&filtro.codigoDaHolding=&filtro.codigoDaLoja=&_=1710854458959'

    # pegando os dados geral
    parsed_json = pegar_json(driver, url)



    vendas = parsed_json['vendas']
    for venda in vendas:
        banco.insere_venda(conexao, venda, data)
    salvar_json(vendas, "lojas.json")

def atualizar_venda_dia(driver,conexao,data):
    data_formatada = data.strftime('%d/%m/%Y')

    log("Deletando duplicatas de vendas diárias")
    if not banco.delete_duplicate_dia(conexao, data):
        raise Exception("Falha ao deletar duplicatas")

    log("Atualizando vendas diárias")
    pegar_venda_por_produto_todas_lojas(driver,banco.insere_produto,conexao,data,data)

def pegar_venda_por_produto_todas_lojas(driver,funcaoInseridora,conexao,dataIncio,dataFim):
    cursor = conexao.cursor()
    for i in range(1, 6, 1):
        if i == 4:
            continue
        vendas = pegar_vendas_por_produto(driver, dataIncio, dataFim, i)
        salvar_json(vendas, f'loja_{i}.json')
        for venda in vendas:
            funcaoInseridora(cursor, venda, dataIncio, i)
        time.sleep(1)
    conexao.commit()
    cursor.close()

def pegar_vendas_por_produto(driver,dataInicio,dataFim,loja):
    dataInicioFormatada = dataInicio.strftime('%d/%m/%Y')
    dataFimFormatada  =dataFim.strftime('%d/%m/%Y')
    url = f'https://rmb.varejofacil.com/vendaConsolidada/porProdutosMaisVendidos?=&filtro.dataInicial={dataInicioFormatada}&filtro.dataFinal={dataFimFormatada}&filtro.itemMenuSelecionado=produto&filtro.tipoDeGrafico=&filtro.codigoDaHolding=&filtro.codigoDaLoja={loja}&_=1710854458978'
    parsed_json = pegar_json(driver, url)
    return parsed_json['vendas']

def atualizar_vendas(driver, conexao,args):
    atualizar_venda_loja(driver, conexao,args[0])
    atualizar_venda_dia(driver, conexao,args[0])

def atualizar_venda_mensal(driver, conexao,args):
    ano = args[0]
    mes = args[1]

    if not banco.delete_duplicate_mensal(conexao,ano,mes):
        raise Exception("Falha ao deletar duplicatas")


    dataInicio = datetime(year=ano, month=mes, day=1)
    dataFim = datetime(year=ano,month=mes,day=calendar.monthrange(ano, mes)[1])
    pegar_venda_por_produto_todas_lojas(driver,banco.insere_produto_mensal,conexao,dataInicio,dataFim)

def executar(function):
    def wrapper(args):
        conexao = None
        driver = None
        try:
            log("Conectando no banco: " + Variables.database +", No IP: "+Variables.host)
            conexao = banco.conecta()
            log("Inicializando Driver")
            driver = initialze_driver()
            log("Logando no varejo fácil")
            login(driver)
            log("Excutando tarefa")
            function(driver, conexao,args)
            log("Fechando conexão")
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            if conexao:
                conexao.close()
            if driver:
                driver.close()
    return wrapper
def main(data):
    return executar(atualizar_vendas)([data])

def main_mensal(ano,mes):
    return executar(atualizar_venda_mensal)([ano,mes])


if __name__ == "__main__":
    dia_anterior = datetime.now() - timedelta(days=1)
    main(dia_anterior)
