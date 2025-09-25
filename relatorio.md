# Relatório Técnico do Projeto RPA IMDB

## 1. Introdução

Este documento detalha o processo de desenvolvimento e depuração do robô de automação para extração de dados do IMDB. O objetivo inicial era criar um script funcional que coletasse informações sobre os 250 filmes mais bem avaliados, mas o projeto evoluiu para uma solução robusta, resiliente e bem arquitetada, capaz de contornar desafios complexos de web scraping.

## 2. Fases do Projeto

### Fase 1: Implementação e Arquitetura Inicial

- **Desafio:** Criar um script funcional para navegar até o IMDB, extrair os dados e salvá-los em um arquivo Excel.
- **Solução:** Um primeiro script monolítico foi criado usando Selenium e Pandas.
- **Evolução:** O script foi rapidamente refatorado para uma arquitetura orientada a objetos, separando as responsabilidades em classes distintas (`IMDBScraper`, `DataHandler`) e organizando o código-fonte em um diretório `src/`, tornando o projeto mais limpo, manutenível e escalável.

### Fase 2: A Jornada de Depuração

A fase mais crítica do projeto envolveu a resolução de uma série de problemas que impediam a extração de dados. Cada problema resolvido revelava uma camada mais profunda de complexidade.

**Problema 1: `TimeoutException` e Detecção de Automação**
- **Sintoma:** O script falhava consistentemente ao tentar carregar a página de detalhes do filme, mesmo com seletores HTML/CSS inicialmente corretos.
- **Hipótese:** O site poderia estar bloqueando o robô através de mecanismos de detecção de automação, pop-ups ou banners.
- **Solução Aplicada:**
    1.  Implementação de funções para detectar e fechar o **banner de consentimento de cookies** e o **pop-up de login**.
    2.  Aplicação de **técnicas avançadas de camuflagem** no Selenium para esconder a "bandeira" de automação (`navigator.webdriver`), fazendo o robô se passar por um navegador humano.
- **Resultado:** O `Timeout` principal foi resolvido, permitindo que o robô carregasse a página, mas a extração de alguns dados ainda falhava.

**Problema 2: A Sinopse Fantasma (O Desafio Final)**
- **Sintoma:** Mesmo com a página carregada, a sinopse consistentemente não era encontrada, resultando em avisos e dados nulos. Múltiplas tentativas de corrigir o seletor CSS (`class`) e usar seletores complexos com XPath (baseados nos títulos "Enredo" ou "Storyline") falharam.
- **Ponto de Virada (Diagnóstico):** A implementação de uma **rotina de depuração** que salvava o código-fonte HTML da página no momento do erro foi crucial. Ao analisar o arquivo `debug_page_synopsis_fail_*.html` fornecido, a causa raiz foi finalmente descoberta.
- **Causa Raiz Definitiva:** Todas as tentativas anteriores falharam porque procuravam a sinopse na seção "Storyline" (Enredo) na parte inferior da página. A análise do HTML de depuração revelou que a sinopse estava, na verdade, em uma seção completamente diferente, muito mais acima na página, dentro de uma tag `<p>` com um identificador de teste estável.
- **Solução Definitiva:** Abandono de todas as estratégias complexas e frágeis em favor de um **seletor CSS simples, direto e robusto**, baseado na evidência do arquivo de depuração: `[data-testid='plot']`.
- **Resultado:** A sinopse passou a ser extraída com 100% de sucesso, finalizando a fase de depuração.

### Fase 3: Melhorias de Arquitetura e Observabilidade

- **Desafio:** Os artefatos do projeto (logs, planilhas) estavam sendo sobrescritos a cada execução e o acúmulo de dados em memória representava um risco para a estabilidade.
- **Solução 1 - Arquitetura Orientada por Execução:** Foi implementado um sistema onde cada execução do robô cria uma pasta única com data e hora no diretório `executions/`. Essa pasta armazena de forma isolada todos os arquivos gerados (logs, planilhas e arquivos de depuração), garantindo um histórico completo e organizado.
- **Solução 2 - Processamento Incremental:** Para otimizar o uso de memória, a lógica foi alterada para salvar os dados de cada filme em um arquivo `.json` individual. Ao final de todo o processo, esses arquivos são lidos e consolidados em uma única planilha Excel, tornando o robô escalável e resiliente a falhas de memória.
- **Evolução:** Foi adicionado um sumário detalhado ao final do log, informando o tempo total de execução e outras estatísticas, melhorando a observabilidade do processo.

## 3. Próximos Passos e Melhorias Sugeridas

O projeto encontra-se em um estado estável, funcional e bem arquitetado, mas pode ser expandido com as seguintes melhorias:

1.  **Paralelismo com Gerenciamento de Proxies:** Para acelerar a extração em cenários de larga escala, a paralelização poderia ser implementada, desde que combinada com um serviço de proxies rotativos para evitar bloqueios de IP.
2.  **Armazenamento em Banco de Dados:** Substituir o salvamento em Excel por um banco de dados (como SQLite para simplicidade ou PostgreSQL para produção) para permitir consultas mais complexas e melhor gerenciamento dos dados.
3.  **Configuração Externa:** Mover parâmetros como a URL do IMDB e nomes de arquivos para um arquivo de configuração (`.env` ou `config.ini`) para facilitar a manutenção sem alterar o código.
4.  **Containerização com Docker:** Empacotar a aplicação em um contêiner Docker para garantir a portabilidade e simplificar o deploy em qualquer ambiente.
5.  **Interface Gráfica:** Desenvolver uma interface de usuário simples (com Tkinter ou Streamlit) para que usuários não técnicos possam executar o robô e acompanhar seu progresso.