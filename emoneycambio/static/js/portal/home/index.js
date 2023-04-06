function showOptionsFormPrice (e) {

    let curTarget = e.currentTarget

    clearFeatsFormPrice()
    
    curTarget.classList.add('shadow')

    for (const child of curTarget.children) {
        if (child.tagName == 'UL') {
            child.style.display = "block";
        }
    }
    
}

function selectValueFromUl(e) {
    console.log(e.target)
}

function clearFeatsFormPrice() {

    let coinSelect = document.getElementById("coin-select")
    let locationSelect = document.getElementById("location-select")
    let customOptions = document.querySelectorAll("#custom-options")

    for (const option of customOptions) {
        option.style.display="none"
    }

    locationSelect.classList.remove("shadow")
    coinSelect.classList.remove("shadow")

}