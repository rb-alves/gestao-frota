// Interação com a sidebar
const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});



// Função pega os dados do laço de repetição e envia para um modal - Modal Exlusão de colaboradores
function pegar_dados_colaborador(id, nome){
    document.getElementById('idColaborador').value = id
    document.getElementById('nomeColaborador').innerText = nome
}


// Recupera os dados de cada fornecedor fornecido pelo laço de repetição - Modal Exclusão de Fornecedores
function dados_forn_del(id, nome){
  document.getElementById('idFornecedor').value = id
  document.getElementById('nomeFornecedor').innerText = nome
}

// Recupera os dados e envia para o modal de exclusão de veículos
function dados_veiculos_del(id, nome){
  document.getElementById('idVeiculo').value = id
  document.getElementById('nomeVeiculo'). innerText = nome
}

// Recupera os dados e envia para o modal de exclusão de Maquinas
function dados_maquinas_del(id, nome){
  document.getElementById('idMaquina').value = id
  document.getElementById('nomeMaquina').innerText = nome
}

// Recupera os dados e envia para o modal de exclusão de Manutenções - Veiculos e Maquinas
function dados_manutVeiculo_del(id, placa, documento){
  document.getElementById('idManutencao').value = id
  document.getElementById('placaManutencao').innerText = placa
  document.getElementById('numDocumentoManut').innerText = documento
}

// Recupera os dados e envia para o modal de exclusão de Manutenções - Manutenção Geral
function dados_manutGeral_del(id, valor, documento){
  document.getElementById('idManutencao').value = id
  document.getElementById('valorManutencaoGeral').innerText = "R$" + valor
  document.getElementById('numDocumentoManut').innerText = documento
}

// Recupera os dados e envia para o modal de exclusão de Multas - Multas
function dados_multa_del(id, placa, auto_infracao){
  document.getElementById('idMulta').value = id
  document.getElementById('placaMulta').innerText = placa
  document.getElementById('numAutoInfracao').innerText = auto_infracao
}

// Recupera os dados e envia para o modal de exclusão de Ocorridos - Ocorridos
function dados_ocorrido_del(id, placa, nome){
  document.getElementById('idOcorrido').value = id
  document.getElementById('placaOcorrido').innerText = placa
  document.getElementById('nomeColaborador').innerText = nome
}



// pega os dados e ultiliza nos modais de cadastros para realização das requisições
function pegar_dados(id, descricao){
  //Cargos
  document.getElementById('idCargoEdit').value = id
  document.getElementById('descricaoCargoEdit').value = descricao

  document.getElementById('idCargoDel').value = id
  document.getElementById('descricaoCargoDel').innerText = descricao

  //Departamentos
  document.getElementById('idDepartamentoEdit').value = id
  document.getElementById('descricaoDepartamentoEdit').value = descricao

  document.getElementById('idDepartamentoDel').value = id
  document.getElementById('descricaoDepartamentoDel').innerText = descricao

  //Especialidade dos Fornecedores
  document.getElementById('idEspFornecedorEdit').value = id
  document.getElementById('descricaoEspFornecedorEdit').value = descricao

  document.getElementById('idEspFornecedoresDel').value = id
  document.getElementById('descricaoEspFornecedoresDel').innerText = descricao

  //Grupo de veículos
  document.getElementById('idgrupoVeiculoEdit').value = id
  document.getElementById('descricaogrupoVeiculoEdit'). value = descricao

  document.getElementById('idgrupoVeiculoDel').value = id
  document.getElementById('descricaogrupoVeiculoDel'). innerText = descricao

  //Combustíveis
  document.getElementById('idcombustivelEdit').value = id
  document.getElementById('descricaocombustivelEdit'). value = descricao

  document.getElementById('idcombustivelDel').value = id
  document.getElementById('descricaocombustivelDel'). innerText = descricao

  //Causas manutenções
  document.getElementById('idCausaEdit').value = id
  document.getElementById('descricaoCausaEdit'). value = descricao

  document.getElementById('idCausaDel').value = id
  document.getElementById('descricaoCausaDel'). innerText = descricao

  //Tipos das manutenções
  document.getElementById('idTipoEdit').value = id
  document.getElementById('descricaoTipoEdit'). value = descricao

  document.getElementById('idTipoDel').value = id
  document.getElementById('descricaoTipoDel'). innerText = descricao

  //Centros de Custos
  document.getElementById('idCentroCustoEdit').value = id
  document.getElementById('descricaoCentroCustoEdit'). value = descricao

  document.getElementById('idCentroCustoDel').value = id
  document.getElementById('descricaoCentroCustoDel'). innerText = descricao

    
}



