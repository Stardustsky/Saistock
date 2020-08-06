function nine_change() {
    var httpRequest = new XMLHttpRequest();
    var curr_url = document.URL;
    var args = "get_nine_change=1";
    httpRequest.open('post', curr_url, true);
    httpRequest.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    httpRequest.send(args);
}

function show_yb(content) {
    alert(content);
}