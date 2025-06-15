

window.addEventListener("load", (event) => {
    const togleButton = document.querySelector(".btn-toggle");
    console.log(togleButton)
    const togleButtonIconClose = document.querySelector(".btn-toggle .icon-close");
    const togleButtonIconOpen = document.querySelector(".btn-toggle .icon-burger");

    const dropDownMenu = document.querySelector(".dropdown-menu");


    togleButton.addEventListener("click", (e) => {
        dropDownMenu.classList.toggle("open");

        const isOpen = dropDownMenu.classList.contains("open");
        if (isOpen){
            togleButtonIconClose.classList.add("open-icon")
            togleButtonIconOpen.classList.remove("open-icon")

        }else{
            togleButtonIconClose.classList.remove("open-icon")
            togleButtonIconOpen.classList.add("open-icon")
        }
    });
});