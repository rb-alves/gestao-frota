from django import template

register = template.Library()

@register.filter
def to_decimal(valor):
    """
    Formata o valor como um número decimal sem separador de milhar
    e com ponto (.) como separador decimal.
    """
    try:
        # Converte o valor para float e formata com ponto como separador decimal
        valor_formatado = f"{float(valor):.2f}"
        return valor_formatado
    except (ValueError, TypeError):
        # Caso o valor não seja numérico, retorna um valor padrão
        return "0.00"
