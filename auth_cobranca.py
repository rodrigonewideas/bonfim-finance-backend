from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# Usuários hardcoded (ajuste aqui para o par correto)
USERS = {
    "rps": "cobranca"
    # se quiser outro, adicione: "cobranca": "bonfim2025@"
}

def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    print(f"\n=== DEBUG AUTENTICACAO ===")
    print(f"Usuário recebido: '{credentials.username}'")
    print(f"Senha recebida: '{credentials.password}'")
    print(f"Senha esperada (no dict): '{USERS.get(credentials.username)}'")
    print(f"Todos os usuários no dict: {USERS}")
    print("==========================\n")
    if credentials.username in USERS and USERS[credentials.username] == credentials.password:
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Basic"},
    )


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_password = USERS.get(credentials.username)
    # Usar comparação segura para evitar timing attack
    valid_user = correct_password is not None and secrets.compare_digest(credentials.password, correct_password)
    if valid_user:
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Basic"},
    )
def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    print(f"Usuário recebido: {credentials.username}")
    print(f"Senha recebida: {credentials.password}")
    if credentials.username in USERS and USERS[credentials.username] == credentials.password:
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Basic"},
    )
def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    print(f"Usuário recebido: {credentials.username}")
    print(f"Senha recebida: {credentials.password}")
    if credentials.username in USERS and USERS[credentials.username] == credentials.password:
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Basic"},
    )
