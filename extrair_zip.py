import zipfile
import re

def extrair_codigo_zpl(conteudo_bytes):
    try:
        conteudo = conteudo_bytes.decode('utf-8', errors='ignore')

        # Tenta extrair código de barras: ^FD>:45149061470^FS
        procurar_etiqueta = re.search(r"\^FD>:\s*(\d{10,})\^FS", conteudo)
        if procurar_etiqueta:
            return procurar_etiqueta.group(1)

        # Tenta extrair do QR Code JSON {"id":"45149061470","t":"lm"}
        procurar_qr = re.search(r'"id"\s*:\s*"(\d{10,})"', conteudo)
        if procurar_qr:
            return procurar_qr.group(1)

        return None
    except Exception:
        return None

def extrair_nf(conteudo_bytes):
    try:
        conteudo = conteudo_bytes.decode('utf-8', errors='ignore')
        procurar_nf = re.search(r"NF:\s*(\d+)", conteudo)
        if procurar_nf:
            return procurar_nf.group(1)
    except Exception:
        return None

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
