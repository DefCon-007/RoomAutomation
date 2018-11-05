var spellAnimation = bodymovin.loadAnimation({
    container: document.getElementById("potter-animation"),
    renderer: "svg",
    loop: false,
    autoplay: false,
    path: "https://raw.githubusercontent.com/abrahamrkj/facebook-spell/master/data.json"
});
console.log("Initialesed")
var base_url = window.location.origin;

$(".wand").click(function() {
    spellAnimation.stop();
    spellAnimation.play();
});


$(".on").click(function() {
    var url = base_url + "/lumos"
    console.log(url)
   var xhr = new XMLHttpRequest();
xhr.open('GET', url, true);
xhr.send();
});


$(".off").click(function() {
    var url = base_url + "/nox"
    console.log(url)
   var xhr = new XMLHttpRequest();
xhr.open('GET', url, true);
xhr.send();
});


$(".blon").click(function() {
    var url = base_url + "/bluemos"
    console.log(url)
   var xhr = new XMLHttpRequest();
xhr.open('GET', url, true);
xhr.send();
});


$(".bloff").click(function() {
    var url = base_url + "/blueox"
    console.log(url)
   var xhr = new XMLHttpRequest();
xhr.open('GET', url, true);
xhr.send();
});


$(".rndon").click(function() {
    var url = base_url + "/randomcoloron"
    console.log(url)
   var xhr = new XMLHttpRequest();
xhr.open('GET', url, true);
xhr.send();
});


$(".rndoff").click(function() {
    var url = base_url + "/randomcoloroff"
    console.log(url)
   var xhr = new XMLHttpRequest();
xhr.open('GET', url, true);
xhr.send();
});


function sendMonitorData(pos) {
    var url = base_url + "/setMonitor"
    console.log(url)
    const params = "pos="+pos 
   var xhr = new XMLHttpRequest();
xhr.open('GET', url + "?"+, true);
xhr.send();
}

$("#monitorTop").click(function() {

    var color = $("#picker").spectrum("get");
    console.log(color)
    sendMonitorData("top")
});



