var checkedTokenObj = document.getElementById("checkedToken");
var checkedToken = checkedTokenObj.innerText;

if (checkedToken == "DONE") {
  console.log("Token already checked");
}else {
  var token = window.localStorage.getItem('token');
  var username = window.localStorage.getItem('username');
      
  window.location.href = "/loginwithtoken?token="+token+"&username="+username;
}






