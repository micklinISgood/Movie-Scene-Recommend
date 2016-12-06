
if (getCookie("mid")==""){
	setCookie("mid", "F2bk_9T482g", 360);
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
	  		console.log(ret);
	  		setCookie("mid", ret["mid"], 360);
	  		vid = document.getElementById("html-main-video");
	  		vid.src=ret["mlink"];
	  		vid.load();
	  		text= document.getElementById("main_video_name");
	  		text.innerHTML= ret["name"];
	  		rec = document.getElementById("recommendation-section");
	  		rec.innerHTML="";
	  		for( var i in ret["rec_list"]){
	  			var a = document.createElement('a');
	  			a.id=ret["rec_list"][i]["mid"];
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

	  });
}

function videoClick () {
	console.log(this);
	getVid(this.id);
	// body...
}
