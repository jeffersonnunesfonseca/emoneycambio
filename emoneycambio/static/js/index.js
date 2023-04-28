const toogleMenuHeader = (event) => {
    let menu = document.getElementById("menu-header").style.height
    if (!menu || menu=="0px"){
        document.getElementById("menu-header").style.display = "flex"
        document.getElementById("menu-header").style.height = "auto"
    }
    else{
       document.getElementById("menu-header").style.height = "0"
       document.getElementById("menu-header").style.display = "none"
    }
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

function validaEmail(email) {
    var reg = /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/
    if (reg.test(email)){
        return true; 
    }
    return false;
    
}
function formataDinheiro(n) {
    result = n.toFixed(5).replace('.', ',').replace(/(\d)(?=(\d{3})+\,)/g, "$1.");
    result = result.substring(0, result.length - 3);
    console.log(result)
    return result
}


function updateBulletCoin(){
    $.get('/v1/exchange_commercial_coins', function(obj) {
        for (const iterator of obj) {
            if ($(`#${iterator.key}`)){
                let valor = formataDinheiro(iterator.value)
                $(`#${iterator.key}`).text(`${iterator.symbol} ${valor}`)
            }
        }
    })
}

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
            else if (element.name == "email") {
                if (!validaEmail(element.value)){
                    console.log("invalido EMAIL", element.value)
                    element.classList.add('check-value')
                    return "stop"
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

function phoneMask(event) {
    $("#phone").mask('(00) 00000-0000');
}

function nextStepForm(e) {
    e.preventDefault()

    let currentUrlPath = document.location.pathname
    let step = document.getElementById('steps')
    let form = document.getElementById("form-step")
    var formdata = $(".form-step").serializeArray()
    var data = {};
    let keys = []
    $(formdata ).each(function(index, obj){
        data[obj.name] = obj.value;
        if (obj.name =='pfpj' || obj.name == 'delivery'){

        }else{
            keys.push(obj.name)
        }
    });
    
    if (forceValidation(keys) == "stop") {
        return
    }

    
    
    if (document.getElementById("money-tourism") || document.getElementById("money")) {

        let moneyInput = document.getElementById("money-tourism") || document.getElementById("money")
        let moneyValue = moneyInput.value.replace("R$", "").trim()
        console.log((parseFloat(onlyNumbers(moneyValue)/100)))
        if ((parseFloat(onlyNumbers(moneyValue))/100) < 100) {
            moneyInput.classList.add("check-value")
            return
        }

        if (document.getElementById("fee_value")) {
            let value = onlyNumbers(moneyInput.value)
            let feeValue = onlyNumbers(document.getElementById("fee_value").value)
            currentUrlPath = `${currentUrlPath}/${value}/${feeValue}`

        }
    }
    
    let newUrl = `${currentUrlPath}?step=${data['nextstep']}`
    if ($('input[name="finish"]').val() && $('input[name="finish"]').val() == 'true') {
        console.log( $('input[name="finish"]').val())  
        console.log(e.currentTarget)      
        e.currentTarget.value = 'Enviando ...'
        e.currentTarget.disabled= true

    }
    response = ajaxReplaceHtmlToResponse(newUrl,'POST', data, step, form)
    window.history.pushState({},"", newUrl);
}

// PORTAL/HOME
function sendFormPrice(e) {
    e.preventDefault();
    
    let searchCoin = document.getElementById("search-coin").value
    let searchLocation = document.getElementById("search-location").value
    console.log(searchCoin)
    console.log(searchLocation)

    if (forceValidation(['search-coin', 'search-location']) == "stop") {
        return
    }

    
    return window.location = `/cotacao/${searchCoin}/${searchLocation}`
}

// PORTAL/NEGOTIATION-INTERNATIONAL-SHIPMENT
function updateTextValues() {

    let coinText = $("#coin").find('option:selected')
    let transactionText = $('input[name="transaction"]:checked')

    console.log(coinText.text())
    console.log(coinText.attr('attr-symbol'))
    console.log(transactionText.val())

    $("#money").maskMoney({prefix: `${coinText.attr('attr-symbol')} `, thousands:'.', decimal:',', affixesStay: true});

    $("#coin-text").text(coinText.text())
    
    $("#transaction-text").text(transactionText.val())

    if (transactionText.val() == "enviar") {
        $(".msg-calc-enviar").css("display", "block")
        $(".msg-calc-receber").css("display", "none")

    } else {
        $(".msg-calc-enviar").css("display", "none")
        $(".msg-calc-receber").css("display", "block")
    }

}


function nextStepFormCustom(event) {
    // http://localhost:5656/remessa-internacional/dolar/pf/enviar/10000/111
    event.preventDefault()

    var formdata = $(".form-step").serializeArray()
    let keys = []
    let data = {}
    $(formdata ).each(function(index, obj){
        value = clearAccentuation(obj.value).toLowerCase();
        if (obj.name == 'value'|| obj.name == 'fee'){
            value = onlyNumbers(value)
        }
        data[obj.name] = value
        keys.push(obj.name)
    });

    console.log(data)

    if (forceValidation(keys) == "stop") {
        return
    }

    if (document.getElementById("money")) {

        let moneyInput = document.getElementById("money")
        let moneyValue = moneyInput.value.replace("R$", "").trim()
        console.log((parseFloat(onlyNumbers(moneyValue)/100)))
        if ((parseFloat(onlyNumbers(moneyValue))/100) < 100) {
            moneyInput.classList.add("check-value")
            return
        }
    }

    let currentUrlPath = document.location.pathname.replace(/\/$/g, '') // força retirar ultimo slash
    if (data.hasOwnProperty("pfpjreason")) {
        console.log(currentUrlPath)
        currentUrlPath = currentUrlPath + "/" + data["pfpjreason"]
    }
    else {
        currentUrlPath = `/remessa-internacional/${data['coin']}/${data['person_type']}/${data['transaction']}`
    }
    
    
    console.log(data, currentUrlPath)

    // location.href = currentUrlPath
    window.history.pushState({},"", currentUrlPath);
    nextStepForm(event)
}

// PORTAL/SEARCH-RESULT
function goToNegotiation(event, type, companyBranchId, negotiationType) {
    event.preventDefault()
    let currentUrlPath = document.location.pathname
    let newUrl = currentUrlPath.replace('cotacao', `negociacao/${type}/${negotiationType}`) + "/" + companyBranchId 
    console.log(companyBranchId, type, currentUrlPath, negotiationType, newUrl)
    location.href = newUrl

}

$(document).ready(function() {
    
    setInterval(() => {
        // macete para desabilitar autocomple cpf 
        $("input[type='text']").attr('autocomplete', 'off');        
    }, 500);

    $('#phone').mask('(00) 00000-0000');
      
    $(".filter-select").select2({
        // matcher: matchStart
        minimumResultsForSearch: -1 //desabilita o buscador
    });

    updateBulletCoin()
    setInterval(function(){
        updateBulletCoin()
    }, 300000);
 
    // NEGOTIATION-TOURISM
    $("#money-tourism").maskMoney({prefix:'$ ', thousands:'.', decimal:',', affixesStay: true});
    $("#money-tourism").keyup(function(e){
        // alert()
        e.preventDefault()
        let currentValue = onlyNumbers($(this).val())
        let feeValue = onlyNumbers($('input#fee_value').val())
        let newValue = parseFloat((currentValue/100) * (feeValue/100)).toFixed(2);
        // newValue = Number(newValue.replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,"),'$1,')
        // newValue = Number(newValue).toFixed(0).replace(/^(?!0\.00)\d{1,3}(,\d{3})*(\.\d\d)?$/g, "$1");
        // console.log(newValue)
        newValue = formataDinheiro(Number(newValue))
        $("#dynamic-total-value").text(newValue)


    })

    //NEGOTIATION-INTERNATION-SHIPMENT
    updateTextValues()

    $('#phone').keyup(function(e){
        $(this).mask('(00) 00000-0000');
    })
    
    $("#coin").change(function(e){
        e.preventDefault()
        let coinValue= $("#coin").find('option:selected').val()
        // console.log(coinValue)
        location.href = `/remessa-internacional?coin=${coinValue}&step=initial&update_select=True`


    })

    $("input[name='transaction']").click(function(e){
        updateTextValues()
    })

    $("#money").keyup(function(e){
        // alert()
        let currentValue = onlyNumbers($(this).val())
        let feeValue = onlyNumbers($('input#fee_value').val())
        let newValue = parseFloat((currentValue/100) * (feeValue/100)).toFixed(2);
        console.log(currentValue)
        console.log(feeValue)
        console.log(newValue)
        newValue = formataDinheiro(Number(newValue))
        $("#dynamic-total-value-enviar").text(newValue)
        $("#dynamic-total-value-receber").text(newValue)
    })

    //FOOTER
    const mainContent = document.getElementById("#content")
    const footerElement = document.createElement("footer")
    footerElement.innerHTML = `<div>
                    
                <a class="logo-footer-negotiation-tourism-link" href="/">
        
                        <img src="/static/images/logo.png" alt="facebook" width="120"  height="120"/>
                    </a>
                </div>
        
                <div>
                    <span class="subtitle-font-style">Institucional</span>
                    <ul>
                        <li><a class="aboutus-link" rel="noreferrer nofollow" href="/quem-somos/">Quem Somos</a></li>
                        <li><a class="termsuse-link" rel="noreferrer nofollow" href="/termos-de-uso/">Termos de uso</a></li>
                        <li><a class="privacypolicy-link" rel="noreferrer nofollow" href="/politicas-de-privacidade/">Políticas de privacidade</a></li>
                    </ul>
                </div>
                <div>
                    <span class="subtitle-font-style">Serviços</span>
                    <ul>
                        <li><a rel="noreferrer nofollow" href="/remessa-internacional/">Remessas</a></li>
                        <li><a href="/">Papel/Moeda</a></li>
                       <!-- <li><a href="#">Anuncie Conosco</a></li> -->
                    </ul>
                </div>
                <div>
                    <span class="subtitle-font-style">Social</span>
                    <ul>
                        <li style="width:48px;height: 48px" >
                            <a class="linkedin-link" target="_blank" rel="noreferrer nofollow" href="https://www.linkedin.com/company/cwbank-brasil/">
                                <img src="/static/icons/logotipo-do-linkedin.png" alt="linkedin" width="24" height="24" />
                            </a>
                        </li>
                        <li style="width:48px;height: 48px">
                            <a class="instagram-link" target="_blank" rel="noreferrer nofollow" href="https://www.instagram.com/emoney.cambio/">                            
                                <img src="/static/icons/logotipo-do-instagram.png" alt="instagram" width="24" height="24" />
                            </a>
                        </li>
                    </ul>
                    
                </div>`

    
    mainContent.append(footerElement)

});