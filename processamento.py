def classificar_codigo(codigo):
    codigo_str = str(codigo)
    if codigo_str.startswith("45"):
        return "Mercado Livre"
    elif codigo_str.startswith("`^") or codigo_str.startswith("^") or codigo_str.startswith("id"):
        return "Flex"
    else:
        return "Site"
