import pandas as pd
import os
import logging
import json
import glob

logger = logging.getLogger(__name__)

class DataHandler:
    def __init__(self, execution_path):
        self.execution_path = execution_path
        self.initial_dir = os.path.join(execution_path, 'dados_extraidos')
        self.processed_dir = os.path.join(execution_path, 'dados_processados')
        self._create_directories()

    def _create_directories(self):
        try:
            os.makedirs(self.initial_dir, exist_ok=True)
            os.makedirs(self.processed_dir, exist_ok=True)
            logger.info("Diretórios de dados verificados/criados.")
        except OSError as e:
            logger.error("Falha ao criar diretórios de dados: %s", e)
            raise

    def save_single_movie_as_json(self, movie_data, file_id):
        """Salva os dados de um único filme em um arquivo JSON."""
        if not movie_data or not movie_data.get('Nome do filme'):
            logger.warning("Dados do filme inválidos ou sem nome, não será salvo.")
            return False
        
        filename = f"movie_{file_id}.json"
        filepath = os.path.join(self.initial_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(movie_data, f, ensure_ascii=False, indent=4)
            logger.debug(f"Dados do filme salvos em: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Falha ao salvar o arquivo JSON para o filme {movie_data.get('Nome do filme')}.", exc_info=True)
            return False

    def consolidate_json_to_excel(self, output_filename):
        """Lê todos os arquivos JSON, consolida e gera o Excel final."""
        json_pattern = os.path.join(self.initial_dir, '*.json')
        file_list = glob.glob(json_pattern)

        if not file_list:
            logger.warning("Nenhum arquivo JSON encontrado em 'dados_extraidos' para consolidar.")
            return

        all_movies_data = []
        for filepath in file_list:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    all_movies_data.append(json.load(f))
            except json.JSONDecodeError:
                logger.error(f"Erro ao ler o arquivo JSON: {filepath}. Pulando.")
        
        if not all_movies_data:
            logger.error("Nenhum dado válido foi carregado dos arquivos JSON.")
            return

        logger.info(f"Consolidando {len(all_movies_data)} arquivos de filme em uma planilha Excel.")
        df = pd.DataFrame(all_movies_data)
        
        excel_path = os.path.join(self.processed_dir, output_filename)
        try:
            df.to_excel(excel_path, index=False)
            logger.info(f"Planilha Excel final gerada com sucesso em: {excel_path}")
        except Exception as e:
            logger.error("Falha ao gerar o arquivo Excel final.", exc_info=True)