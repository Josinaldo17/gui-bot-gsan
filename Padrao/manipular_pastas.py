import os

def verificar_e_criar_pasta(caminho, criar):
    """
    Verifica se a pasta existe.
    Se não existir e criar=True, cria a pasta.
    Retorna (existe, criado):
      - existe: True se já existia
      - criado: True se foi criada agora
    """
    if os.path.exists(caminho) and os.path.isdir(caminho):
        return True, False  # já existia, não criou

    if not criar:
        return False, False  # não existia, não criou

    os.makedirs(caminho)
    # print(f'Pasta criada: {caminho}')
    return False, True  # não existia, mas foi criada


def verificar_e_criar_arquivo(caminho, criar):
    """
    Verifica se o arquivo existe.
    Se não existir e criar=True, cria o arquivo (e a pasta pai, se necessário).
    Retorna (existe, criado):
      - existe: True se já existia
      - criado: True se foi criado agora
    """
    if os.path.exists(caminho) and os.path.isfile(caminho):
        return True, False  # já existia, não criou

    if not criar:
        return False, False  # não existia, não criou

    # Cria pasta pai se necessário
    pasta_pai = os.path.dirname(caminho)
    if pasta_pai and not os.path.exists(pasta_pai):
        os.makedirs(pasta_pai)
        # print(f'Pasta pai criada: {pasta_pai}')
    
    with open(caminho, 'w') as f:
        pass
    # print(f'Arquivo criado: {caminho}')
    return False, True  # não existia, mas foi criado