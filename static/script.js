const hamburger = document.getElementById("hamburger");
const links = document.getElementsByClassName("navbar-center");
const height = "2.75rem";
let hamburger_expanded = false;


/*
 * Toggle dropdown menu for smaller screens.
 */
function toggleHamburger() {
    if (hamburger_expanded) {
        for (let div of links) {
            div.style.height = 0;
            // div.children[0].style.opacity = 0;
        }
        hamburger_expanded = false;
    } else {
        for (let div of links) {
            div.style.height = height;
            // div.children[0].style.opacity = 1;
        }
        hamburger_expanded = true;
    }
}


hamburger.addEventListener("click", toggleHamburger);

let navbar_divs = document.getElementsByClassName("navbar-center")
let page_name = window.location.pathname

for (let div of navbar_divs) {
    for (let anchor of div.children) {
        if (page_name === anchor.pathname) {
            if (!anchor.parentElement.classList.contains("active"))
                anchor.parentElement.classList.add("active");
        } else {
            if (anchor.parentElement.classList.contains("active"))
                anchor.parentElement.classList.remove("active");
        }
    }
}
