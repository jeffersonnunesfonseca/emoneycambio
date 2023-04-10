function goToNegotiation(event, type, companyId, negotiationType) {
    // negociacao/comprar/papel-moeda/dolar/sao-paulo-sp/1
    //  cotacao/euro/sao-paulo-sp
    event.preventDefault()
    let currentUrlPath = document.location.pathname
    let newUrl = currentUrlPath.replace('cotacao', `negociacao/${type}/${negotiationType}`) + "/" + companyId 
    console.log(companyId, type, currentUrlPath, negotiationType, newUrl)
    location.href = newUrl

}