// Fechamento e abertura de modais na aba cadastro
function openModal(modalPrincipal, modalSecundario) {
  $(modalPrincipal).modal('hide'); // Fecha o modal Principal
  
  //SETIMEOUT causa um atraso na abertura do modal
  setTimeout(function(){
    $(modalSecundario).modal('show'); // Abre o modal Secundario
  }, 500);
  
}



// Plugin de ordenação de datas
jQuery.extend(jQuery.fn.dataTable.ext.type.order, {
  "date-br-pre": function (date) {
      if (!date) {
          return 0;
      }
      var parts = date.split('/');
      return new Date(parts[2], parts[1] - 1, parts[0]).getTime();
  },
  "date-br-asc": function (a, b) {
      return a - b;
  },
  "date-br-desc": function (a, b) {
      return b - a;
  }
});


  // Função para inicializar a tabela
  function inicializarTabela(tabela) {
    return new DataTable(tabela, {
        // Tradução para português
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.11.3/i18n/pt_br.json",
            lengthMenu: "Exibir _MENU_ ",
        },

        // Define o tipo de paginação
        pagingType: "simple_numbers",

        // Remove a ordenação padrão da primeira coluna
        order: [],

        // Define o tipo de ordenação para colunas específicas
        columnDefs: [
            {
                targets: "data-br", // Aplica a configuração para colunas com a classe "data-br"
                type: "date-br"
            },
        ],

        // Posiciona os elementos da tabela
        layout: {
            bottomStart: 'info',
            bottom: 'paging',
            bottomEnd: {
                buttons: [
                    'colvis',
                    {
                        extend: 'excelHtml5',
                        autoFilter: true,
                        text: 'Exportar',
                        exportOptions: {
                            columns: ':visible', // Exporta apenas as colunas visíveis
                        },
                        customizeData: function (data) {
                            // Itera sobre os dados para corrigir os números decimais
                            data.body.forEach(function (row) {
                                row.forEach(function (cell, index) {
                                    // Substitui vírgula por ponto apenas em valores numéricos
                                    if (cell.match(/^-?\d+,\d+$/)) {
                                        row[index] = cell.replace(',', '.');
                                    }
                                });
                            });
                        },
                    },
                ],
            },
        },

        // Torna a tabela responsiva
        responsive: true,
    });
}



// Inicializa as tabelas ultlizando a configuração padrão da função datatables
let colaboradores = inicializarTabela('#colaboradores')
let fornecedores = inicializarTabela('#fornecedores')
let cadastros = inicializarTabela('#cadastros')
let cargos = inicializarTabela('#cargos')
let departamentos = inicializarTabela('#departamentos')
let especialidade_fornecedores = inicializarTabela('#espFornecedores')
let grupo_veiculos = inicializarTabela('#grupoVeiculos')
let combustiveis = inicializarTabela('#combustiveis')
let causas = inicializarTabela('#causas')
let tipos = inicializarTabela('#tipos')
let centros_custos = inicializarTabela('#centros_custos')
let veiculos = inicializarTabela('#veiculos')
let maquinas = inicializarTabela('#maquinas')
let manutencoes = inicializarTabela('#manutencoes')
let manutencoesMaquinas = inicializarTabela('#manutencoesMaquinas')
let manutencoesGerais = inicializarTabela('#manutencoesGerais')
let multas = inicializarTabela('#multas')
let incidentes = inicializarTabela('#incidentes')
let abastecimentos = inicializarTabela('#abastecimentos')



// Inicializa e formata os campos de valores monetários
function inicializarCampoMonetario(campo){
  return new Cleave(campo,{
    numeral: true,
    numeralThousandsGroupStyle: 'thousand',
    numeralDecimalMark: ',',
    delimiter: '.',
    prefix: 'R$ ',
    numeralPositiveOnly: true,
    rawValueTrimPrefix: true
  })
}

function inicializarCampoDecimal(campo){
  return new Cleave(campo,{
    numeral: true,
    numeralThousandsGroupStyle: 'thousand',
    numeralDecimalMark: ',',
    delimiter: '.',
    numeralPositiveOnly: true,
    rawValueTrimPrefix: true,
    noImmediatePrefix: true // Evita adicionar "R$ " em campos vazios
  })
}

