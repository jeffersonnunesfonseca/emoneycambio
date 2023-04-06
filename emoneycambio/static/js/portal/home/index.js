function showOptions (e) {
    console.log(e.currentTarget)
    let curTarget = e.currentTarget
    // curTarget.classList.toggle('shadow')
    curTarget.classList.add('shadow')

    // console.log(curTarget.children)
    for (const child of curTarget.children) {
        console.log(child.tagName);
        if (child.tagName == 'UL') {
            console.log(child)
            child.style.display = "block";
 
            // if (child.style.display === "none") {
            // } else {
            //     child.style.display = "none";
            // }
        }
      }
}