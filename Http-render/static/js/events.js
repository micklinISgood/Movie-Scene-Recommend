var socket = io.connect('http://' + document.domain + ':' + 6888);
   socket.on('connect', function() {
   		// console.log("open");
        socket.emit('init', {data: 'I\'m connected!'});
   });


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
