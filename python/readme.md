# RPA para Extração de Filmes do IMDB

Este projeto consiste em um robô de automação (RPA) desenvolvido em Python que extrai os dados dos filmes mais bem avaliados do site IMDB, salva essas informações em uma planilha Excel e, por fim, organiza os arquivos gerados.

## Funcionalidades

1.  Abre o navegador e navega até a página do Google e, em seguida, para o [Top 250 Filmes do IMDB em português](https://www.imdb.com/pt/chart/top/).
2.  Extrai as seguintes informações de cada filme da lista:
      * Nome do filme
      * Ano de lançamento
      * Duração
      * Nota de avaliação
      * Sinopse
3.  Insere todos os dados coletados em uma planilha do Excel (`.xlsx`).
4.  Salva a planilha em um diretório chamado `dados_extraidos`.
5.  Move a planilha recém-criada para um diretório final chamado `dados_processados`.

## Tecnologias Utilizadas

  * **Python 3.x**
  * **Selenium:** Para automação da navegação e extração de dados da web.
  * **Pandas:** Para a estruturação dos dados e criação do arquivo Excel.
  * **WebDriver Manager:** Para o gerenciamento automático do driver do navegador.

## Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

### 1\. Pré-requisitos

  * **Python 3.8 ou superior** instalado.
  * **Google Chrome** instalado.

### 2\. Instalação

**a. Clone o repositório:**

```bash
git clone git@github.com:deivid-a1/web_scraper_invisual.git
cd web_scraper_invisual/python/
```

**b. Crie e ative um ambiente virtual (recomendado):**

```bash
# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente no Windows
venv\Scripts\activate

# Ativa o ambiente no macOS/Linux
source venv/bin/activate
```

**c. Instale as dependências:**
Crie um arquivo chamado `requirements.txt` na raiz do projeto com o seguinte conteúdo:

```
selenium
pandas
webdriver-manager
openpyxl
```

Em seguida, instale as bibliotecas com o comando:

```bash
pip install -r requirements.txt
```

### 3\. Execução

Com o ambiente virtual ativado e as dependências instaladas, execute o script principal:

```bash
python main.py
```

Após a execução, duas pastas serão criadas no diretório do projeto: `dados_extraidos` e `dados_processados`. O arquivo final `top_filmes_imdb.xlsx` estará localizado dentro da pasta `dados_processados`.

-----

## Sugestões de Melhorias

Este projeto é um excelente ponto de partida, mas pode ser aprimorado com práticas mais avançadas de engenharia de software para torná-lo mais robusto, escalável e de fácil manutenção.

#### 1\. **Logging Estruturado**

Substituir os comandos `print()` por um sistema de logging (utilizando o módulo `logging` do Python). Isso permite:

  * Controlar o nível de detalhe das mensagens (DEBUG, INFO, WARNING, ERROR).
  * Salvar os logs de execução em arquivos, facilitando a depuração de erros que ocorrem quando o robô roda de forma autônoma.

#### 2\. **Tratamento de Erros e Retentativas (Resiliência)**

A extração de dados pode falhar por instabilidade da rede ou mudanças no layout do site. É possível tornar o robô mais resiliente implementando:

  * Blocos `try...except` mais específicos para capturar diferentes tipos de exceções (ex: `TimeoutException`, `NoSuchElementException`).
  * Uma política de retentativas (usando bibliotecas como a `tenacity`) para que o robô tente novamente uma operação que falhou, como carregar uma página, antes de desistir.

#### 3\. **Arquivo de Configuração**

Remover dados "hardcoded" (como URLs, nomes de arquivos e diretórios) do código-fonte e movê-los para um arquivo de configuração externo (ex: `config.ini`, `.env`). Isso permite alterar parâmetros da execução sem modificar o código.

#### 4\. **Aumento de Performance com Processamento Paralelo/Assíncrono**

O processo de visitar a página de cada filme individualmente é lento. Para acelerar a extração, poderíamos utilizar:

  * **Multithreading/Multiprocessing:** Para baixar os detalhes de vários filmes simultaneamente.
  * **Bibliotecas assíncronas (AsyncIO):** Com `aiohttp` e `beautifulsoup4` (ou `pyppeteer`), seria possível fazer requisições de forma não bloqueante, otimizando o tempo de espera de I/O.

#### 5\. **Containerização com Docker**

"Dockerizar" a aplicação para encapsular o robô e todas as suas dependências em um contêiner. Isso garante que o ambiente de execução seja consistente e simplifica o deploy em qualquer máquina ou servidor que tenha o Docker instalado, eliminando o clássico problema do "funciona na minha máquina".

#### 6\. **Validação de Dados**

Utilizar uma biblioteca como `Pydantic` para criar modelos de dados que validem as informações extraídas. Isso garante a integridade dos dados (ex: o campo `Ano` é sempre um número, a `Nota` é um float), evitando que dados corrompidos ou mal formatados sejam salvos na planilha final.

#### 7\. **Escalabilidade do Armazenamento**

Para volumes maiores de dados, salvar em um arquivo Excel pode não ser a melhor solução. O projeto poderia ser estendido para salvar os dados em um banco de dados (como **SQLite** para simplicidade, ou **PostgreSQL** para um ambiente mais robusto), facilitando consultas e análises futuras.

#### 8\. **Scraping Consciente**

Para evitar sobrecarregar o servidor do IMDB ou ter o acesso bloqueado, é uma boa prática adicionar pausas (`time.sleep()`) entre as requisições, simulando um comportamento de navegação mais humano.