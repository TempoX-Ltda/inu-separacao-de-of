import os
import sys
import re
from pathlib import Path
import tempfile
import logging
from logging.handlers import RotatingFileHandler

from argparse import ArgumentParser

from pypdf import PdfReader, PdfWriter
__version__ = "1.1.0"


log_file = tempfile.gettempdir() + '/send_ardis.log'

formatter = logging.Formatter('%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_log_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)
file_log_handler.setLevel(logging.DEBUG)
file_log_handler.setFormatter(formatter)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)

logger.addHandler(file_log_handler)
logger.addHandler(stdout_handler)

logger.info('Arquivo de log: %s', log_file)

parser = ArgumentParser(
    prog='separacao_de_of',
    description='Recebe um PDF bruto de OF exportado do Focco e '
                'separa cada of num arquivo PDF próprio.'
)

parser.add_argument(
    '-v', '--version',
    action='version',
    version='%(prog)s ' + __version__
)

parser.add_argument(
    '--ord-regex',
    type=str,
    default=r'\*(ORD[^*]+)\*',
    help='Expressão regular para encontrar o código de barras da OF no texto extraído do PDF. '
         'O padrão é "%(default)s"',
)

parser.add_argument(
    '--lote-regex',
    type=str,
    default=r"LOTE (\S+)\n",
    help='Expressão regular para encontrar o código do lote no texto extraído do PDF. '
         'O padrão é "%(default)s"',
)


parser.add_argument(
    '-i', '--input-folder',
    type=Path,
    help='Diretório onde serão buscados todos os PDFs brutos de OFs exportados do Focco. '
         'Todos os PDFs existentes nessa pasta serão processados.',
    required=True
)

parser.add_argument(
    '-o', '--output-folder',
    type=Path,
    help='Diretório onde serão salvos os PDFs de OFs separados. ',
    required=True
)

args = parser.parse_args()

#SEPARA O PDF BRUTO EM PDFs UNICOS DE FRENTE E VERSO
for file in os.listdir(args.input_folder):
    logger.info('Processando o arquivo %s...', file)

    with open(args.input_folder / file, "rb") as f:
        pdf = PdfReader(f)

        pdf_page_qtd = len(pdf.pages)
        logger.info('Número de páginas: %s', pdf_page_qtd)

        for i in range(pdf_page_qtd // 2):
            logger.info('Processando a página %s...', i * 2)

            front_page = pdf.pages[i * 2]
            back_page = pdf.pages[i * 2 + 1]

            page_text = front_page.extract_text()

            try:
                codigo_ordem = re.search(args.ord_regex, page_text).group(1)
                logger.info('Código de barras da OF: %s', codigo_ordem)
            except AttributeError as exc:
                logger.error('Não foi possível encontrar o código de barras da OF no PDF %s.', file)
                raise RuntimeError from exc

            try:
                lote = re.search(args.lote_regex, page_text).group(1)
                logger.info('Código do lote: %s', lote)
            except AttributeError as exc:
                logger.error('Não foi possível encontrar o código do lote no PDF %s.', file)
                raise RuntimeError from exc

            # concatena a pasta de destino com o codigo do lote
            output_folder = args.output_folder / lote

            try:
                # cria a pasta de destino caso ela não exista
                output_folder.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                logger.error('Não foi possível criar a pasta de destino %s.', output_folder)
                raise RuntimeError from exc

            # cria o arquivo de saída
            output_file = output_folder / f'{codigo_ordem}.pdf'

            output_pdf = PdfWriter()
            output_pdf.add_page(front_page)
            output_pdf.add_page(back_page)

            with open(output_file, "wb") as outputStream:
                output_pdf.write(outputStream)

            logger.info('Arquivo %s criado com sucesso.', output_file)

    logger.info('Arquivo %s processado com sucesso.', file)

logger.info('Processamento finalizado com sucesso.')
