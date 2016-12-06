// get User info

// var currentUser = getUser();


// should get it from db
var likeMainVideo = false;
var thumbUp = false;
var thumbDown= false;


function getMainVideoIconByClassName(iconClassName){
    return document.getElementById("html-main-video-section").getElementsByClassName(iconClassName)[0];
}

var likeMainVideoIcon = getMainVideoIconByClassName('fa-heart-o');
var dislikeMainVideoIcon = getMainVideoIconByClassName('fa-heart');
var thumbUpIcon = getMainVideoIconByClassName('fa-thumbs-o-up');
var unThumbUpIcon= getMainVideoIconByClassName('fa-thumbs-up');
var thumbDownIcon = getMainVideoIconByClassName('fa-thumbs-o-down');
var unThumbDownIcon= getMainVideoIconByClassName('fa-thumbs-down');

// toggle movie like


var addToggleLikeIconListener = function(icon){

    console.log("icon", icon)
	icon.addEventListener("click", function(){
	likeMainVideo = !likeMainVideo;
        console.log(likeMainVideo);
	});
}

var addToggleThumbUpIconListener = function(icon){
    icon.addEventListener("click", function(){
    thumbUp = !thumbUp;
        console.log(thumbUp);
    });
}

var addToggleThumbDownIconListener = function(icon){
    icon.addEventListener("click", function(){
    thumbDown = !thumbDown;
        console.log(thumbDown);
    });
}

addToggleLikeIconListener(likeMainVideoIcon );
addToggleLikeIconListener(dislikeMainVideoIcon);
addToggleThumbUpIconListener(thumbUpIcon );
addToggleThumbUpIconListener(unThumbUpIcon);
addToggleThumbDownIconListener(thumbDownIcon );
addToggleThumbDownIconListener(unThumbDownIcon);

// send movie like to database



//add interval
var last_m=[],start;
var myVideo = document.getElementById("html-main-video");
myVideo.ontimeupdate = show;
myVideo.onplay = play;
myVideo.onpause= pause;
myVideo.onseeked= seeked;
myVideo.controls = true;

function seeked(){
        start = myVideo.currentTime;
        myVideo.play();
        console.log("play video");
}
function show(){
        last_m.push(myVideo.currentTime);
        console.log("show");
}
function play() {
        start = myVideo.currentTime;
        console.log("start");

}
function pause() {

    console.log("pause");
      
    console.log("watched interval:"+start+":"+last_m[last_m.length-3]);
        //upload interval here

    last_m=[];
}
function makeBig() {
    console.log("make large");
    myVideo.width = 560;
}
function makeSmall() {
    console.log("make small");
    myVideo.width = 320;
}
function makeNormal() {
    console.log("make normal");
    myVideo.width = 420;
}

function addTrackLinkListenerFunction(){
    var recommendationList = document.getElementsByClassName("recommended-movie");
    console.log("hihihi", recommendationList);
    for (var i = 0; i < recommendationList.length ; i++){
        recommendationList[i].addEventListener("click", function(event){
            event.preventDefault();
            console.log("clicked on link", event.target.parentNode.getAttribute('href'));
        });
    }
}

addTrackLinkListenerFunction();



// *N*play
// *N*slow
// Quality Change

