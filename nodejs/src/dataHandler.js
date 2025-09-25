const fs = require('fs/promises');
const path = require('path');
const ExcelJS = require('exceljs');

class DataHandler {
    constructor(executionPath, logger) {
        this.executionPath = executionPath;
        this.initialDir = path.join(executionPath, 'dados_extraidos');
        this.processedDir = path.join(executionPath, 'dados_processados');
        this.logger = logger.child({ service: 'DataHandler' });
        this._createDirectories();
    }

    async _createDirectories() {
        try {
            await fs.mkdir(this.initialDir, { recursive: true });
            await fs.mkdir(this.processedDir, { recursive: true });
            this.logger.info("Diretórios de dados verificados/criados.");
        } catch (error) {
            this.logger.error(`Falha ao criar diretórios de dados: ${error.message}`);
            throw error;
        }
    }

    async saveSingleMovieAsJson(movieData, fileId) {
        if (!movieData || !movieData['nome_filme']) {
            this.logger.warn("Dados do filme inválidos ou sem nome, não será salvo.");
            return false;
        }

        const filename = `movie_${fileId}.json`;
        const filepath = path.join(this.initialDir, filename);

        try {
            const jsonString = JSON.stringify(movieData, null, 4);
            await fs.writeFile(filepath, jsonString, 'utf-8');
            this.logger.debug(`Dados do filme salvos em: ${filepath}`);
            return true;
        } catch (error) {
            this.logger.error(`Falha ao salvar o arquivo JSON para o filme ${movieData['nome_filme']}: ${error.message}`);
            return false;
        }
    }

    async consolidateJsonToExcel(outputFilename) {
        let fileList;
        try {
            fileList = await fs.readdir(this.initialDir);
        } catch (error) {
            this.logger.error(`Não foi possível ler o diretório 'dados_extraidos': ${error.message}`);
            return;
        }

        const jsonFiles = fileList.filter(f => f.endsWith('.json'));

        if (jsonFiles.length === 0) {
            this.logger.warn("Nenhum arquivo JSON encontrado para consolidar.");
            return;
        }

        const allMoviesData = [];
        for (const file of jsonFiles) {
            const filepath = path.join(this.initialDir, file);
            try {
                const content = await fs.readFile(filepath, 'utf-8');
                allMoviesData.push(JSON.parse(content));
            } catch (error) {
                this.logger.error(`Erro ao ler o arquivo JSON: ${filepath}. Pulando.`);
            }
        }

        if (allMoviesData.length === 0) {
            this.logger.error("Nenhum dado válido foi carregado dos arquivos JSON.");
            return;
        }

        this.logger.info(`Consolidando ${allMoviesData.length} arquivos de filme em uma planilha Excel.`);
        
        const workbook = new ExcelJS.Workbook();
        const worksheet = workbook.addWorksheet('Top Filmes IMDB');

        worksheet.columns = Object.keys(allMoviesData[0]).map(key => ({
            header: key,
            key: key,
            width: key === 'nome_filme' ? 40 : (key === 'sinopse' ? 60 : 15)
        }));

        worksheet.addRows(allMoviesData);

        const excelPath = path.join(this.processedDir, outputFilename);
        try {
            await workbook.xlsx.writeFile(excelPath);
            this.logger.info(`Planilha Excel final gerada com sucesso em: ${excelPath}`);
        } catch (error) {
            this.logger.error(`Falha ao gerar o arquivo Excel final: ${error.message}`);
        }
    }
}

module.exports = DataHandler;