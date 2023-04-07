function showOptionsFormPrice (e) {

    let curTarget = e.currentTarget

    clearFeatsFormPrice()
    
    curTarget.classList.add('shadow')

    let searchCoin = document.getElementById("search-coin")
    let searchLocation = document.getElementById("search-location")
    if (curTarget.id == 'coin-select') {
        if (!searchCoin.classList.contains('focus-input-search')) {
            searchLocation.classList.remove('focus-input-search')
            searchCoin.classList.add('focus-input-search')
            searchCoin.focus()
        }
        
    } else {
        if (!searchLocation.classList.contains('focus-input-search')) {
            searchCoin.classList.remove('focus-input-search')
            searchLocation.classList.add('focus-input-search')
            searchLocation.focus()
        }

    }

    for (const child of curTarget.children) {
        if (child.tagName == 'UL') {
            child.style.display = "block";
        }
    }
    
}

function selectValueFromUl(e) {
    e.stopPropagation()
    console.log(e.target)
    let search = e.target.parentNode.parentNode
    let searchCoin = document.getElementById("search-coin")
    let searchLocation = document.getElementById("search-location")
    console.log(search.id)
    if (search.id == 'coin-select') {
        searchCoin.value = e.target.innerText
    }
    else {
        searchLocation.value = e.target.innerText

    }
    clearFeatsFormPrice()
}

function clearFeatsFormPrice() {

    console.log("limpa feats")
    let coinSelect = document.getElementById("coin-select")
    let locationSelect = document.getElementById("location-select")
    let customOptions = document.querySelectorAll("#custom-options")
    let searchCoin = document.getElementById("search-coin")
    let searchLocation = document.getElementById("search-location")

    for (const option of customOptions) {
        option.style.display="none"
    }

    locationSelect.classList.remove("shadow")
    coinSelect.classList.remove("shadow")
    searchCoin.classList.remove('focus-input-search')
    searchLocation.classList.remove('focus-input-search')

}

function filter(e) {
    var input = e.currentTarget
    let ulElement = false

    for (const child of input.parentNode.parentNode.children) {
        if (child.tagName == 'UL') {
            console.log('a')
            ulElement=child
            break
        }
        
    }

    var filter = input.value.toUpperCase();
    var lis = ulElement.children;
    console.log(lis)
    console.log(ulElement)
    for (var i = 0; i < lis.length; i++) {
        console.log(lis[i].innerText)
        // var name = lis[i].getElementsByClassName('name')[0].innerHTML;
        if (lis[i].innerText.toUpperCase().indexOf(filter) == 0) 
            lis[i].style.display = 'list-item';
        else
            lis[i].style.display = 'none';
    }

}