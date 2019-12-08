$(document).ready(function() {

    var baseUrl = "http://localhost:5000/zomic"

    var url = new URL(window.location.href);
    var c = 1;//url.searchParams.get("id");
    console.log(c);

    const Http = new XMLHttpRequest();
    Http.open("GET", baseUrl+'/proposals/get?id='+c, false);
    Http.send();
    propData = JSON.parse(JSON.parse(Http.responseText));

    $("#title").text(propData["title"]);
    $("#description").text(propData["description"]);
    $("#topic").text(propData["topic"]);
    $("#status").text(propData["status"]);
    $("#deadline").text(propData["deadline"]);

});