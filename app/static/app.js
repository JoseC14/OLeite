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
