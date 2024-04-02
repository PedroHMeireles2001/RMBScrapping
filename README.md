# Bot de Web Scraping para Varejo Fácil

## Descrição

Este projeto consiste no desenvolvimento de um bot de automação para varejo com a única finalidade de realizar web scraping em um sistema denominado "Varejo Fácil". O bot coleta dados relevantes do sistema e os armazena em um banco de dados MySQL para análise posterior. Essa abordagem permite que as empresas realizem uma análise detalhada dos dados coletados, identifiquem tendências de mercado e tomem decisões estratégicas embasadas.

## Funcionalidades

  **Web Scraping do Varejo Fácil**: O bot realiza web scraping do sistema "Varejo Fácil", coletando informações como inventário de produtos, vendas realizadas, histórico de compras dos clientes, entre outros.
    
-  **Armazenamento em Banco de Dados**: Os dados coletados são armazenados em um banco de dados MySQL, proporcionando uma base sólida para análise e consulta posterior.

-   **Rota para Atualizar os Dados Manualmente**: Implementa uma rota no Flask para atualização manual dos dados, permitindo que os usuários possam forçar uma nova coleta de dados a qualquer momento.
    
-   **Cron Job para Execução Automática**: Utiliza um cron job para agendar a execução do script principal (`main.py`) em intervalos regulares, garantindo que os dados sejam atualizados automaticamente em determinados horários.
    

## Tecnologias Utilizadas

-   **Linguagem de Programação**: Python
-   **Bibliotecas**: Selenium, Flask
-   **Banco de Dados**: MySQL


## Como Utilizar

1. **Configuração do Ambiente**:
   - Crie um ambiente virtual Python utilizando o `venv`:
     ```
     python3 -m venv venv
     ```
   - Ative o ambiente virtual:
     - No Windows:
       ```
       venv\Scripts\activate
       ```
     - No Linux/macOS:
       ```
       source venv/bin/activate
       ```
2. **Instalação das Dependências**:
   ```
   pip install -r requirements.txt
   ```

3. **Configuração das Credenciais**:
   - Renomeie o arquivo `.env.example` para `.env`.
   - Edite o arquivo `.env` e forneça as credenciais de acesso necessárias, como as informações de login para o sistema "Varejo Fácil" e as configurações do banco de dados MySQL.

4. **Execução do Bot**:
   ```
   python main.py
   ```

   Certifique-se de que o bot esteja conectado à internet para realizar o web scraping e que o banco de dados MySQL esteja configurado corretamente para receber os dados coletados do dia anterior.

5. **Atualização Manual dos Dados**:
   - Utilize a rota fornecida pelo Flask ("/bot?data=dd/MM/yyyy")  para atualizar manualmente os dados, acessando-a por meio de um navegador ou enviando uma requisição HTTP.
   - ``python Flask.py``

6. **Execução Automática com Cron Job**:
   - Configure um cron job no servidor onde o bot está hospedado para executar o script `main.py` em intervalos regulares. Por exemplo, para agendar a execução a cada 6 horas, você pode adicionar a seguinte linha ao seu arquivo de cron jobs:
     ```
     0 */6 * * * /path/to/python /path/to/main.py
     ```
   Isso garantirá que os dados sejam atualizados automaticamente sem intervenção manual. Certifique-se de substituir `/path/to/python` pelo caminho para a instalação do Python e `/path/to/main.py` pelo caminho para o script principal do bot.
    

## Autor

Este projeto foi desenvolvido por Pedro Meireles e faz parte do trabalho RMBScrapping
