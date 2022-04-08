var username_ = document.getElementById("usernameStorage").innerHTML;

var token = document.getElementById("token").innerHTML;

window.localStorage.setItem('username', username_);
window.localStorage.setItem('token', token);

