# Localização: /main.py
import logging
import os
import time
from datetime import datetime
from src.scraper import IMDBScraper
from src.data_handler import DataHandler

def setup_logging(execution_path):
    log_dir = os.path.join(execution_path, 'log')
    os.makedirs(log_dir, exist_ok=True)
    log_filename = 'execution.log'
    log_path = os.path.join(log_dir, log_filename)
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[logging.FileHandler(log_path, mode='w'), logging.StreamHandler()],
        force=True 
    )

def main():
    base_executions_dir = 'executions'
    execution_timestamp = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")
    current_execution_path = os.path.join(base_executions_dir, execution_timestamp)
    os.makedirs(current_execution_path, exist_ok=True)
    
    setup_logging(current_execution_path)
    logger = logging.getLogger(__name__)

    start_time = time.time()
    successful_scrapes = 0
    failed_scrapes = 0
    
    logger.info("==============================================")
    logger.info("Iniciando o processo de RPA de extração do IMDB")
    logger.info(f"Diretório da execução: {current_execution_path}")
    logger.info("==============================================")
    
    IMDB_URL = "https://www.imdb.com/pt/chart/top/"
    FILENAME = "top_filmes_imdb.xlsx"

    scraper = None
    try:
        scraper = IMDBScraper(url=IMDB_URL, execution_path=current_execution_path)
        data_handler = DataHandler(execution_path=current_execution_path)
        
        # O método scrape_movies é um gerador, processamos um filme por vez
        for i, movie_data in enumerate(scraper.scrape_movies()):
            if movie_data:
                data_handler.save_single_movie_as_json(movie_data, file_id=i+1)
                successful_scrapes += 1
            else:
                failed_scrapes += 1
        
        # Após o loop, consolida os arquivos JSON salvos em um único Excel
        data_handler.consolidate_json_to_excel(FILENAME)
    
    except Exception as e:
        logger.critical("Ocorreu um erro não tratado na execução principal.", exc_info=True)

    finally:
        if scraper:
            scraper.close_driver()
        
        end_time = time.time()
        execution_time = end_time - start_time
        minutes, seconds = divmod(execution_time, 60)
        
        total_processed = successful_scrapes + failed_scrapes

        logger.info("===================================")
        logger.info("      SUMÁRIO DA EXECUÇÃO")
        logger.info("===================================")
        logger.info(f"Tempo total de execução: {int(minutes)} minutos e {seconds:.2f} segundos.")
        logger.info(f"Total de filmes processados: {total_processed}")
        logger.info(f"Salvos com sucesso (JSON individual): {successful_scrapes}")
        logger.info(f"Falhas na extração: {failed_scrapes}")
        logger.info(f"Artefatos salvos em: {current_execution_path}")
        logger.info("===================================")
        logger.info("Processo de RPA finalizado.")
        logger.info("===================================")

if __name__ == "__main__":
    main()