import re
from core.pattern_loader import TaskField, get_task_field

def normalize_task_text(text: str) -> str:
    """
    Remove prefixos de tarefas (ex: 'Tenho um pendente para') do início do texto
    e limpa espaços extras.
    """
    if not text:
        return ""

    # 1. Vai buscar a lista de prefixos dinamicamente do YAML via Enum
    prefixes = get_task_field(TaskField.PREFIXES)
    
    # Texto original limpo de espaços nas pontas
    normalized = text.strip()

    # 2. Ordena os prefixos pelo tamanho (maior primeiro) para evitar que 
    # um prefixo menor quebre um maior (ex: "tenho" vs "tenho um pendente para")
    sorted_prefixes = sorted(prefixes, key=len, reverse=True)

    # 3. Varre os prefixos e remove se o texto começar com algum deles
    for prefix in sorted_prefixes:
        # Usamos re.escape para o caso de haver caracteres especiais no prefixo
        # re.IGNORECASE garante que "Tenho" ou "tenho" funcionem igual
        pattern = rf"^{re.escape(prefix)}\s*"
        
        # Se encontrar o prefixo no início, remove-o
        if re.match(pattern, normalized, re.IGNORECASE):
            normalized = re.sub(pattern, "", normalized, flags=re.IGNORCASE)
            break # Remove apenas o primeiro prefixo correspondente

    return normalized.strip()