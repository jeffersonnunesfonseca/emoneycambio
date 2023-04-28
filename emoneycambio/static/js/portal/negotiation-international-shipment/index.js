$(document).ready(function() {

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
});

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
