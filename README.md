# Separação de OF
Separação de ordens de fabricação do Focco


```sh
> SEPARACAO_PDF.exe -h
usage: separacao_de_of [-h] [-v] [--ord-regex ORD_REGEX] [--lote-regex LOTE_REGEX] -i INPUT_FOLDER -o OUTPUT_FOLDER

Recebe um PDF bruto de OF exportado do Focco e separa cada of num arquivo PDF próprio.

options:
  -h, --help            show this help message and exit
  -v, --version         show program version number and exit
  --ord-regex ORD_REGEX
                        Expressão regular para encontrar o código de barras da OF no texto extraído do PDF. O padrão é "\*(ORD[^*]+)\*"
  --lote-regex LOTE_REGEX
                        Expressão regular para encontrar o código do lote no texto extraído do PDF. O padrão é "LOTE (\S+)\n"
  -i INPUT_FOLDER, --input-folder INPUT_FOLDER
                        Diretório onde serão buscados todos os PDFs brutos de OFs exportados do Focco. Todos os PDFs existentes nessa pasta serão processados.
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        Diretório onde serão salvos os PDFs de OFs separados.

```

O código da ordem (ORD) e o Lote são extraídos da página do PDF através de regex, que podem ser passados através dos parâmetros `--ord-regex` e `--lote-regex`. O programa já possui valores padrões para esses parâmetros (que pode ser visualizados com `SEPARACAO_PDF.exe -h`).

O código do lote é utilizado para definir a pasta onde os PDFS separados serão salvos, portanto se `--output-folder C:/pdfs-separados`, e uma ordem tiver o lote `4936` e ORD `ORD123456789`, então o PDF será salvo na pasta `C:/pdfs-separados/4936/ORD123456789.pdf`.

Serão processados TODOS os arquivos `.pdf` que estiverem na `--input-folder`

O código assume que o arquivo bruto SEMPRE irá possuir 2 páginas (frente e verso) para um ordem, portanto para um arquivo bruto com 3 ordems (6 páginas), será gerado 3 PDFs separados:
- Ordem 1 (pag 1 e 2 do arquivo original)
- Ordem 2 (pag 3 e 4 do arquivo original)
- Ordem 3 (pag 5 e 6 do arquivo original)