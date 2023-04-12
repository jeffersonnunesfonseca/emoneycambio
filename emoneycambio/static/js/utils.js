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

function forceValidation(names) {
    if (!names)
        return
        
    for (var i = 0; i < names.length; i++) {
        
        let elements = document.getElementsByName(names[i])
        for (const element of elements){

            element.classList.remove('check-value')
            if (!element.value) {
                element.classList.add('check-value')
                return "stop"
            }
            break
        }
    }
}

function documentMask(event) {
    if (event.keyCode == 8 || event.keyCode == 46){
        return
    }

    let personType = $('input[name="pfpj"]:checked').val();
    if (personType == "pf") {
        $("#cpfcnpj").mask("999.999.999-99");
    }else {
        $("#cpfcnpj").mask("99.999.999/9999-99");

    }
}