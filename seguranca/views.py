from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib import messages
from .models import Multa, Ocorrido
from colaboradores.models import Colaborador
from frota.models import Veiculo, CentroCusto
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

def formataValor(valor):
    """
    Converte um valor monetário no formato brasileiro para um float.
    Retorna None para valores vazios ou inválidos.
    """
    if not valor or valor.strip() == "R$":
        return None  # Retorna None se o valor for vazio ou apenas o prefixo "R$"
    
    try:
        # Remove "R$ ", pontos de milhar e substitui a vírgula decimal por ponto
        valor = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(valor)
    except ValueError:
        # Retorna None se a conversão falhar
        return None



# Lista todas as multas cadastradas no banco de dados passandos os contextos necessarios para o template
@login_required
def ListaMultas(request):
    multas = Multa.objects.all().order_by("-id")
    
    # Inicializa as variáveis do filtro como vazias
    data_inicial = ""
    data_final = ""
    gravidade = ""
    situacao = ""
    infracao = ""
    valor_multa = ""
    data_vencimento_inicial = ""
    data_vencimento_final = ""
    colaborador = ""
    veiculo = ""
    centro_custo = ""
    descricao = ""
    
    # Verifica se existe uma requisição tipo POST para aplicar os filtros
    if request.method == "POST":
        situacao = request.POST.get("filtro-situacao_multa", "")
        if situacao:
            multas = multas.filter(situacao_multa=situacao)

        data_inicial = request.POST.get("filtro-dataInfracaoInicial", "")
        if data_inicial:
            multas = multas.filter(data_infracao__gte=data_inicial)

        data_final = request.POST.get("filtro-dataInfracaoFinal", "")
        if data_final:
            multas = multas.filter(data_infracao__lte=data_final)

        gravidade = request.POST.get("filtro-gravidade", "")
        if gravidade:
            multas = multas.filter(gravidade=gravidade)

        valor_multa = request.POST.get("filtro-valorMulta", "")
        valor_multa = formataValor(valor_multa)  # Converte o valor monetário
        if valor_multa is not None:  # Apenas filtra se o valor for válido
            multas = multas.filter(valor=valor_multa)

        data_vencimento_inicial = request.POST.get("filtro-dataVencimentoInicial", "")
        if data_vencimento_inicial:
            multas = multas.filter(data_vencimento__gte=data_vencimento_inicial)

        data_vencimento_final = request.POST.get("filtro-dataVencimentoFinal", "")
        if data_vencimento_final:
            multas = multas.filter(data_vencimento__lte=data_vencimento_final)

        infracao = request.POST.get("filtro-infracao", "")
        if infracao:
            multas = multas.filter(auto_infracao__icontains=infracao)

        colaborador = request.POST.get("filtro-colaborador", "")
        if colaborador:
            colaborador = int(colaborador)
            multas = multas.filter(colaborador=colaborador)

        veiculo = request.POST.get("filtro-veiculo", "")
        if veiculo:
            veiculo = int(veiculo)
            multas = multas.filter(veiculo=veiculo)

        centro_custo = request.POST.get("filtro-centro_custo", "")
        if centro_custo:
            centro_custo = int(centro_custo)
            multas = multas.filter(centro_custo=centro_custo)

        descricao = request.POST.get("filtro-descricao", "")
        if descricao:
            multas = multas.filter(descricao__icontains=descricao)
    
    # Valores para os cards de resumo
    qtd_pago = multas.filter(situacao_multa="Pago").count()
    qtd_a_pagar = multas.filter(situacao_multa="A Pagar").count()
    qtd_recorrendo = multas.filter(situacao_multa="Recorrendo").count()
    qtd_anulada = multas.filter(situacao_multa="Anulada").count()
    valor_total = multas.aggregate(total=Sum('valor'))['total'] or 0

    # Resolvidas e Pendentes
    total_resolvidas = qtd_pago + qtd_anulada
    total_pendentes = qtd_a_pagar + qtd_recorrendo

    # Contexto para Multas
    gravidades = Multa._meta.get_field("gravidade").choices
    situacoes = Multa._meta.get_field("situacao_multa").choices
    colaboradores = Colaborador.objects.all().filter(situacao="Ativo")
    veiculos = Veiculo.objects.all().filter(situacao="Ativo")
    centros = CentroCusto.objects.all().order_by("descricao")
    
    return render(
        request,
        "seguranca/multas/lista_multas.html",
        {
            "multas": multas,
            "colaboradores": colaboradores,
            "veiculos": veiculos,
            "centros": centros,
            "gravidades": gravidades,
            "situacoes": situacoes,
            "filtro_situacao": situacao,
            "filtro_data_inicial": data_inicial,
            "filtro_data_final": data_final,
            "filtro_gravidade": gravidade,
            "filtro_valor_multa": valor_multa,
            "filtro_data_vencimento_inicial": data_vencimento_inicial,
            "filtro_data_vencimento_final": data_vencimento_final,
            "filtro_infracao": infracao,
            "filtro_colaborador": colaborador,
            "filtro_veiculo": veiculo,
            "filtro_centro_custo": centro_custo,
            "filtro_descricao": descricao,
            "total_pendentes": total_pendentes,
            "total_resolvidas": total_resolvidas,
            "valor_total": valor_total
        },
    )


