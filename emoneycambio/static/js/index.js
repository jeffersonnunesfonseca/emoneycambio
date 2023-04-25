$(document).ready(function() {
    
    setInterval(() => {
        // macete para desabilitar autocomple cpf 
        $("input[type='text']").attr('autocomplete', 'off');        
    }, 500);
    
    function matchStart(params, data) {

        if ($.trim(params.term) === '') {
            return data;
        }
      
        // `data.children` contains the actual options that we are matching against
        var filteredChildren = [];
        
        if (clearAccentuation(data.text).toUpperCase().indexOf(clearAccentuation(params.term).toUpperCase()) == 0) {
            filteredChildren.push(data);
        }

        // If we matched any of the timezone group's children, then set the matched children on the group
        // and return the group object
        if (filteredChildren.length) {
          var modifiedData = $.extend({}, data, true);
          modifiedData.children = filteredChildren;
      
          // You can return modified objects from here
          // This includes matching the `children` how you want in nested data sets
          return modifiedData;
        }
      
        // Return `null` if the term should not be displayed
        return null;
    }

    $('#phone').mask('(00) 00000-0000');
      
    $(".filter-select").select2({
        // matcher: matchStart
        minimumResultsForSearch: -1 //desabilita o buscador
    });

    updateBulletCoin()
    setInterval(function(){
        updateBulletCoin()
    }, 300000);

    
    const mainContent = document.getElementById("#content")
    const footerElement = document.createElement("footer")
    footerElement.innerHTML = `<div>
                    <a href="/">
        
                        <img src="/static/images/logo.png" alt="facebook" width="120"  height="120"/>
                    </a>
                </div>
        
                <div>
                    <span class="subtitle-font-style">Institucional</span>
                    <ul>
                        <li><a rel="noreferrer nofollow" href="/quem-somos/">Quem Somos</a></li>
                        <li><a rel="noreferrer nofollow" href="/termos-de-uso/">Termos de uso</a></li>
                        <li><a rel="noreferrer nofollow" href="/politicas-de-privacidade/">Políticas de privacidade</a></li>
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
                            <a target="_blank" rel="noreferrer nofollow" href="https://www.linkedin.com/company/cwbank-brasil/">
                                <img src="/static/icons/logotipo-do-linkedin.png" alt="linkedin" width="24" height="24" />
                            </a>
                        </li>
                        <li style="width:48px;height: 48px">
                            <a target="_blank" rel="noreferrer nofollow" href="https://www.instagram.com/emoney.cambio/">                            
                                <img src="/static/icons/logotipo-do-instagram.png" alt="instagram" width="24" height="24" />
                            </a>
                        </li>
                    </ul>
                </div>`

    
    mainContent.append(footerElement)

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

    response = ajaxReplaceHtmlToResponse(newUrl,'POST', data, step, form)
    window.history.pushState({},"", newUrl);
}

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