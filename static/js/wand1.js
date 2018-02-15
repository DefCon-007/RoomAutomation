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
xhr.open('GET', url, false);
xhr.send();
});
