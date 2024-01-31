/*
 * Removes (hides) the error message on the login page.
 */
function removeLoginErrorMessage() {
    document.getElementById("input-error-msg").style.display = "none";
}

document.getElementById("username-input").addEventListener("click", removeLoginErrorMessage);
document.getElementById("password-input").addEventListener("click", removeLoginErrorMessage);
