import logging
import os
from src.scraper import IMDBScraper
from src.data_handler import DataHandler

def setup_logging():
    LOG_DIR = 'log'
    LOG_FILENAME = 'rpa_execution.log'
    
    os.makedirs(LOG_DIR, exist_ok=True)
    
    log_path = os.path.join(LOG_DIR, LOG_FILENAME)
    
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_path, mode='w'),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("==============================================")
    logger.info("Iniciando o processo de RPA de extração do IMDB")
    logger.info("==============================================")
    
    IMDB_URL = "https://www.imdb.com/pt/chart/top/"
    FILENAME = "top_filmes_imdb.xlsx"

    scraper = IMDBScraper(IMDB_URL)
    data_handler = DataHandler()

    try:
        movies_data = scraper.scrape_movies()
        logger.info("Total de %d filmes extraídos com sucesso.", len(movies_data))
        
        if movies_data:
            initial_path = data_handler.save_to_excel(movies_data, FILENAME)
            
            if initial_path:
                success = data_handler.move_file_to_processed(initial_path)
                if success:
                    logger.info("Arquivo de dados movido para o diretório de processados.")
                else:
                    logger.error("A movimentação do arquivo de dados falhou.")
    
    except Exception as e:
        logger.critical("Ocorreu um erro não tratado na execução principal.", exc_info=True)

    finally:
        scraper.close_driver()
        logger.info("===================================")
        logger.info("Processo de RPA finalizado.")
        logger.info("===================================")

if __name__ == "__main__":
    main()