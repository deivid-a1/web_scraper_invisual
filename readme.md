
# RPA para Extração de Filmes do IMDB (Python e Node.js)

Este repositório contém um robô de automação (RPA) desenvolvido para extrair informações dos filmes mais bem avaliados do site IMDB. O projeto oferece duas implementações funcionalmente equivalentes: uma em **Python** e outra em **Node.js**.

## Funcionalidades Principais

Ambas as versões do robô compartilham as seguintes funcionalidades:

  - **Extração de Dados:** Coleta informações detalhadas dos 250 filmes mais bem avaliados, incluindo nome, ano, duração, nota e sinopse.
  - **Navegação Inteligente:** Lida com mecanismos de detecção de robôs, como banners de cookies e pop-ups de login, para garantir uma extração de dados estável e contínua.
  - **Organização de Artefatos:** Cria uma pasta única para cada execução, nomeada com data e hora, para armazenar todos os arquivos gerados (logs, planilhas e arquivos de depuração).
  - **Processamento de Dados:** Salva os dados de cada filme individualmente e, ao final, consolida todas as informações em uma única planilha Excel.
  - **Relatório de Execução:** Exibe um sumário detalhado ao final do processo, informando o tempo de execução, o total de filmes processados e o número de sucessos e falhas.

## Estrutura do Projeto

O repositório está dividido em duas pastas principais, `python/` e `nodejs/`, cada uma contendo uma implementação completa e independente do robô. A estrutura interna de cada projeto é semelhante:

```
/
├── python/
│   ├── executions/
│   ├── src/
│   │   ├── scraper.py
│   │   └── data_handler.py
│   ├── main.py
│   └── requirements.txt
│
└── nodejs/
    ├── executions/
    ├── src/
    │   ├── scraper.js
    │   ├── dataHandler.js
    │   └── logger.js
    ├── main.js
    └── package.json
```

## Tecnologias Utilizadas

### Versão Python

  - **Linguagem:** Python 3.8+
  - **Automação Web:** Selenium
  - **Manipulação de Dados:** Pandas
  - **Geração de Excel:** openpyxl
  - **Gerenciamento de Drivers:** WebDriver Manager

### Versão Node.js

  - **Ambiente de Execução:** Node.js v16+
  - **Automação Web:** Selenium-WebDriver
  - **Geração de Excel:** ExcelJS
  - **Sistema de Logging:** Winston

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados em sua máquina:

  - **Git**
  - **Google Chrome**
  - **Python 3.8 ou superior** (para a versão Python)
  - **Node.js v16 ou superior** (para a versão Node.js)

## Instalação e Execução

Primeiro, clone o repositório para a sua máquina local:

```bash
git clone git@github.com:deivid-a1/web_scraper_invisual.git
```

Após clonar, siga as instruções específicas para a versão que deseja executar.

-----

### 🐍 Para a versão em Python

**1. Navegue até a pasta do projeto:**

```bash
cd web_scraper_invisual/python
```

**2. Crie e ative um ambiente virtual:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**4. Execute o robô:**

```bash
python main.py
```

-----

### 🚀 Para a versão em Node.js

**1. Navegue até a pasta do projeto:**

```bash
cd web_scraper_invisual/nodejs
```

**2. Instale as dependências:**

```bash
npm install
```

**3. Execute o robô:**

```bash
npm start
```

ou

```bash
node main.js
```

## Saída do Projeto

Ao final da execução de qualquer uma das versões, uma nova pasta será criada dentro do diretório `executions/` (por exemplo, `run_AAAA-MM-DD_HH-MM-SS`). Esta pasta conterá:

  - **`/log/`**: Um arquivo de log detalhado (`execution.log`) com todos os passos da execução.
  - **`/dados_extraidos/`**: Arquivos JSON individuais para cada filme extraído.
  - **`/dados_processados/`**: A planilha Excel final (`top_filmes_imdb.xlsx`) com todos os dados consolidados.
  - **`/debug/`**: Capturas de tela ou código-fonte HTML de páginas onde ocorreram erros (se aplicável).