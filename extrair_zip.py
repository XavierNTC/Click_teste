import zipfile
from io import BytesIO
from comparador import arquivos_zip, extrair_codigo_zpl, extrair_nf

def processar_arquivos_zip(arquivos_zip):
    todos_conteudos_zpl = []

    for arquivo in arquivos_zip:
        if arquivo.type == "application/zip":
            with zipfile.ZipFile(arquivo) as z:
                for nome_arquivo in z.namelist():
                    if nome_arquivo.endswith('.zpl'):
                        with z.open(nome_arquivo) as zpl_file:
                            conteudo_bytes = zpl_file.read()
                            codigo = extrair_codigo_zpl(conteudo_bytes)
                            nf = extrair_nf(conteudo_bytes)
                            if codigo:
                                todos_conteudos_zpl.append({'codigo': codigo, 'fisco': nf})
    return todos_conteudos_zpl

#esse é de teste, pode excluir se quiser