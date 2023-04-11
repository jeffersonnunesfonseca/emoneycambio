$(document).ready(function() {
    $("#money").maskMoney({prefix:'R$ ', thousands:'.', decimal:',', affixesStay: true});
   
    $('#phone').mask('(00) 00000-0000');

    // $("#cpfcnpj").keydown(function(){
    //     console.log("cpfcnpj")
    //     try {
    //         $("#cpfcnpj").unmask();
    //     } catch (e) {}
    
    //     var tamanho = $("#cpfcnpj").val().length;
    
    //     if(tamanho < 11){
    //         $("#cpfcnpj").mask("999.999.999-99");
    //     } else {
    //         $("#cpfcnpj").mask("99.999.999/9999-99");
    //     }
    
    //     // ajustando foco
    //     var elem = this;
    //     setTimeout(function(){
    //         // mudo a posição do seletor
    //         elem.selectionStart = elem.selectionEnd = 10000;
    //     }, 0);
    //     // reaplico o valor para mudar o foco
    //     var currentValue = $(this).val();
    //     $(this).val('');
    //     $(this).val(currentValue);
    // });
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
        if (obj.name =='pfpj' || obj.name == 'delivery'){

        }else{

            keys.push(obj.name)
        }

    });
    

    console.log(keys);
    console.log(data)
    
    if (forceValidation(keys) == "stop") {
        return
    }

    if (data["nextstep"] == "2") {

        let moneyInput = document.getElementById("money")
        let moneyValue = moneyInput.value.replace("R$", "").trim()
        console.log((parseFloat(onlyNumbers(moneyValue)/100)))
        if ((parseFloat(onlyNumbers(moneyValue))/100) < 100) {
            moneyInput.classList.add("check-value")
            return
        }
    }

    let newUrl = `${currentUrlPath}?step=${data['nextstep']}`

    console.log(data, newUrl)
    response = ajaxReplaceHtmlToResponse(newUrl,'POST', data, step, form)
    window.history.pushState({},"", newUrl);

    // console.log(response)


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

    // var tamanho = onlyNumbers(elem.value).length;
    // console.log(tamanho)
    // if(tamanho > 11){
    // } else {
 
    // }

    // ajustando foco
    // var elem = this;
    // setTimeout(function(){
    //     // mudo a posição do seletor
    //     elem.selectionStart = elem.selectionEnd = 10000;
    // }, 0);
    // // // reaplico o valor para mudar o foco
    // var currentValue = elem.value
    // console.log(currentValue)
    // elem.value = currentValue
    // $(this).val('');
    // $(this).val(currentValue);

}