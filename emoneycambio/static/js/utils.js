function ajax(url, method, data) {
    
    var ajax = new XMLHttpRequest();

    // Seta tipo de requisição e URL com os parâmetros
    ajax.open(method, url, true);
    ajax.setRequestHeader("Content-type", "application/json");
    
    if (data) {
        data = JSON.stringify(data)
        ajax.send(data);
    } else {
        ajax.send()
    }

    // Cria um evento para receber o retorno.
    ajax.onreadystatechange = function() {
      // Caso o state seja 4 e o http.status for 200, é porque a requisiçõe deu certo.
        if (ajax.readyState == 4 && ajax.status == 200) {        
            var data = JSON.parse(this.responseText);
            return data
        }
    }
}

function clearAccentuation(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
}