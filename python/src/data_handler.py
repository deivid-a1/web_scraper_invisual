import pandas as pd
import os
import shutil
import logging

logger = logging.getLogger(__name__)

class DataHandler:
    def __init__(self, initial_dir='dados_extraidos', processed_dir='dados_processados'):
        self.initial_dir = initial_dir
        self.processed_dir = processed_dir
        self._create_directories()

    def _create_directories(self):
        try:
            os.makedirs(self.initial_dir, exist_ok=True)
            os.makedirs(self.processed_dir, exist_ok=True)
            logger.info("Diretórios '%s' e '%s' verificados/criados.", self.initial_dir, self.processed_dir)
        except OSError as e:
            logger.error("Falha ao criar diretórios: %s", e)
            raise

    def save_to_excel(self, data, filename):
        if not data:
            logger.warning("Nenhum dado fornecido para salvar no Excel.")
            return None
        
        df = pd.DataFrame(data)
        file_path = os.path.join(self.initial_dir, filename)
        
        try:
            df.to_excel(file_path, index=False)
            logger.info("Dados salvos com sucesso em: %s", file_path)
            return file_path
        except Exception as e:
            logger.error("Falha ao salvar o arquivo Excel em %s.", file_path, exc_info=True)
            return None

    def move_file_to_processed(self, source_path):
        if not source_path or not os.path.exists(source_path):
            logger.error("Arquivo de origem não encontrado para movimentação: %s", source_path)
            return False
            
        filename = os.path.basename(source_path)
        destination_path = os.path.join(self.processed_dir, filename)
        
        try:
            shutil.move(source_path, destination_path)
            logger.info("Arquivo movido de '%s' para '%s'.", source_path, destination_path)
            return True
        except Exception as e:
            logger.error("Falha ao mover o arquivo para o destino: %s", destination_path, exc_info=True)
            return False