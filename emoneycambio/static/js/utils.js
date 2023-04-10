function ajaxReplaceHtmlToResponse(url, method, data, parent, replace) {
    
    var ajax = new XMLHttpRequest();

    // Seta tipo de requisição e URL com os parâmetros
    ajax.open(method, url, true);
    ajax.setRequestHeader("Content-type", "application/json");
    ajax.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    

    
    if (data) {
        data = JSON.stringify(data)
        console.log(data)
        ajax.send(data);
    } else {
        ajax.send()
    }

    // Cria um evento para receber o retorno.
    ajax.onreadystatechange = function() {
      // Caso o state seja 4 e o http.status for 200, é porque a requisiçõe deu certo.
        if (ajax.readyState == 4 && ajax.status == 200) {        
            // var data = JSON.parse(this.responseText);
            parent.removeChild(replace);
            // console.log(this.responseText)
            parent.innerHTML = this.responseText
            


        }
    }
}

function clearAccentuation(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
}

function onlyNumbers(input_str) {

    if (!input_str)
        return ""

    return input_str.replace(/\D/g, "");
}

function forceValidation(elementsId) {
    if (!elementsId)
        return
    
    for (var i = 0; i < elementsId.length; i++) {
        let element = document.getElementById(elementsId[i])
        element.classList.remove('check-value')
        if (!element.value) {
            element.classList.add('check-value')
            return "stop"
        }
    }

}