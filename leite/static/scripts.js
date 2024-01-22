
function populaTabela(id_soma){
    console.log(id_soma)

    let data = fetch("http://127.0.0.1:8000/leites/")
    tabela = document.getElementById("corpo-tabela")
    tabela.innerHTML = ''
    var content = ''
    data.then((response)=>{
        return response.json()
    }).then((data) =>{
        console.log(data)
        data.forEach(element => {
            if(element['soma_id'] == id_soma){
                content +=
                '<tr><td>'
                + element['id']
                + '</td><td>'
                + element['quantidade']
                + '</td><td>'
                + element['data']
                + '</td></tr>';
            }
            

            
        });
        tabela.innerHTML += content
    })


}

function passaTabela(){
    let form = document.getElementById('form-rel')
    event.preventDefault()
    console.log('passando tabela...')
    let tabela = document.getElementById('tabela').innerHTML
    area_texto = document.getElementById('content-table')
    console.log("teste")
    let css = "<style>    .table{border: 1px solid black;}tr{   text-align: center;}</style>\n"
    area_texto.value = css
    area_texto.value += tabela
    console.log(area_texto.value)
    form.submit()
}


function deletaDados(id){
  console.log("Deletando...")
  var confirmacao = confirm("Deseja realmente deletar?")
  if(confirmacao){
    window.location.href = '/deletarleite/'+id
  }
}
  $(document).ready(function () {
    $('.dropdown-toggle').dropdown();
  });
  categorias = new Array()
  dados_leite = new Array()
  let registros = fetch("http://127.0.0.1:8000/registros/").then((data)=>{

    return data.json()
  }).then((registros)=>{
    registros.forEach(element => {
        categorias.push(element['data_fim'])
        dados_leite.push(element['total'])
        console.log(categorias)
        console.log(dados_leite)
    })
  })
  var options = {
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
      colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
      opacity: 0.5
    },
  },
  xaxis: {
    categories: categorias,
  }
  };

  var chart = new ApexCharts(document.querySelector("#chart"), options);
  chart.render();