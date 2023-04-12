function nextStepFormCustom(event) {
    // http://localhost:5656/remessa-internacional/dolar/pf/enviar/10000/111

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
        currentUrlPath = `/remessa-internacional/${data['coin']}/${data['person_type']}/${data['transaction']}/${data['value']}/${data['fee']}`
    }
    
    
    console.log(data, currentUrlPath)

    // location.href = currentUrlPath
    window.history.pushState({},"", currentUrlPath);
    nextStepForm(event)
}