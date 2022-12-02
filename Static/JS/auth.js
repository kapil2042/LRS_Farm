var headlogin = document.getElementById('headlogin');
function login() {
    var login = document.getElementById('modalbodylogin');
    var forgot = document.getElementById('modalbodyforgot');
    login.classList.remove('hidden');
    forgot.classList.add('hidden');
    headlogin.innerHTML = "Sign in to your account";
}
function forgotpass() {
    var login = document.getElementById('modalbodylogin');
    var forgot = document.getElementById('modalbodyforgot');
    login.classList.add('hidden');
    forgot.classList.remove('hidden');
    headlogin.innerHTML = "Forgot your Password";
}