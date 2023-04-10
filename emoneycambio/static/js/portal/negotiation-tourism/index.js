$(document).ready(function() {
    $("#money").maskMoney({prefix:'R$ ', thousands:'.', decimal:',', affixesStay: true});
   
    $('#phone').mask('(00) 00000-0000');

    $("#cpfcnpj").keydown(function(){
        try {
            $("#cpfcnpj").unmask();
        } catch (e) {}
    
        var tamanho = $("#cpfcnpj").val().length;
    
        if(tamanho < 11){
            $("#cpfcnpj").mask("999.999.999-99");
        } else {
            $("#cpfcnpj").mask("99.999.999/9999-99");
        }
    
        // ajustando foco
        var elem = this;
        setTimeout(function(){
            // mudo a posição do seletor
            elem.selectionStart = elem.selectionEnd = 10000;
        }, 0);
        // reaplico o valor para mudar o foco
        var currentValue = $(this).val();
        $(this).val('');
        $(this).val(currentValue);
    });
});

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
        keys.push(obj.name)
    });
    

    console.log(keys);
    console.log(data)
    
    if (forceValidation(keys) == "stop") {
        return
    }

    if (data["nextstep"] == "2") {

        let moneyInput = document.getElementById("money")
        let moneyValue = data["money"].replace("R$", "").trim()
        if (parseFloat(moneyValue) < 100) {
            money.classList.add("check-value")
            return
        }
    }



    let newUrl = `${currentUrlPath}?step=${data['nextstep']}`

    console.log(data, newUrl)
    response = ajaxReplaceHtmlToResponse(newUrl,'POST', data, step, form)
    window.history.pushState({},"", newUrl);

    // console.log(response)


}