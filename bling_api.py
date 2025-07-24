import requests
import base64
import json
import os
import time  # Para simular verificação de expiração do token

# --- Credenciais Bling ---
# ATENÇÃO: Substitua pelos seus CLIENT_ID e CLIENT_SECRET reais do Bling.
# Mantenha-os seguros e não os compartilhe publicamente.
CLIENT_ID = "65ff897a8541bf0a8700a8e83095d28b271e1a4a"
CLIENT_SECRET = "65dfda765417138df6eaafe8c455395aeaabb23d01d5d7daa1542a350402"
REDIRECT_URI = "http://localhost:8501"  # Deve ser o mesmo configurado no seu app Bling

# --- Endpoints da API Bling ---
TOKEN_URL = "https://www.bling.com.br/Api/v3/oauth/token"
BASE_API_V3_URL = "https://api.bling.com.br/v3"

# --- Configuração do Token Local ---
TOKEN_FILE_PATH = "bling_token.json"  # Onde o token será salvo localmente


def _save_token(token_data: dict):
    """Salva os dados do token (access_token, expires_in, etc.) em um arquivo JSON."""
    # Adiciona um timestamp para controlar a expiração
    token_data['timestamp'] = time.time()
    with open(TOKEN_FILE_PATH, "w") as f:
        json.dump(token_data, f, indent=4)
    print(f"✅ Token salvo em '{TOKEN_FILE_PATH}'.")


def _load_token():
    """Carrega os dados do token de um arquivo JSON."""
    if os.path.exists(TOKEN_FILE_PATH):
        try:
            with open(TOKEN_FILE_PATH, "r") as f:
                token_data = json.load(f)
            print(f"✅ Token carregado de '{TOKEN_FILE_PATH}'.")
            return token_data
        except json.JSONDecodeError:
            print(f"⚠️ Erro ao decodificar '{TOKEN_FILE_PATH}'. O arquivo pode estar corrompido.")
            os.remove(TOKEN_FILE_PATH)
            return None
    return None


def _is_token_expired(token_data: dict) -> bool:
    """Verifica se o token de acesso expirou."""
    if not token_data or 'access_token' not in token_data or 'expires_in' not in token_data or 'timestamp' not in token_data:
        return True  # Dados insuficientes para verificar expiração

    # O Bling geralmente retorna expires_in em segundos (ex: 3600 para 1 hora)
    # Subtraímos uma margem de segurança (ex: 300 segundos = 5 minutos)
    expires_at = token_data['timestamp'] + token_data['expires_in'] - 300  # Margem de 5 minutos
    return time.time() >= expires_at


def get_access_token(auth_code: str = None) -> str:
    """
    Obtém um token de acesso válido para a API do Bling.
    Prioriza carregar um token salvo se for válido.
    Caso contrário, usa um código de autorização para obter um novo token.
    """
    token_data = _load_token()

    if token_data and not _is_token_expired(token_data):
        print("✅ Token existente ainda válido. Reutilizando...")
        return token_data['access_token']

    print("🔑 Token inexistente ou expirado. Tentando obter um novo...")

    if not auth_code:
        raise Exception("⚠️ Código de autorização não fornecido. Necessário para obter um novo token.")

    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_client_creds = base64.b64encode(client_creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_client_creds}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }

    print(f"📞 Enviando requisição para obter novo token de: {TOKEN_URL}")
    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    if response.status_code == 200:
        new_token_data = response.json()
        _save_token(new_token_data)
        print("✅ Novo token de acesso obtido com sucesso!")
        return new_token_data["access_token"]
    else:
        print(f"❌ Erro ao obter token: Status {response.status_code}")
        print(f"   Detalhes do erro: {response.text}")
        raise Exception(f"Erro ao obter token: {response.status_code} - {response.text}")


def generate_authorization_url() -> str:
    """Gera a URL para o usuário autorizar o aplicativo no Bling."""
    return (
        f"https://www.bling.com.br/Api/v3/oauth/authorize?"
        f"response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state=xyz123"
    )


def _make_api_request(endpoint: str, access_token: str) -> dict:
    """Função auxiliar para fazer requisições GET à API Bling."""
    url = f"{BASE_API_V3_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    print(f"\n📞 Tentando acessar URL: {url}")
    print(f"   Com Headers: {headers.get('Authorization')[:30]}...")  # Evitar imprimir token completo

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro na consulta de '{endpoint}' - Status: {response.status_code}")
        print(f"   Corpo da resposta de erro: {response.text}")
        raise Exception(f"Erro na consulta de '{endpoint}': {response.status_code} - {response.text}")


def list_products(access_token: str) -> dict:
    """Lista os produtos da sua conta Bling."""
    print("--- 🔍 Consultando Produtos ---")
    return _make_api_request("produtos", access_token)


def list_orders(access_token: str) -> dict:
    """Lista os pedidos da sua conta Bling."""
    print("--- 🔍 Consultando Pedidos ---")
    return _make_api_request("pedidos", access_token)