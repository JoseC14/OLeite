

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