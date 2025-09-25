const { Builder, By, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const fs = require('fs/promises');
const path = require('path');

class IMDBScraper {
    constructor(url, executionPath, logger) {
        this.url = url;
        this.executionPath = executionPath;
        this.debugDir = path.join(executionPath, 'debug');
        this.logger = logger.child({ service: 'Scraper' });
        this.driver = null;
        this.wait = null;
    }

    async init() {
        await fs.mkdir(this.debugDir, { recursive: true });
        this.driver = await this._setupDriver();
        this.wait = this.driver.wait.bind(this.driver);
    }

    async _setupDriver() {
        this.logger.info("Configurando o driver do Selenium via Selenium Manager (automático)...");

        let options = new chrome.Options();
        options.addArguments(
            "--start-maximized",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            '--lang=pt-BR',
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        );
        options.addArguments('--disable-blink-features=AutomationControlled');
        options.setAcceptInsecureCerts(true);
        options.excludeSwitches("enable-automation");
        
        const driver = await new Builder()
            .forBrowser('chrome')
            .setChromeOptions(options)
            .build();

        this.logger.info("Driver configurado com sucesso.");
        return driver;
    }

    async _saveDebugPageSource(contextName = "") {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `debug_page_${contextName}_${timestamp}.html`;
        const filepath = path.join(this.debugDir, filename);
        try {
            const pageSource = await this.driver.getPageSource();
            await fs.writeFile(filepath, pageSource, 'utf-8');
            this.logger.info(`Página de depuração salva em: ${filepath}`);
        } catch (error) {
            this.logger.error(`Não foi possível salvar a página de depuração: ${error.message}`);
        }
    }
    
    async _handleCookieBanner() {
        try {
            const cookieButtonXpath = "//button[contains(text(), 'Aceitar') or contains(text(), 'Accept')]"
            const cookieButton = await this.driver.wait(until.elementLocated(By.xpath(cookieButtonXpath)), 5000);
            await cookieButton.click();
            this.logger.info("Banner de cookies encontrado. Clicando no botão.");
            await this.driver.sleep(1000);
        } catch (error) {
            this.logger.info("Banner de cookies não foi encontrado ou já foi aceito.");
        }
    }

    async _handleLoginPopup() {
        try {
            const closeButtonSelector = "div[role='dialog'] label.ipc-btn";
            const closeButton = await this.driver.wait(until.elementLocated(By.css(closeButtonSelector)), 5000);
            await closeButton.click();
            this.logger.info("Pop-up de login encontrado. Clicando para fechar.");
            await this.driver.sleep(1000);
        } catch (error) {
            this.logger.info("Pop-up de login não foi encontrado.");
        }
    }

    async* scrapeMovies() {
        this.logger.info("Navegando para a URL principal e buscando links dos filmes.");
        await this.driver.get(this.url);
        await this._handleCookieBanner();

        let movieLinks = [];
        try {
            await this.driver.wait(until.elementsLocated(By.css("ul > li.ipc-metadata-list-summary-item")), 30000);
            const movieElements = await this.driver.findElements(By.css("ul > li.ipc-metadata-list-summary-item"));
            for (const movie of movieElements) {
                try {
                    const linkElement = await movie.findElement(By.css("div.ipc-title a"));
                    movieLinks.push(await linkElement.getAttribute('href'));
                } catch (error) {
                     this.logger.warn("Elemento de link não encontrado para um dos filmes. Pulando.");
                }
            }
             this.logger.info(`Encontrados ${movieLinks.length} links de filmes.`);
        } catch (error) {
             this.logger.error("Timeout ao carregar a lista de filmes na página principal.");
             await this._saveDebugPageSource("filmlist");
        }

        if (movieLinks.length === 0) {
            this.logger.error("Nenhum link de filme foi encontrado. Encerrando a extração.");
            return;
        }

        for (let i = 0; i < 2; i++) {
            this.logger.info(`Extraindo dados do filme ${i + 1} de ${movieLinks.length}...`);
            const details = await this._getMovieDetails(movieLinks[i]);
            yield details;
            await this.driver.sleep(Math.random() * 2000 + 1000);
        }
        this.logger.info("Processo de extração de dados finalizado.");
    }

    async _getMovieDetails(movieUrl) {
        await this.driver.get(movieUrl);
        // await this._handleCookieBanner();
        // await this._handleLoginPopup();

        let movieInfo = {
            'nome_filme': null, 'ano': null, 'duracao': null,
            'nota': null, 'sinopse': null
        };

        try {
            await this.driver.wait(until.elementLocated(By.css("[data-testid='hero__pageTitle']")), 30000);
        } catch (error) {
            this.logger.error(`Timeout ao esperar pelo título do filme em: ${movieUrl}`);
            await this._saveDebugPageSource("moviedetail");
            return null;
        }

        try { movieInfo['nome_filme'] = await this.driver.findElement(By.css("[data-testid='hero__pageTitle']")).getText(); } catch (e) { this.logger.warn(`Nome do filme não encontrado em ${movieUrl}`); }
        
        try {
            const metadataSelector = "h1[data-testid='hero__pageTitle'] ~ ul";
            const metadataList = await this.driver.findElement(By.css(metadataSelector));
            const metadataElements = await metadataList.findElements(By.tagName("li"));
            movieInfo['ano'] = await metadataElements[0].getText();
            const durationText = await metadataElements[metadataElements.length - 1].getText();
            
            let hours = 0, minutes = 0;
            if (durationText.includes('h')) {
                const parts = durationText.split('h');
                hours = parseInt(parts[0].trim());
                if (parts.length > 1 && parts[1].includes('min')) {
                    minutes = parseInt(parts[1].replace('min', '').trim());
                }
            } else if (durationText.includes('min')) {
                minutes = parseInt(durationText.replace('min', '').trim());
            }
            const durationList = [];
            if (hours > 0) durationList.push(`${hours}h`);
            if (minutes > 0) durationList.push(`${minutes}min`);
            movieInfo['duracao'] = durationList.join(' ');

        } catch (e) { this.logger.warn(`Ano ou duração não encontrados em ${movieUrl}`); }

        try { movieInfo['nota'] = await this.driver.findElement(By.css("[data-testid='hero-rating-bar__aggregate-rating__score'] > span")).getText(); } catch (e) { this.logger.warn(`Nota não encontrada em ${movieUrl}`); }
        try { movieInfo['sinopse'] = await this.driver.findElement(By.css("[data-testid='plot']")).getText(); } catch (e) { this.logger.warn(`Sinopse não encontrada em ${movieUrl}`); }

        this.logger.debug(`Detalhes extraídos para: ${movieInfo['nome_filme']}`);
        return movieInfo;
    }

    async closeDriver() {
        if (this.driver) {
            this.logger.info("Fechando o driver do navegador.");
            await this.driver.quit();
        }
    }
}

module.exports = IMDBScraper;