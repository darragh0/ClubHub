const hamburger = document.querySelector(".navbar-right a");
const navbar_divs = document.querySelectorAll(".navbar-center");
const height = "2.75rem";
let hamburger_expanded = false;
let page_name = window.location.pathname.substring(1);

if (page_name === "")
    page_name = "none"

let active_anchor = document.querySelector("." + page_name + "-link");

if (!active_anchor.parentElement.classList.contains("nav-active-link"))
    active_anchor.parentElement.classList.add("nav-active-link");

console.log(active_anchor)

// Toggle dropdown menu for smaller screens.
hamburger.addEventListener("click", () => {
    if (hamburger_expanded) {
        for (let div of navbar_divs) {
            div.style.height = 0;
        }
        hamburger_expanded = false;
    } else {
        for (let div of navbar_divs) {
            div.style.height = height;
        }
        hamburger_expanded = true;
    }
});
