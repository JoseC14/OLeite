
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