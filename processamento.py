def classificar_codigo(codigo):
    codigo_str = str(codigo)
    if codigo_str.startswith("45") or codigo_str.startswith("46") or codigo_str.startswith("47"):
        return "Mercado Livre"
    elif codigo_str.startswith("`^") or codigo_str.startswith("^") or codigo_str.startswith("id") or codigo_str.startswith("88"):
        return "Flex"
    else:
        return "Site"
