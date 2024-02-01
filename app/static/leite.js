function populaTabela(id_soma){
    console.log(id_soma)

    
    tabela = document.getElementById("corpo-tabela")
    tabela.innerHTML = ''
    var content = ''
    axios.get("http://localhost:8000/leites/").then((response)=>{
        return response.data
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




function formataPesquisa(){
    var tipo_pesquisa = document.getElementById('tipo_pesquisa')
    if(tipo_pesquisa.value == 'data' || tipo_pesquisa.value == 'data_inicio' || tipo_pesquisa.value == 'data_fim')
    {
        $('#pesquisa').mask('00/00/0000')
    }else if(tipo_pesquisa.value == 'preco' || tipo_pesquisa.value == 'total')
    {
        $('#pesquisa').mask('0000.00',{reverse: true})
    }else{
        $('#pesquisa').unmask()
    }
}


$('#preco').mask('000.00',{reverse: true})