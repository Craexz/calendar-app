dataElement = document.getElementById('data');
rawJson = dataElement.innerHTML;

const dataObj = JSON.parse([rawJson]);

var username_ = document.getElementById("usernameStorage").innerHTML

for(var i = 0; i < dataObj.length; i++) {
        var obj = dataObj[i];

        var obj = JSON.parse(JSON.stringify(obj));

        obj = obj.replace("{'name': '", "").replace("', 'description': '", "Ⓖ").replace("', 'duedate': '", "Ⓖ").replace("', 'id': ", "Ⓖ").replace("}", "");

        var finalData = obj.split('Ⓖ');

        var name_ = finalData[0];
        var desc = finalData[1];
        var duedate = finalData[2];
        var id = finalData[3];
      
        var TR = document.createElement('tr');
        var table = document.getElementById('assignments');
        
        table.append(TR);

        var nametd = document.createElement('td');
        var descriptiontd = document.createElement('td');
        var duedatetd = document.createElement('td');
        var deletetd = document.createElement('td');

        TR.append(nametd);
        TR.append(descriptiontd);
        TR.append(duedatetd);
        TR.append(deletetd);

        TR.id = id;
        
        var deleteBTN = document.createElement('a');
        deleteBTN.class = "button";
        deleteBTN.id = id;
        deleteBTN.innerHTML = "Delete";


        deleteBTN.href = '/deletebtn?id_='+deleteBTN.id+"&username="+username_;

        deletetd.appendChild(deleteBTN);

        nametd.innerHTML = name_;
        descriptiontd.innerHTML = desc;
        duedatetd.innerHTML = duedate;    
}