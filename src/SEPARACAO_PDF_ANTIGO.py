##############################################################################################################
# Esse arquivo está aqui somente para demonstração e registro histórico e não deve ser utilizado por nada nesse mundo.
# Ele foi substituído pelo arquivo src/SEPARACAO_PDF.py
##############################################################################################################

import PyPDF2  
import os
from pathlib import Path
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2 import PdfFileMerger
import glob, sys
import re

#DEFINE FUNÇÃO DE CONVERSÃO LIST --> STRING
def listToString(s):  
    
    # initialize an empty string 
    str1 = " " 
    
    # return string   
    return (str1.join(s)) 

#PEDE AO USUARIO A INSERÇÃO DO CAMINHO DA PASTA CONTENDO O UNICO PDF BRUTO DO LOTE
print("COLE O CAMINHO PARA A PASTA CONTENDO SOMENTE O PDF BRUTO A SER SEPARADO")
PastaPdf = input()

#PEDE AO USUARIO A INSERÇÃO DO CAMINHO DA PASTA DE SAIDA PARA TODOS OS PDFs
print("COLE O DIRETORIO DE SAIDA DOS PDFs RENOMEADOS !!!!!! O DIRETÓRIO DEVE ESTAR VAZIO !!!!!!")
Saida = input()

os.chdir(Saida)

pdfs = os.listdir(PastaPdf)

#SEPARA O PDF BRUTO EM PDFs UNICOS DE FRENTE E VERSO
for pdf in pdfs:
    inputFile = PdfFileReader(open(PastaPdf + "/" + pdf, "rb"))
    for i in range(inputFile.numPages // 2):
        output = PdfFileWriter()
        output.addPage(inputFile.getPage(i * 2))

        if i * 2 + 1 <  inputFile.numPages:
            output.addPage(inputFile.getPage(i * 2 + 1))

        newname = pdf[:30] + "-" + str(i) + ".pdf"

        outputStream = open(newname, "wb")
        output.write(outputStream)
        outputStream.close()

#ABRE OS PDFs DAS OFs GERADAS PELO FOCCO AS RENOMEIA COM O SEU RESPECTIVO CÓDIGO DE BARRAS
pastaLote = Saida
entries = Path(pastaLote)

print("DIGITE O NÚMERO DO LOTE")
NumLote = input()

pastaSaidaOrdem = str(r"C:/tmp/" + NumLote)



#CONFIRMA SE O DIRETORIO JA EXISTE
CHECK_FOLDER = os.path.isdir(pastaSaidaOrdem)

if not CHECK_FOLDER:
    os.makedirs(pastaSaidaOrdem)
    print("created folder : ", pastaSaidaOrdem)

else:
    print("PASTA TEMPORARIA JA EXISTENTE EM: ",pastaSaidaOrdem)





for entry in entries.iterdir():
    #print(entry.name)
    #print(str(pastaLote + entry.name))

    #Constroi o diretorio do PDF a ser aberto
    dirPdf = (str(pastaLote + "\\" + entry.name))

    # creating a pdf file object  
    pdfFileObj = open(str(pastaLote + "\\" + entry.name), 'rb')  

    # creating a pdf reader object  
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

    # creating a page object  
    pageObj = pdfReader.getPage(0)  

    # extracting text from page  
    pdfData = (pageObj.extractText()) 

    #Converte dados do pdf para string
    DataString = str(pdfData)
    #print(DataString)
    #procura o campo com *ORD no PDF e retorna sua posição
    posORD = DataString.find("*ORD")
    posPG = DataString.find("Página")
    #Calcula a localização do código de barras e num pg no PDF
    posiçãoInicialPG = posPG + 7
    posiçãoFinallPG = posPG + 11
    PdfPgBruto = (DataString[posiçãoInicialPG:posiçãoFinallPG])
    PdfPgList = re.findall('([0-9])',PdfPgBruto)
    PdfPg = str(PdfPgList)
    posiçãoInicial = posORD + 1
    posiçãoFinal = posORD + 11
    CodOrd = (DataString[posiçãoInicial:posiçãoFinal])

    # closing the pdf file object  
    pdfFileObj.close()
    
    #Recorta o PDF e cola da pasta C:tmp do windows 
    os.replace(dirPdf,str(pastaSaidaOrdem + "\\" + CodOrd + "_" +  PdfPg + ".pdf"))


#AGRUPA AS OFs COM MAIS DE UMA PAGINA E AS MOVE PARA A PASTA DE SAIDA
ListaSaida = os.listdir(pastaSaidaOrdem)
for eachPDF in ListaSaida:
    filemerger = PdfFileMerger()
    eachPDFINI = 0
    eachPDFEnd = 10
    eachPDFSubs = (eachPDF[eachPDFINI:eachPDFEnd])
    for PDF in ListaSaida:
        if PDF.startswith(eachPDFSubs):
            filemerger.append(pastaSaidaOrdem + "\\" + PDF)
    filemerger.write(eachPDFSubs + ".pdf")
    filemerger.close()






    



