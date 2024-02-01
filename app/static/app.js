categorias_leite = new Array()
dados_leite = new Array()

dados_chuva = new Array()
datas_chuva = new Array()

axios.get("http://localhost:8000/registros/").then((data) => {
  return data.data
}).then((response) => {
  response.forEach((element) => {
    categorias_leite.push(element['data_fim'])
    dados_leite.push(element['total'])
    console.log(categorias_leite)
    console.log(dados_leite)
  })

  // Configuração do gráfico de leites
  var optionsLeites = {
    series: [{
      name: "Leites por Registro",
      data: dados_leite
    }],
    chart: {
      height: 350,
      type: 'line',
      zoom: {
        enabled: false
      }
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'straight'
    },
    title: {
      text: 'Leites por Registro',
      align: 'left'
    },
    grid: {
      row: {
        colors: ['#f3f3f3', 'transparent'],
        opacity: 0.5
      },
    },
    xaxis: {
      categories: categorias_leite,
    }
  };

  var graficos_leites = new ApexCharts(document.querySelector("#leites"), optionsLeites);
  graficos_leites.render();
})

axios.get("http://localhost:8000/chuvas/").then((data) => {
  return data.data
}).then((registros_chuvas) => {
  registros_chuvas.forEach((element) => {
    datas_chuva.push(element['data'])
    dados_chuva.push(element['milimetros'])
    console.log(datas_chuva)
    console.log(dados_chuva)
  })

  // Configuração do gráfico de chuvas
  var optionsChuvas = {
    series: [{
      name: "Milímetros por Data",
      data: dados_chuva
    }],
    chart: {
      height: 350,
      type: 'line',
      zoom: {
        enabled: false
      }
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'straight'
    },
    title: {
      text: 'Milímetros por Data',
      align: 'left'
    },
    grid: {
      row: {
        colors: ['#f3f3f3', 'transparent'],
        opacity: 0.5
      },
    },
    xaxis: {
      categories: datas_chuva,
    }
  };

  var grafico_chuvas = new ApexCharts(document.querySelector("#chuvas"), optionsChuvas);
  grafico_chuvas.render();
})





function checaSenhaNumeros(senha)
{
  var regex = new RegExp('[0-9]')
  return regex.test(senha)
}

function checaSenhaEspecial(senha)
{
  var regex = /[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]/;
  return regex.test(senha)
}

function checaSenhaMaiusculo(senha)
{
  var regex = new RegExp('[A-Z]')
  return regex.test(senha)
}

function checaSenhaMinusculo(senha)
{
  var regex = new RegExp('[a-z]')
  return regex.test(senha)
}

let senha_valida = false
let senha_igual = false


function checaSenha(event)
{
  var botao = document.getElementById('botao-form')
  var senha = document.getElementById('senha').value
  console.log(`Senhas são iguais: ${senha_igual}`)
  console.log(`Senhas é válida: ${senha_valida}`)
  

  if(event.target.id == 'senha'){
    console.log('campo senha')
    
    var numero = document.getElementById('numero')
    var especial = document.getElementById('especial')
    var minuscula = document.getElementById('minuscula')
    var maiuscula = document.getElementById('maiuscula')
    var oito = document.getElementById('oito')
    
    if(senha.length >= 8)
    {
      oito.classList.add('list-invisible')
    }else if(oito.classList.contains('list-invisible')){
      oito.classList.remove('list-invisible')
    }

    if(checaSenhaEspecial(senha))
    {
      especial.classList.add('list-invisible')
    }else if(especial.classList.contains('list-invisible'))
    {
      especial.classList.remove('list-invisible')
     
    }

    if(checaSenhaNumeros(senha))
    {
      numero.classList.add('list-invisible')
    }else if(numero.classList.contains('list-invisible'))
    {
      numero.classList.remove('list-invisible')
      
    }

    if(checaSenhaMaiusculo(senha))
    {
      maiuscula.classList.add('list-invisible')
    }else if(maiuscula.classList.contains('list-invisible'))
    {
      maiuscula.classList.remove('list-invisible')
    
    }

    if(checaSenhaMinusculo(senha))
    {
      minuscula.classList.add('list-invisible')
    }else if(minuscula.classList.contains('list-invisible'))
    {
      minuscula.classList.remove('list-invisible')
    }

    if(checaSenhaEspecial(senha) && checaSenhaMaiusculo(senha)
    && checaSenhaMinusculo(senha) && checaSenhaNumeros(senha))
    {
      senha_valida = true
    }else{
      senha_valida = false
    }
  }else if(event.target.id == 'confirmar_senha')
  {
    console.log('campo confirma senha')
    var checa_senha = document.getElementById('confirmar_senha').value
    if(senha == checa_senha){
      senha_igual = true
    }else{
      senha_igual = false
    }
  }

  if(senha_valida && senha_igual){
    botao.classList.remove('disabled')
    console.log("habilitando botão")
  }
  else
  {
    console.log("desabilitando botão")
    botao.classList.add('disabled')
  }

  
}

function deletaDados(id,modulo){
  event.preventDefault()
  console.log("Deletando...")
  var confirmacao = confirm("Deseja realmente deletar?")
  if(confirmacao == true){
    window.location.href = `/${modulo}/deletar${modulo}/${id}`
  }
}
