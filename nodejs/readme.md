# RPA para Extração de Filmes do IMDB (Versão Node.js)

Este projeto é um robô de automação (RPA) desenvolvido em Node.js que extrai informações dos filmes mais bem avaliados do site IMDB.

## Funcionalidades

  - Extrai dados (nome, ano, duração, nota, sinopse) dos 250 filmes mais bem avaliados do IMDB.
  - Utiliza técnicas de camuflagem para evitar a detecção de robôs.
  - Lida com banners de cookies e pop-ups de login para garantir uma extração estável.
  - Organiza todos os artefatos de cada execução (logs, planilhas, arquivos de depuração) em uma pasta única com data e hora.
  - Salva os dados de forma incremental (filme a filme) para otimizar o uso de memória.
  - Consolida os dados finais em uma planilha Excel e exibe um sumário da execução ao final.

## Estrutura de Pastas

O projeto está organizado da seguinte forma:

```
nodejs/
├── executions/              # Contém as pastas de cada execução
│   └── run_AAAA-MM-DD-HH-MM-SS-MSZ/
│       ├── log/
│       ├── dados_extraidos/
│       ├── dados_processados/
│       └── debug/
├── src/                     # Código-fonte do projeto
│   ├── scraper.js
│   ├── dataHandler.js
│   └── logger.js
├── main.js                  # Ponto de entrada para executar o robô
├── package.json
└── README.md
```

## Tecnologias

  - **Node.js**
  - **Selenium-WebDriver:** Para automação da navegação e extração de dados.
  - **ExcelJS:** Para a geração do arquivo Excel.
  - **Winston:** Para um sistema de logging robusto.
  - **ChromeDriver:** Gerenciado como uma dependência do `npm`.

## Pré-requisitos

  - **Node.js v16 ou superior** instalado.
  - **NPM** (geralmente instalado com o Node.js).
  - **Google Chrome** instalado.

## Instalação

**1. Clone o repositório:**

```bash
git clone git@github.com:deivid-a1/web_scraper_invisual.git
cd web_scraper_invisual/nodejs
```

**2. Instale as dependências:**
A partir da raiz do projeto, execute o comando abaixo. Ele irá baixar todas as bibliotecas listadas no `package.json`.

```bash
npm install
```

## Execução

Para iniciar o robô, utilize o script definido no `package.json`:

```bash
npm start
```

Ou execute diretamente o arquivo principal:

```bash
node main.js
```

Ao final da execução, uma nova pasta será criada dentro do diretório `executions/`. Esta pasta conterá o log detalhado, os arquivos JSON individuais em `dados_extraidos/`, os arquivos de depuração (se houver erros) e a planilha Excel final com os dados consolidados em `dados_processados/`.