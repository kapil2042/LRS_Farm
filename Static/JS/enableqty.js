function enableDisable(bEnable, textBoxID) {
    for (let index = 1; index <= 100 ; index++) {
        document.getElementById(textBoxID+textBoxID+index).disabled = !bEnable
        document.getElementById(textBoxID+index).disabled = !bEnable
    }
}