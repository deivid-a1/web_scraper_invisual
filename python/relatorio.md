
# Relatório Técnico do Projeto RPA IMDB

## 1. Introdução

Este documento detalha o processo de desenvolvimento e depuração do robô de automação para extração de dados do IMDB. O objetivo inicial era criar um script funcional que coletasse informações sobre os 250 filmes mais bem avaliados, mas o projeto evoluiu para uma solução robusta, resiliente e bem arquitetada.

## 2. Fases do Projeto

### Fase 1: Implementação e Arquitetura Inicial

- **Desafio:** Criar um script funcional para navegar até o IMDB, extrair os dados e salvá-los em um arquivo Excel.
- **Solução:** Um primeiro script monolítico foi criado usando Selenium e Pandas.
- **Evolução:** O script foi refatorado para uma arquitetura orientada a objetos, separando as responsabilidades em classes distintas (`IMDBScraper`, `DataHandler`) e organizando o código-fonte em um diretório `src/`, tornando o projeto mais limpo, manutenível e escalável.

### Fase 2: A Jornada de Depuração dos Timeouts

A fase mais crítica do projeto envolveu a resolução de erros de `TimeoutException` persistentes, que impediam a extração dos dados das páginas de detalhes dos filmes.

**Problema 1: `TimeoutException` Inicial**
- **Sintoma:** O script falhava consistentemente ao tentar carregar a primeira página de detalhes do filme, mesmo com seletores HTML/CSS corretos.
- **Hipótese:** O site poderia estar bloqueando o robô através de mecanismos simples, como banners ou pop-ups.
- **Solução Aplicada:** Foram implementadas funções para detectar e fechar o **banner de consentimento de cookies** e o **pop-up de login** que sobrepunham a página.
- **Resultado:** O problema persistiu, indicando uma causa mais profunda e sofisticada.

**Problema 2: Detecção Ativa de Automação (Causa Raiz)**
- **Sintoma:** A análise dos arquivos HTML de depuração revelou que a página era carregada, mas o Selenium não conseguia interagir com ela. Isso provou que não era um simples bloqueio de carregamento.
- **Hipótese Definitiva:** O site executava scripts JavaScript para verificar a propriedade `navigator.webdriver` e outras "bandeiras" que identificam um navegador controlado por automação.
- **Solução Definitiva:** Foram implementadas técnicas avançadas de camuflagem no `_setup_driver`:
    1.  Desativação das "flags" de automação do Chrome com `excludeSwitches` e `useAutomationExtension`.
    2.  Sobrescrita da propriedade `navigator.webdriver` para `undefined` usando `execute_cdp_cmd`, tornando o robô praticamente indistinguível de um navegador humano.

**Problema 3: Ajuste Fino de Seletores**
- **Sintoma:** Após resolver o `Timeout`, o robô passou a registrar avisos de `Ano ou duração não encontrados`.
- **Hipótese:** Pequena alteração no layout do site pelo IMDB.
- **Solução:** Análise do HTML e correção do seletor CSS para uma versão mais robusta (`h1[data-testid='hero__pageTitle'] ~ ul`), resolvendo a extração dos metadados.

### Fase 3: Melhorias de Arquitetura e Observabilidade

- **Desafio:** Os artefatos do projeto (logs, planilhas) estavam sendo sobrescritos a cada execução.
- **Solução:** Foi implementada uma **arquitetura orientada por execução**. Agora, cada vez que o robô é executado, ele cria uma pasta única com data e hora no diretório `executions/`, que armazena de forma isolada todos os arquivos gerados naquela execução específica.
- **Evolução:** Foi adicionado um sumário ao final do log, informando o tempo total de execução, o número de filmes processados com sucesso e o número de falhas, melhorando a observabilidade do processo.

## 3. Próximos Passos e Melhorias Sugeridas

O projeto encontra-se em um estado estável e funcional, mas pode ser expandido com as seguintes melhorias:

1.  **Paralelismo com Gerenciamento de Proxies:** Para acelerar a extração em cenários de larga escala, a paralelização poderia ser implementada, desde que combinada com um serviço de proxies rotativos para evitar bloqueios de IP.
2.  **Armazenamento em Banco de Dados:** Substituir o salvamento em Excel por um banco de dados (como SQLite para simplicidade ou PostgreSQL para produção) para permitir consultas mais complexas e melhor gerenciamento dos dados.
3.  **Configuração Externa:** Mover parâmetros como a URL do IMDB e nomes de arquivos para um arquivo de configuração (`.env` ou `config.ini`) para facilitar a manutenção sem alterar o código.
4.  **Containerização com Docker:** Empacotar a aplicação em um contêiner Docker para garantir a portabilidade e simplificar o deploy em qualquer ambiente.
5.  **Interface Gráfica:** Desenvolver uma interface de usuário simples (com Tkinter ou Streamlit) para que usuários não técnicos possam executar o robô e acompanhar seu progresso.