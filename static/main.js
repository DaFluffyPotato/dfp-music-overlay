function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function update() {
	var song_data = JSON.parse(httpGet("update"));
	if (song_data["title"] != document.getElementById("title").innerHTML) {
		document.getElementById("title").innerHTML = song_data["title"];
		document.getElementById("artist").innerHTML = song_data["artist"];
		document.getElementById("album").innerHTML = "Album: " + song_data["album"];
		var timestamp = new Date().getTime();  
		document.getElementById("cover").src = "static/cover.png?t=" + timestamp;
		document.getElementById("bg-cover").style.backgroundImage = "url('static/cover.png?t=" + timestamp + "')";
	}
}

var interval = setInterval(update, 500);