// Aguarda que o documento seja carregado e em seguida executa a função
document.addEventListener('DOMContentLoaded', function() {
  // Seleciona os campos
  let campoValorManutVeiculo = document.querySelector('#valorManutVeiculo');
  let campoValorManutMaquina = document.querySelector('#valorManutMaquina');
  let campoValorManutGeral = document.querySelector('#valorManutGeral');
  let campoValorMulta = document.querySelector('#valorMulta');
  let campoValorOcorrido = document.querySelector('#valorOcorrido');
  let campoValorTransacao = document.querySelector('#valor_transacao');
  let campoValorLitro = document.querySelector('#valor_unitario');
  let campoQtdLitro = document.querySelector('#litros');
  let campoFiltroValor = document.querySelector('#filtro-valorManutVeiculo')
  let campoFiltroValorMaquina = document.querySelector('#filtro-valorManutMaquina')
  let campoFiltroValorGeral = document.querySelector('#filtro-valorManutGeral')
  let campoFiltroValorOcorrido = document.querySelector('#filtro-valorOcorrido')
  let campoFiltroValorMulta = document.querySelector('#filtro-valorMulta')
  

  if (campoValorManutVeiculo) {
    inicializarCampoMonetario(campoValorManutVeiculo);
  }
  
  if (campoValorManutMaquina) {
    inicializarCampoMonetario(campoValorManutMaquina);
  }

  if (campoValorManutGeral){
    inicializarCampoMonetario(campoValorManutGeral);
  }
  if (campoValorMulta) {
    inicializarCampoMonetario(campoValorMulta);
  }
  if (campoValorOcorrido) {
    inicializarCampoMonetario(campoValorOcorrido);
  }
  if (campoValorTransacao) {
    inicializarCampoMonetario(campoValorTransacao);
  }
  if (campoValorLitro) {
    inicializarCampoMonetario(campoValorLitro);
  }
    if (campoQtdLitro) {
    inicializarCampoDecimal(campoQtdLitro);
  }

  if (campoFiltroValor) {
    inicializarCampoMonetario(campoFiltroValor)
  }

  if (campoFiltroValorMaquina) {
    inicializarCampoMonetario(campoFiltroValorMaquina)
  }

  if (campoFiltroValorGeral) {
    inicializarCampoMonetario(campoFiltroValorGeral)
  }

  if (campoFiltroValorOcorrido) {
    inicializarCampoMonetario(campoFiltroValorOcorrido)
  }

  if (campoFiltroValorMulta) {
    inicializarCampoMonetario(campoFiltroValorMulta)
  }


});


// Função para formatar os campos de CPF
function formataCPF(campo) {
  new Cleave(campo, {
    blocks: [3, 3, 3, 2],
    delimiters: ['.', '.', '-'],
    numericOnly: true
  });
}

// Cria a mascara de CNPJ para os campos
function formataCNPJ(campo) {
  new Cleave (campo, {
    delimiters: ['.', '.', '/', '-'],
    blocks: [2, 3, 3, 4, 2],
    numericOnly: true,
  });
}


// Máscara para Telefone
function formataTelefone(campo) {
  new Cleave(campo, {
    delimiters: ['(', ') ', '-'],
    blocks: [0, 2, 5, 4], // Suporte a 9 dígitos (ex: (11) 91234-5678)
    numericOnly: true,
  });
}


// Aguarda que o documento seja carregado e em seguida executa a função
document.addEventListener('DOMContentLoaded', function() {
// Selecionando os campos pelo ID com querySelector (usando # corretamente)
let campoCPF = document.querySelector('#cpf');
let campoFiltroCPF = document.querySelector('#filtro-cpf');
let campoCNPJ = document.querySelector('#cnpj');
let campoFiltroCNPJ = document.querySelector('#filtro-cnpj');
let campoTelefone = document.querySelector('#telefone');
let campoFiltroTelefone = document.querySelector('#filtro-telefone');


// Verificando se os campos foram encontrados antes de aplicar a formatação
if (campoCPF) {
  formataCPF(campoCPF);
}

if (campoFiltroCPF) {
  formataCPF(campoFiltroCPF);
}

if (campoCNPJ) {
  formataCNPJ(campoCNPJ)
}

if (campoFiltroCNPJ){
  formataCNPJ(campoFiltroCNPJ)
}

if (campoTelefone) {
  formataTelefone(campoTelefone)
}

if (campoFiltroTelefone)
  formataTelefone(campoFiltroTelefone)
});







