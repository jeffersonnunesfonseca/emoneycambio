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
            if (!element.value || element.value == '') {
                element.classList.add('check-value')
                return "stop"
            }
            else if (element.name == "cpfcnpj") {
                value = onlyNumbers(element.value)
                if (value.length == 11){
                    if (!validaCPF(value)){
                        console.log("invalido cpf")
                        element.classList.add('check-value')
                        return "stop"
                    }

                }
                else if(value.length == 14) {
                    if (!validaCNPJ(value)){
                        console.log("invalido cnpj")
                        element.classList.add('check-value')
                        return "stop"
                    }
                }
            }
            break
        }
    }
}

function documentMask(event, type=null) {
    if (event.keyCode == 8 || event.keyCode == 46){
        return
    }

    let personType = type || $('input[name="pfpj"]:checked').val();
    if (personType == "pf") {
        $("#cpfcnpj").mask("999.999.999-99");
    }else {
        $("#cpfcnpj").mask("99.999.999/9999-99");

    }
}

function formataDinheiro(n) {
    const toFixed = (n, fixed) => `${n}`.match(new RegExp(`^-?\\d+(?:\.\\d{0,${fixed}})?`))[0];
    n = String(n).replace('.', ',').replace(/(\d)(?=(\d{3})+\,)/g, "$1.");
    // const toFixed = (n, 2) => `${n}`.match(new RegExp(`^-?\\d+(?:\.\\d{0,${fixed}})?`))[0];
    // const toFixed = (n, fixed) => ~~(Math.pow(10, fixed) * n) / Math.pow(10, fixed);

    return toFixed(n, 2)
}

// Valida CPF
function validaCPF(cpf) {  
    cpf = cpf.replace(/[^\d]+/g,'');    
    if(cpf == '') return false;   
    if (
        cpf.length != 11 || 
        cpf == "00000000000" || 
        cpf == "11111111111" || 
        cpf == "22222222222" || 
        cpf == "33333333333" || 
        cpf == "44444444444" || 
        cpf == "55555555555" || 
        cpf == "66666666666" || 
        cpf == "77777777777" || 
        cpf == "88888888888" || 
        cpf == "99999999999" || 
        cpf == "01234567890" )
        return false;      
    add = 0;    
    for (i=0; i < 9; i ++)       
    add += parseInt(cpf.charAt(i)) * (10 - i);  
    rev = 11 - (add % 11);  
    if (rev == 10 || rev == 11)     
        rev = 0;    
    if (rev != parseInt(cpf.charAt(9)))     
        return false;    
    add = 0;    
    for (i = 0; i < 10; i ++)        
        add += parseInt(cpf.charAt(i)) * (11 - i);  
    rev = 11 - (add % 11);  
    if (rev == 10 || rev == 11) 
        rev = 0;    
    if (rev != parseInt(cpf.charAt(10)))
        return false;       
    return true;   
}

// Valida CNPJ
function validaCNPJ(CNPJ) {
    CNPJ = CNPJ.replace(/[^\d]+/g,''); 
    var a = new Array();
    var b = new Number;
    var c = [6,5,4,3,2,9,8,7,6,5,4,3,2];
    for (i=0; i<12; i++){
        a[i] = CNPJ.charAt(i);
        b += a[i] * c[i+1];
    }
    if ((x = b % 11) < 2) { a[12] = 0 } else { a[12] = 11-x }
    b = 0;
    for (y=0; y<13; y++) {
        b += (a[y] * c[y]);
    }
    if ((x = b % 11) < 2) { a[13] = 0; } else { a[13] = 11-x; }
    if ((CNPJ.charAt(12) != a[12]) || (CNPJ.charAt(13) != a[13])){
        return false;
    }
    if (CNPJ == 00000000000000) {
        return false;
    }
    return true;
}