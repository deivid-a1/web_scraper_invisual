import logging
import time
import os
from datetime import datetime
from random import uniform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logger = logging.getLogger(__name__)

class IMDBScraper:
    def __init__(self, url):
        self.url = url
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 30)
        self.debug_dir = 'debug'
        os.makedirs(self.debug_dir, exist_ok=True)

    def _setup_driver(self):
        logger.info("Configurando o driver do Selenium em modo stealth (camuflado)...")
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })
        logger.info("Driver configurado com sucesso.")
        return driver

    def _save_debug_page_source(self, context_name=""):
        timestamp = datetime.now().strftime("%Y%m%d_%HM%S")
        filename = f"debug_page_{context_name}_{timestamp}.html"
        filepath = os.path.join(self.debug_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            logger.info(f"Página de depuração salva em: {filepath}")
        except Exception as e:
            logger.error(f"Não foi possível salvar a página de depuração: {e}")

    def _handle_cookie_banner(self):
        try:
            cookie_button_xpath = "//button[contains(text(), 'Aceitar') or contains(text(), 'Accept')]"
            cookie_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, cookie_button_xpath))
            )
            logger.info("Banner de cookies encontrado. Clicando no botão.")
            cookie_button.click()
            time.sleep(1)
        except TimeoutException:
            logger.info("Banner de cookies não foi encontrado ou já foi aceito.")

    def _handle_login_popup(self):
        try:
            close_button_selector = "div[role='dialog'] label.ipc-btn"
            close_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, close_button_selector))
            )
            logger.info("Pop-up de login encontrado. Clicando para fechar.")
            close_button.click()
            time.sleep(1)
        except TimeoutException:
            logger.info("Pop-up de login não foi encontrado.")
            
    def _get_movie_links(self):
        logger.info("Navegando para a URL principal e buscando links dos filmes.")
        self.driver.get(self.url)
        self._handle_cookie_banner()
        movie_links = []
        try:
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul > li.ipc-metadata-list-summary-item")))
            movie_elements = self.driver.find_elements(By.CSS_SELECTOR, "ul > li.ipc-metadata-list-summary-item")
            for movie in movie_elements:
                try:
                    link_element = movie.find_element(By.CSS_SELECTOR, "div.ipc-title a")
                    movie_links.append(link_element.get_attribute('href'))
                except NoSuchElementException:
                    logger.warning("Elemento de link não encontrado para um dos filmes. Pulando.")
            logger.info("Encontrados %d links de filmes.", len(movie_links))
        except TimeoutException:
            logger.error("Timeout ao carregar a lista de filmes na página principal.")
            self._save_debug_page_source("filmlist")
        return movie_links

    def _get_movie_details(self, movie_url):
        self.driver.get(movie_url)
        # self._handle_cookie_banner()
        # self._handle_login_popup()
        
        movie_info = {'Nome do filme': None, 'Ano': None, 'Duração': None, 'Nota': None, 'Sinopse': None}
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='hero__pageTitle']")))
        except TimeoutException:
            logger.error(f"Timeout ao esperar pelo título do filme em: {movie_url}")
            logger.debug(f"URL atual no momento do erro: {self.driver.current_url}")
            logger.debug(f"Título da página no momento do erro: '{self.driver.title}'")
            self._save_debug_page_source("moviedetail")
            return None
        
        try:
            movie_info['Nome do filme'] = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='hero__pageTitle']").text
        except NoSuchElementException: logger.warning("Nome do filme não encontrado em %s", movie_url)
        
        try:
            metadata_selector = "h1[data-testid='hero__pageTitle'] ~ ul"
            metadata_elements = self.driver.find_element(By.CSS_SELECTOR, metadata_selector).find_elements(By.TAG_NAME, "li")

            movie_info['Ano'] = metadata_elements[0].text
            duration_text = metadata_elements[-1].text
            hours, minutes = 0, 0
            if 'h' in duration_text:
                parts = duration_text.split('h')
                hours = int(parts[0].strip())
                if len(parts) > 1 and 'min' in parts[1]: minutes = int(parts[1].replace('min', '').strip())
            elif 'min' in duration_text: minutes = int(duration_text.replace('min', '').strip())
            duration_list = []
            if hours > 0: duration_list.append(f"{hours}h")
            if minutes > 0: duration_list.append(f"{minutes}min")
            movie_info['Duração'] = " ".join(duration_list)
        except (NoSuchElementException, IndexError): logger.warning("Ano ou duração não encontrados em %s", movie_url)
        
        try:
            rating_element = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='hero-rating-bar__aggregate-rating__score'] > span")
            movie_info['Nota'] = rating_element.text.split('/')[0]
        except NoSuchElementException: logger.warning("Nota não encontrada em %s", movie_url)
        try:
            synopsis_element = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='plot-l']")
            movie_info['Sinopse'] = synopsis_element.text
        except NoSuchElementException: logger.warning("Sinopse não encontrada em %s", movie_url)
        
        logger.debug(f"Detalhes extraídos para: {movie_info.get('Nome do filme')}")
        return movie_info

    def scrape_movies(self):
        logger.info("Iniciando processo de extração de dados dos filmes.")
        movie_links = self._get_movie_links()
        total_links = len(movie_links)
        all_movies_data = []

        if not movie_links:
            logger.error("Nenhum link de filme foi encontrado. Encerrando a extração.")
            return [], total_links 
        
        for i, link in enumerate(movie_links):
            logger.info(f"Extraindo dados do filme {i + 1} de {len(movie_links)}...")
            details = self._get_movie_details(link)
            if details:
                all_movies_data.append(details)
            time.sleep(uniform(1, 3))
            
        logger.info("Processo de extração de dados finalizado.")
        return all_movies_data, total_links

    def close_driver(self):
        if self.driver:
            logger.info("Fechando o driver do navegador.")
            self.driver.quit()