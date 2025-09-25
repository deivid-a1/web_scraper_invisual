import logging
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
        self.wait = WebDriverWait(self.driver, 15)

    def _setup_driver(self):
        logger.info("Configurando o driver do Selenium...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Driver configurado com sucesso.")
        return driver

    def _get_movie_links(self):
        logger.info("Navegando para a URL principal e buscando links dos filmes.")
        self.driver.get(self.url)
        movie_links = []
        try:
            movie_elements = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul > li.ipc-metadata-list-summary-item")))
            for movie in movie_elements:
                try:
                    link_element = movie.find_element(By.CSS_SELECTOR, "div.ipc-title a")
                    movie_links.append(link_element.get_attribute('href'))
                except NoSuchElementException:
                    logger.warning("Elemento de link não encontrado para um dos filmes. Pulando.")
                    continue
            logger.info("Encontrados %d links de filmes.", len(movie_links))
        except TimeoutException:
            logger.error("Timeout: Não foi possível carregar a lista de filmes na página principal.")
        return movie_links

    def _get_movie_details(self, movie_url):
        self.driver.get(movie_url)
        movie_info = {}
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='hero-title-block__title']")))
            
            movie_info['Nome do filme'] = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='hero-title-block__title']").text
            
            metadata_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='hero-title-block__metadata'] ul > li")
            movie_info['Ano'] = metadata_elements[0].text
            
            duration_text = metadata_elements[-1].text
            hours = 0
            minutes = 0
            if 'h' in duration_text:
                parts = duration_text.split('h')
                hours = int(parts[0].strip())
                if 'min' in parts[1]:
                    minutes = int(parts[1].replace('min', '').strip())
            elif 'min' in duration_text:
                minutes = int(duration_text.replace('min', '').strip())
            
            duration_list = []
            if hours > 0:
                duration_list.append(f"{hours}h")
            if minutes > 0:
                duration_list.append(f"{minutes}min")
            movie_info['Duração'] = " ".join(duration_list)

            rating_element = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='hero-rating-bar__aggregate-rating__score'] > span")
            movie_info['Nota'] = rating_element.text.split('/')[0]
            
            synopsis_element = self.driver.find_element(By.CSS_SELECTOR, "p > [data-testid='plot-xl']")
            movie_info['Sinopse'] = synopsis_element.text
            
            logger.debug("Detalhes extraídos para: %s", movie_info.get('Nome do filme'))

        except (NoSuchElementException, TimeoutException, IndexError) as e:
            logger.error("Não foi possível extrair todos os detalhes da URL %s: %s", movie_url, e)
            return None
        return movie_info

    def scrape_movies(self):
        logger.info("Iniciando processo de extração de dados dos filmes.")
        self.driver.get("https://www.google.com.br")
        movie_links = self._get_movie_links()
        all_movies_data = []
        for i, link in enumerate(movie_links):
            logger.info("Extraindo dados do filme %d de %d...", i + 1, len(movie_links))
            details = self._get_movie_details(link)
            if details:
                all_movies_data.append(details)
        logger.info("Processo de extração de dados finalizado.")
        return all_movies_data

    def close_driver(self):
        if self.driver:
            logger.info("Fechando o driver do navegador.")
            self.driver.quit()