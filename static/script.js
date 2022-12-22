let timeoutID;
let timeout = 1000;

function setup(){
    document.getElementById("theButton").addEventListener("click", sendit);
}

function sendit(){
    const message = document.getElementById("message").value;

    fetch("/message/<room>", {
        method: "POST",
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: JSON.stringify(message)
    })
    .then((response) => {
        console.log(response.json())
        return response.json();
    })
    .then((result) => {
        console.log(result)
        updateMessages(result);
    })
    .catch(() => {
        console.log("Error posting your message!");
    });
}

function poller() {
	console.log("Polling for new items");
	fetch("/messages")
		.then((response) => {
			return response.json();
		})
		.then(updateTable)
		.catch(() => {
			console.log("Error fetching items!");
		});
}

function updateMessages(result){
    var list = document.getElementById("list");
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(result));
    list.appendChild(li);

    timeoutID = window.setTimeout(poller, timeout);
}

window.addEventListener("load", setup);
