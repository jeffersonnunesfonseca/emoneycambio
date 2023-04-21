$(document).ready(function(){

    $("#money-tourism").maskMoney({prefix:'$ ', thousands:'.', decimal:',', affixesStay: true});
    $('#phone').mask('(00) 00000-0000');
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
})


