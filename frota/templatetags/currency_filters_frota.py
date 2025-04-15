import locale
from django import template

# Registra o filtro
register = template.Library()

# Tenta configurar o locale para o formato brasileiro
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    print("Locale pt_BR.UTF-8 não disponível. Usando o locale padrão.")
    locale.setlocale(locale.LC_ALL, '')  # Usa o locale padrão do sistema

@register.filter
def currency(value):
    """
    Formata um número como moeda brasileira (R$).
    """
    if value is None:
        return 'R$ 0,00'  # Valor padrão caso seja nulo
    try:
        return locale.currency(value, grouping=True)
    except Exception as e:
        print(f"Erro ao formatar valor como moeda: {e}")
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
