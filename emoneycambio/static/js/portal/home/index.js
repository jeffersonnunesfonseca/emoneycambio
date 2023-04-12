function sendFormPrice(e) {
    e.preventDefault();
    let searchCoin = document.getElementById("search-coin").value
    let searchLocation = document.getElementById("search-location").value
    console.log(searchCoin)
    console.log(searchLocation)

    if (forceValidation(['search-coin', 'search-location']) == "stop") {
        return
    }

    
    return window.location = `/cotacao/${searchCoin}/${searchLocation}`
}