function showFileName(input) {
  var file = input.files[0]; // Obtém o primeiro arquivo selecionado
  var fileName = file ? file.name : 'Sem arquivo'; // Define o nome do arquivo ou texto padrão
  
  // Tenta localizar o span file-chosen próximo ao input (caso seja um irmão direto)
  var fileChosen = input.parentElement.nextElementSibling;

  // Se não encontrar, procura o span dentro do contexto mais amplo (para Documentos e Fotos/Vídeos)
  if (!fileChosen || !fileChosen.classList.contains('file-chosen')) {
      fileChosen = input.closest('.col, .input-group')?.querySelector('.file-chosen, .mt-1');
  }

  if (fileChosen) {
      fileChosen.textContent = fileName; // Atualiza o texto do elemento encontrado
  } else {
      console.warn('Elemento file-chosen não encontrado para:', input);
  }
}







// Oculta os INPUT FILES caso o tipo de OCORRIDO seja PERDA OU FURTO
document.addEventListener("DOMContentLoaded", function(){
  const tipoOcorridoSelecionado = document.getElementById("tipo_ocorrido");
  const documentosSecao = document.getElementById("documentos-secao");
  const fotosVideosSecao = document.getElementById("fotos-videos-secao");
  const dadosPrejudicadoSecao = document.getElementById("dados-prejudicado-secao");

  function toggleSections(){
    if(tipoOcorridoSelecionado.value === "Perda ou Furto" || tipoOcorridoSelecionado.value === ""){
      documentosSecao.style.display = "none";
      fotosVideosSecao.style.display = "none";
      dadosPrejudicadoSecao.style.display = "none";
    }else{
      documentosSecao.style.display = "block";
      fotosVideosSecao.style.display = "block";
      dadosPrejudicadoSecao.style.display = "block";
    }
  }

  tipoOcorridoSelecionado.addEventListener("change", toggleSections);
  toggleSections();

});


// Realiza a requição para view ULTIMO_HODOMETRO pega o valor e atribui ao elemento KM_ANTERIOR
document.getElementById("veiculo_cad_abastecimento").addEventListener("change", function(){

  // Armazena o valor atual do elemento veiculo na variável
  var veiculoID = this.value;

  if (veiculoID) {
    fetch(`/ultimo_hodometro/${veiculoID}`)
      .then(response => response.json())
      .then(data => {
            // Preenche o campo "Km Anterior" com o hodômetro recebido
            document.getElementById("km_anterior").value = data.hodometro;
      })
      .catch(error => console.error('Erro', error))
  } else {
    // Limpa o campo caso não haja veiculo selecionado
    document.getElementById("km_anterior").value = '';
  }

});


 // Adicionando os listeners nos campos que podem disparar o cálculo - Caso Km_transacao seja preenchido
 document.getElementById("km_transacao").addEventListener("input", function() {
  calcularKmPercorrido();
  calcularConsumo();
});

 // Adicionando os listeners nos campos que podem disparar o cálculo - Caso km anterior seja preenchido
 document.getElementById("km_anterior").addEventListener("input", function() {
  calcularKmPercorrido();
  calcularConsumo();
});

 // Adicionando os listeners nos campos que podem disparar o cálculo - Caso litros seja preechidos
 document.getElementById("litros").addEventListener("input", function() {
  calcularKmPercorrido();
  calcularConsumo();
});

function calcularKmPercorrido () {
// Obtém os valores dos campos Km de Transação e Km Anterior
var kmTransacao = parseFloat(document.getElementById("km_transacao").value) || 0;
var km_anterior = parseFloat(document.getElementById("km_anterior").value) || 0;

// Calcula a diferença (KM Percorrido)
var kmPercorrido = kmTransacao - km_anterior;

// Preenche o campo "Km Percorrido"
document.querySelector("input[name='km_percorrido']").value = kmPercorrido;
}




function formataNumero(valorF){
  valor = valorF.replace(".", "").replace(",", ".")
  return valor
}


function calcularConsumo() {
// Obtém os valores dos campos Litros e Km Percorrido
var litros = parseFloat(formataNumero(document.getElementById("litros").value)) || 0;
var kmPercorrido = parseFloat(document.querySelector("input[name='km_percorrido']").value) || 0

// Trata as divisões por zero
if (kmPercorrido > 0 && litros > 0) {
  // Calcula a média de consumo
  var consumo = kmPercorrido / litros;

  // Preenche o campo consumo
  document.querySelector("input[name='consumo']").value = consumo.toFixed(2); // Exibe com duas casas decimais
}
}