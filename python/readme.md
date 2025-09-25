
# RPA para Extração de Filmes do IMDB

Este projeto é um robô de automação (RPA) desenvolvido em Python que extrai informações dos filmes mais bem avaliados do IMDB.

## Funcionalidades

- Extrai dados (nome, ano, duração, nota, sinopse) dos 250 filmes mais bem avaliados do IMDB.
- Lida com mecanismos de detecção de robôs, banners de cookies e pop-ups de login para garantir uma extração estável.
- Organiza todos os artefatos de cada execução (logs, planilhas, arquivos de depuração) em uma pasta única com data e hora.
- Salva os dados finais em uma planilha Excel e exibe um sumário da execução ao final.

## Estrutura de Pastas

O projeto está organizado da seguinte forma:

```

projeto\_rpa/
├── executions/              \# Contém as pastas de cada execução
│   └── run\_AAAA-MM-DD\_HH-MM-SS/
│       ├── log/
│       ├── dados\_extraidos/
│       ├── dados\_processados/
│       └── debug/
├── src/                     \# Código-fonte do projeto
│   ├── **init**.py
│   ├── scraper.py
│   └── data\_handler.py
└── main.py                  \# Ponto de entrada para executar o robô

````

## Tecnologias

- **Python 3.x**
- **Selenium:** Para automação da navegação e extração de dados.
- **Pandas:** Para a estruturação e salvamento dos dados em Excel.
- **WebDriver Manager:** Para o gerenciamento automático do driver do navegador.

## Pré-requisitos

- **Python 3.8 ou superior** instalado.
- **Google Chrome** instalado.

## Instalação

**1. Clone o repositório:**
```bash
git clone git@github.com:deivid-a1/web_scraper_invisual.git
cd web_scraper_invisual/python
````

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
Instale as bibliotecas com o comando:

```bash
pip install -r requirements.txt
```

## Execução

Com o ambiente virtual ativado, execute o script principal a partir da raiz do projeto:

```bash
python main.py
```

Ao final da execução, uma nova pasta será criada dentro do diretório `executions/`. Esta pasta conterá o log detalhado, os arquivos de depuração (se houver erros) e a planilha Excel final com os dados dos filmes em `dados_processados/`.
