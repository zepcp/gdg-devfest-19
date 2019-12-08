
$(document).ready(function() {

    var baseUrl = "http://localhost:5000/zomic"

    var Http = new XMLHttpRequest();

    var url_string = window.location.href
    var url = new URL(url_string);
    var wallet = "0x66B655a4CE711F00b570f9801c498071e9A15045";//url.searchParams.get("wallet");

    Http.open("GET", baseUrl+'/topics/get', false);
    Http.send();
    topicsData = JSON.parse(Http.responseText);
    var topice = document.getElementById("topic");
    var topic = "";
    for(var i = 0; i < topicsData.length; i++) {
        var opt = topicsData[i];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        topice.appendChild(el);
    }

    var titlee = document.getElementById("title");
    var title = titlee.value;

    var descriptione = document.getElementById("description");
    var description = descriptione.value;

    var deadlinee = document.getElementById("deadline");
    var deadline = deadlinee.value;

    //button click
    document.getElementById("submitButton").addEventListener("click", submitAction);

    function submitAction() {
        topic = topice.options[topice.selectedIndex].value;
        wallet = url.searchParams.get("wallet");
        description = descriptione.value;
        title = titlee.value;
        deadline = deadlinee.value;
        console.log(topic);
        console.log(wallet);
        console.log(title);
        console.log(description);
        console.log(deadline);

        var Http = new XMLHttpRequest();
        Http.open("POST", baseUrl+"/proposals/post", false);
        Http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        Http.send("topico="+topic+"&wallet="+wallet+"&description="+description+"&title="+title+"&deadline="+deadline);

    }


});