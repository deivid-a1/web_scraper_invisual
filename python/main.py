import logging
import os
import time 
from datetime import datetime
from src.scraper import IMDBScraper
from src.data_handler import DataHandler

def setup_logging():
    LOG_DIR = 'log'
    execution_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    LOG_FILENAME = f"rpa_execution_{execution_timestamp}.log"
    
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, LOG_FILENAME)
    
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_path, mode='w'),
            logging.StreamHandler()
        ],
        force=True 
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    start_time = time.time()
    movies_data = []
    total_links_found = 0
    
    logger.info("==============================================")
    logger.info("Iniciando o processo de RPA de extração do IMDB")
    logger.info("==============================================")
    
    IMDB_URL = "https://www.imdb.com/pt/chart/top/"
    FILENAME = "top_filmes_imdb.xlsx"

    scraper = None
    try:
        scraper = IMDBScraper(IMDB_URL)
        data_handler = DataHandler()
        
        movies_data, total_links_found = scraper.scrape_movies()
        
        if not movies_data:
            logger.warning("Nenhum dado de filme foi extraído. O processo terminará sem gerar arquivo.")
        else:
            logger.info("Total de %d filmes extraídos com sucesso.", len(movies_data))
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
        if scraper:
            scraper.close_driver()
        
        end_time = time.time()
        execution_time = end_time - start_time
        minutes, seconds = divmod(execution_time, 60)
        
        successful_scrapes = len(movies_data)
        failed_scrapes = total_links_found - successful_scrapes

        logger.info("===================================")
        logger.info("      SUMÁRIO DA EXECUÇÃO")
        logger.info("===================================")
        logger.info(f"Tempo total de execução: {int(minutes)} minutos e {seconds:.2f} segundos.")
        logger.info(f"Total de links encontrados: {total_links_found}")
        logger.info(f"Filmes processados com sucesso: {successful_scrapes}")
        logger.info(f"Falhas na extração: {failed_scrapes}")
        logger.info("===================================")
        logger.info("Processo de RPA finalizado.")
        logger.info("===================================")


if __name__ == "__main__":
    main()