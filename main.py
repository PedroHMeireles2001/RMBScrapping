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

def main(data):
    conexao = None
    try:
        conexao = banco.conecta()
    except:
        return False


    data_formatada = data.strftime('%d/%m/%Y')
    url = f'https://rmb.varejofacil.com/vendaConsolidada/porLoja?=&filtro.dataInicial={data_formatada}&filtro.dataFinal={data_formatada}&filtro.itemMenuSelecionado=loja&filtro.tipoDeGrafico=&filtro.codigoDaHolding=&filtro.codigoDaLoja=&_=1710854458959'
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="lin",  # Generate only Windows platform
        headers=False  # generate misc headers
    )
    customUserAgent = header.generate()['User-Agent']

    chrome_options.add_argument(f"user-agent={customUserAgent}")

    # Configurando driver
    servico = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servico, options=chrome_options)

    # logando
    try:
        driver.get(url)
        time.sleep(5)
        driver.find_element('xpath',
                            '/html/body/div[1]/div[1]/section[2]/div/form/div[1]/div/div/div[2]/input').send_keys(
            Variables.varejo_user)
        time.sleep(1)
        driver.find_element('xpath',
                            '/html/body/div[1]/div[1]/section[2]/div/form/div[2]/div/div/div[2]/input').send_keys(
            Variables.verejo_senha)
        driver.find_element('xpath', '/html/body/div[1]/div[1]/section[2]/div/form/button').click()
        time.sleep(10)
    except:
        return False

    driver.save_screenshot('screenshot.png')

    if not banco.delete_duplicate(conexao, data):
        return False


    # pegando os dados geral
    parsed_json = pegar_json(driver, url)
    vendas = parsed_json['vendas']
    for venda in vendas:
        banco.insere_venda(conexao,venda,data)
    salvar_json(vendas, "lojas.json")

    # pegando os dados de cada loja
    for i in range(1, 6, 1):
        if i == 4:
            continue
        url = f'https://rmb.varejofacil.com/vendaConsolidada/porProdutosMaisVendidos?=&filtro.dataInicial={data_formatada}&filtro.dataFinal={data_formatada}&filtro.itemMenuSelecionado=produto&filtro.tipoDeGrafico=&filtro.codigoDaHolding=&filtro.codigoDaLoja={i}&_=1710854458978'
        parsed_json = pegar_json(driver, url)
        vendas = parsed_json['vendas']
        salvar_json(vendas, f'loja_{i}.json')
        for venda in vendas:
            banco.insere_produto(conexao,venda,data,i)
        time.sleep(1)
    driver.close()
    conexao.close()
    return True


if __name__ == "__main__":
    dia_anterior = datetime.now() - timedelta(days=1)
    main(dia_anterior)
