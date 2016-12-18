
//document.domain, '54.221.40.5'
var socket = io.connect('http://' + document.domain + ':' + 6888);
  
socket.on('connect', function() {

   });

socket.on('message', function(message) {
   		 console.log(message);
   		 var action = JSON.parse(message);
    	 // alert(action["action"]);
    	 if(action["action"] == "rec") printRecList(action["rec_list"]);
    	 if(action["action"] == "recScene") printSceneRecList(action["rec_list"]);
   		 // alert(message);

   });

logoutbtn = document.getElementById("logout");
logoutbtn.onclick = nullCookie;


function printRecList(list){
	console.log(list);
	table = document.getElementById("recommend");
	table.innerHTML = "";

	t =document.createElement('table');
	var row1 = t.insertRow(0);
	var row2 = t.insertRow(1);
	
	for(var i in list){
		

		var cell1 = row1.insertCell(-1);
		var cell2 = row2.insertCell(-1);
		cell1.style = "color: #e6ffff;"
		cell1.innerHTML = list[i][0];
		var cell3 = row1.insertCell(-1);
		cell3.innerHTML = " ";

		cell2 = row2.insertCell(-1);
		cell2.innerHTML = list[i][1];
		cell2.style = "color: #e6ffff;"
	

	}
	p = document.createElement('p');
	p.style = "color: #e6ffff;"
	p.innerHTML = "ALS Recommendation List:";
	p.appendChild(t)
	table.appendChild(p);


}
function printSceneRecList(list){
	table = document.getElementById("recommendScene");
	table.innerHTML = "";
	table.innerHTML = "";

	t =document.createElement('table');
	var row1 = t.insertRow(0);
	var row2 = t.insertRow(1);
	
	for(var i in list){
		

		var cell1 = row1.insertCell(-1);
		var cell2 = row2.insertCell(-1);
		cell1.style = "color: #e6ffff;"
		cell1.innerHTML = list[i][0];
		var cell3 = row1.insertCell(-1);
		cell3.innerHTML = " ";

		cell2 = row2.insertCell(-1);
		cell2.innerHTML = list[i][1];
		cell2.style = "color: #e6ffff;"

	}
	p = document.createElement('p');
	p.style = "color: #e6ffff;"
	p.innerHTML = "Scene Recommendation List:";
	p.appendChild(t)
	table.appendChild(p);
}



function nullCookie () {
	setCookie("uid", "", 0);
	setCookie("mid", "", 0);
	location.reload();
	// body...
}

getVid(getCookie("mid"));

function getVid(mid) {

	data ={};
	data["uid"]=getCookie("uid");
    if(data["uid"]=="")data["uid"]=0;
    data["mid"]=mid;
    // console.log(data);
	$.getJSON('http://'+ window.location.host + '/getmid', data, function(data) {
	  		ret= data.data;
	
	  		if(ret["mid"]==null) return false;
	  		//console.log(ret);
	  		setCookie("mid", ret["mid"], 360);
	  		vid = document.getElementById("html-main-video");
	  		vid.src=ret["mlink"];
	  		vid.load();
	  		text= document.getElementById("main_video_name");
	  		text.innerHTML= ret["name"];
	  		rec = document.getElementById("recommendation-section");
	  		rec.innerHTML="";
	  		list_id =[];
	  		for( var i in ret["rec_list"]){
	  			var a = document.createElement('a');
	  			a.id=ret["rec_list"][i]["mid"];
	  			list_id.push(ret["rec_list"][i]["mid"])
	  			a.onclick = videoClick; 
	  			img= document.createElement('img');
	  			img.src=ret["rec_list"][i]["mimg"];
	  			a.appendChild(img);
	  			p= document.createElement('p');
	  			p.innerHTML=ret["rec_list"][i]["name"];
	  			a.appendChild(p);
	  			rec.appendChild(a);
	  		}
	  		
	  		last_m=[];
	  		vid.play();
	  		track_rec_list (list_id);

	  });
}

function videoClick () {
	// console.log(this);

	getVid(this.id);
	data ={}
	var uid = getCookie("uid");
    if(uid==""){
        data["uid"]="non-login";
    }else{
        data["uid"]=uid;
    }
    data["mid"]=this.id;
    data["epoch"]=new Date().getTime();
    socket.emit('click_video', data);

}

function track_rec_list (rec_list) {
	
	data ={}
	var uid = getCookie("uid");
    if(uid==""){
        data["uid"]="non-login";
    }else{
        data["uid"]=uid;
    }
    data["rec_list"]=rec_list;
    data["epoch"]=new Date().getTime();
    socket.emit('rec_list', data);

}
