function checaLeitera()
{
    console.log('checando se é leitera...')
    tipo_gado = document.getElementById('tipo-gado')
    leitera   = document.getElementById('leitera')
    if(tipo_gado.value=='vaca')
    {
        leitera.classList.remove('leitera')
    }else
    {
        leitera.classList.add('leitera')
    }
}