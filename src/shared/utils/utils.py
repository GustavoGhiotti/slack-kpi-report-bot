
def indicador_percentual(valor):
    if valor >= 100:
        return "🔺", "#2eb67d"  # verde
    return "🔻", "#e01e5a"     # vermelho
