$(document).ready(function(){

    $("#money-tourism").maskMoney({prefix:'$ ', thousands:'.', decimal:',', affixesStay: true});
    
    $("#money-tourism").keyup(function(e){
        // alert()
        let currentValue = onlyNumbers($(this).val())
        let feeValue = onlyNumbers($('input#fee_value').val())
        let newValue = parseFloat((currentValue/100) * (feeValue/100)).toFixed(2);
        $("#dynamic-total-value").text(newValue)
    })
})