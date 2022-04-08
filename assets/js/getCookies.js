var token = window.localStorage.getItem('token');
var username = window.localStorage.getItem('username');


window.location.href = "/loginwithtoken?token="+token+"&username="+username;
