try {
    const seleniumInfo = require('selenium-webdriver/package.json');
    console.log(`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
[VERIFICAÇÃO] Versão do selenium-webdriver em execução: ${seleniumInfo.version}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
`);
} catch (e) {
    console.log(`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
[VERIFICAÇÃO] ERRO: Não foi possível encontrar o selenium-webdriver.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
`);

}
const fs = require('fs');
const path = require('path');
const { setupLogger } = require('./src/logger');
const DataHandler = require('./src/dataHandler');
const IMDBScraper = require('./src/scraper');

async function main() {
    const baseExecutionsDir = 'executions';
    const executionTimestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const currentExecutionPath = path.join(baseExecutionsDir, `run_${executionTimestamp}`);
    fs.mkdirSync(currentExecutionPath, { recursive: true });

    const logger = setupLogger(currentExecutionPath);

    const startTime = Date.now();
    let successfulScrapes = 0;
    let failedScrapes = 0;

    logger.info("==============================================");
    logger.info("Iniciando o processo de RPA de extração do IMDB");
    logger.info(`Diretório da execução: ${currentExecutionPath}`);
    logger.info("==============================================");

    const IMDB_URL = "https://www.imdb.com/pt/chart/top/";
    const FILENAME = "top_filmes_imdb.xlsx";

    const scraper = new IMDBScraper(IMDB_URL, currentExecutionPath, logger);
    let dataHandler;

    try {
        await scraper.init();
        dataHandler = new DataHandler(currentExecutionPath, logger);
        
        let fileId = 1;
        for await (const movieData of scraper.scrapeMovies()) {
            if (movieData) {
                await dataHandler.saveSingleMovieAsJson(movieData, fileId++);
                successfulScrapes++;
            } else {
                failedScrapes++;
            }
        }
        
        await dataHandler.consolidateJsonToExcel(FILENAME);

    } catch (error) {
        logger.error(`Ocorreu um erro não tratado na execução principal: ${error.message}`, { stack: error.stack });
    } finally {
        await scraper.closeDriver();

        const endTime = Date.now();
        const executionTime = (endTime - startTime) / 1000; // em segundos
        const minutes = Math.floor(executionTime / 60);
        const seconds = (executionTime % 60).toFixed(2);
        
        const totalProcessed = successfulScrapes + failedScrapes;

        logger.info("===================================");
        logger.info("      SUMÁRIO DA EXECUÇÃO");
        logger.info("===================================");
        logger.info(`Tempo total de execução: ${minutes} minutos e ${seconds} segundos.`);
        logger.info(`Total de filmes processados: ${totalProcessed}`);
        logger.info(`Salvos com sucesso (JSON individual): ${successfulScrapes}`);
        logger.info(`Falhas na extração: ${failedScrapes}`);
        logger.info(`Artefatos salvos em: ${currentExecutionPath}`);
        logger.info("===================================");
        logger.info("Processo de RPA finalizado.");
        logger.info("===================================");
    }
}

main();