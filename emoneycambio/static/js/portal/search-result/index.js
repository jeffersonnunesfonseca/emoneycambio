function goToNegotiation(event, type, companyId, negotiationType) {
    event.preventDefault()
    let currentUrlPath = document.location.pathname
    let newUrl = currentUrlPath.replace('cotacao', `negociacao/${type}/${negotiationType}`) + "/" + companyId 
    console.log(companyId, type, currentUrlPath, negotiationType, newUrl)
    location.href = newUrl

}