# Cadastra uma nova Multa
def novaMulta(request):
    # Verifica se o metodo de requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores enviados pelo formulário
        data_infracao = request.POST.get("dataInfracao")
        hora_infracao = request.POST.get("horaInfracao")
        auto_infracao = request.POST.get("infracao").upper()
        gravidade = request.POST.get("gravidade")
        data_vencimento = request.POST.get("dataVencimento")
        colaborador = request.POST.get("colaborador")
        veiculo = request.POST.get("veiculo")
        centro_custo = request.POST.get("centro_custo")
        descricao = request.POST.get("descricao").upper()

        valor = request.POST.get("valorMulta")
        # Trata o valor monetario enviado pelo formulario
        try:
            # Substitui "R$" por Vazio "", Substitui "." por Vazio, Substitui "," por "." e retira os espaços desnecessários
            valor = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
            valor_tratado = float(valor)
        except ValueError:
            return HttpResponseBadRequest("O valor da multa fornecido não é valido!")



        # Buscar os objetos colaborador, veiculo e centro_custo pelos IDs fornecidos em suas respectivas tabelas
        colaborador = Colaborador.objects.get(id=colaborador)
        veiculo = Veiculo.objects.get(id=veiculo)
        centro_custo = CentroCusto.objects.get(id=centro_custo)

        # Tenta realizar o cadastro da multa
        try:
            # Registar uma nova multa no banco de dados
            cadastrar_multa = Multa(
                data_infracao = data_infracao,
                hora_infracao = hora_infracao,
                auto_infracao = auto_infracao,
                gravidade = gravidade,
                valor = valor_tratado,
                data_vencimento = data_vencimento,
                colaborador = colaborador,
                veiculo = veiculo,
                centro_custo = centro_custo,
                descricao = descricao
            )

            # Salva o novo registro no banco de dados
            cadastrar_multa.save()
            messages.success(request, "A multa foi cadastrada com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao cadastrar a multa: {str(e)}")

        # Retorna a lista de multas em caso de sucesso ou fracasso
        return redirect("lista_multas")
    


#Edita uma multa no banco de dados
def editarMulta(request, multa_id):
    # A função get_object_or_404 possui dois argumentos (TABELA DO BANCO E ID)
    # Caso a função encontre o ID na tabela o registro é retornado, caso o ID não seja encontrado ocorrera um erro 404
    multa =  get_object_or_404(Multa, pk=multa_id)

    # Variaveis usadas para passar contexto para o template
    colaboradores = Colaborador.objects.all().order_by("nome")
    veiculos = Veiculo.objects.all().order_by("placa")
    centros = CentroCusto.objects.all().order_by("descricao")
    gravidades = Multa._meta.get_field("gravidade").choices
    situacoes = Multa._meta.get_field("situacao_multa").choices

    # Verifica se a requisição é do tipo POST
    if request.method == 'POST':
         # Recupera os valores enviados pelo formulário
        data_infracao = request.POST.get("dataInfracao")
        hora_infracao = request.POST.get("horaInfracao")
        auto_infracao = request.POST.get("infracao").upper()
        gravidade = request.POST.get("gravidade")
        data_vencimento = request.POST.get("dataVencimento")
        situacao_multa = request.POST.get("situacao_multa")
        colaborador = request.POST.get("colaborador")
        veiculo = request.POST.get("veiculo")
        centro_custo = request.POST.get("centro_custo")
        descricao = request.POST.get("descricao").upper()

        valor = request.POST.get("valorMulta")
        # Trata o valor monetario enviado pelo formulario
        try:
            # Substitui "R$" por Vazio "", Substitui "." por Vazio, Substitui "," por "." e retira os espaços desnecessários
            valor = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
            valor_tratado = float(valor)
        except ValueError:
            return HttpResponseBadRequest("O valor da multa fornecido não é valido!")
        
        # Buscar os objetos colaborador, veiculo e centro_custo pelos IDs fornecidos em suas respectivas tabelas
        colaborador = Colaborador.objects.get(id=colaborador)
        veiculo = Veiculo.objects.get(id=veiculo)
        centro_custo = CentroCusto.objects.get(id=centro_custo)

        try:
            # Realiza a edição em cada um dos campos da tabela
            multa.data_infracao = data_infracao
            multa.hora_infracao = hora_infracao
            multa.auto_infracao = auto_infracao
            multa.gravidade = gravidade
            multa.data_vencimento = data_vencimento
            multa.situacao_multa = situacao_multa
            multa.colaborador = colaborador
            multa.veiculo = veiculo
            multa.centro_custo = centro_custo
            multa.descricao = descricao
            multa.valor = valor_tratado

            # Salva as alterações no banco de dados
            multa.save()

            messages.success(request, "A multa foi atualizada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao atualizar a multa: {str(e)}")

        # Após o sucesso ou fracasso da requisição o usuario é retornando de volta para a pagina de lista de multas
        return redirect("lista_multas")

    # Renderiza a pagina de edição de multas passando os contextos necessarios para a edição da multa
    return render(request, "seguranca/multas/editar_multa.html", {"multa": multa, "colaboradores": colaboradores, "veiculos": veiculos, "centros": centros, "gravidades": gravidades, "situacoes": situacoes})


# Exclui uma multa do banco de dados
def excluirMulta(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera o id enviado pelo formulário
        multa_id = request.POST.get('idMulta')

        # Busca na tabela de multas um ID igual ao ID enviado pelo modal
        multa = get_object_or_404(Multa, pk=multa_id)

        # Tenta apagar a multa
        try:
            multa.delete()
            messages.success(request, "Multa excluída com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao tentar excluir a multa: {str(e)}")
        
        return redirect("lista_multas")
    

