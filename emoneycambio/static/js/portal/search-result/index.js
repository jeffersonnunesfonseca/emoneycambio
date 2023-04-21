function goToNegotiation(event, type, companyBranchId, negotiationType) {
    event.preventDefault()
    let currentUrlPath = document.location.pathname
    let newUrl = currentUrlPath.replace('cotacao', `negociacao/${type}/${negotiationType}`) + "/" + companyBranchId 
    console.log(companyBranchId, type, currentUrlPath, negotiationType, newUrl)
    location.href = newUrl

}