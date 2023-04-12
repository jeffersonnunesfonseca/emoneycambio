$(document).ready(function() {

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

      
    $("select").select2({
        matcher: matchStart
    });
    
    const mainContent = document.getElementById("#content")
    const footerElement = document.createElement("footer")
    footerElement.innerHTML = `<div>
                    <a href="/">
        
                        <img src="/static/images/logo.png" alt="facebook" width="120" />
                    </a>
                </div>
        
                <div>
                    <span class="subtitle-font-style">Institucional</span>
                    <ul>
                        <li><a href="#">Quem Somos</a></li>
                        <li><a href="#">Termos de uso</a></li>
                        <li><a href="#">Políticas de privacidade</a></li>
                    </ul>
                </div>
                <div>
                    <span class="subtitle-font-style">Serviços</span>
                    <ul>
                        <li><a href="#">Remessas</a></li>
                        <li><a href="#">Papel/Moeda</a></li>
                        <li><a href="#">Anuncie Conosco</a></li>
                    </ul>
                </div>
                <div>
                    <span class="subtitle-font-style">Social</span>
                    <ul>
                        <li>
                            <a target="_blank" rel="noreferrer nofollow" href="https://www.linkedin.com/company/cwbank-brasil/">
                                <img src="/static/icons/logotipo-do-linkedin.png" alt="facebook" width="24" />
                            </a>
                        </li>
                        <li>
                            <a target="_blank" rel="noreferrer nofollow" href="https://www.instagram.com/emoney.cambio/">                            
                                <img src="/static/icons/logotipo-do-instagram.png" alt="instagram" width="24" />
                            </a>
                        </li>
                    </ul>
                </div>`

    
    mainContent.append(footerElement)

});

// const mainContent = document.getElementById("#content")