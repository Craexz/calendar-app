var username_ = document.getElementById("usernameStorage").innerHTML;

var token = document.getElementById("token").innerHTML;

document.cookie = "token="+token+"; username="+username_+";";