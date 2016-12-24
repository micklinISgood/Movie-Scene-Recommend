# Movie-Scene-Recommend

###demo Video
[![demo](https://img.youtube.com/vi/cs7U9zyJlho/0.jpg)](https://www.youtube.com/watch?v=cs7U9zyJlho)

###Architecture
![http://localhost:5566](https://github.com/micklinISgood/Movie-Scene-Recommend/blob/master/arch/CloudFinalArch3.png)

###Data model
```java

{
    "event": "watch_interval",
    "watch_interval": "20.008688:21.172696",
    "uid": "cl3469@columbia.edu",
    "remote_addr": "160.39.12.174",
    "mid": "7",
    "epoch": 1481127735559
}
{
    "event": "click_video",
    "epoch": 1481127679816,
    "remote_addr": "160.39.12.174",
    "uid": "cl3469@columbia.edu",
    "mid": "7"
}
{
    "event": "rec_list",
    "rec_list": ["7", "128648", "99822", "84374", "113775"],
    "epoch": 1482187923192,
    "uid": "lol",
    "remote_addr": "160.39.142.183"
}

```

##HTTP render-engine
###User watch_interval event catch: 
we use html5 <video> tag to play the videos which we hosted on S3. video tag api provides onplay , onpause, ontimeupdate and onseeked callback to listen on. However, when onseeked is triggered, the video’s current time will ping to the seeked position. We desired to get the final time position before the video was seeked. Here, we keep an array to push all the current time of the video while ontimeupdate is triggered. Therefore, when onseeked is triggered, we can look up the array to get the final time position before seeked. Below is the code sample. And we pass the interval with key “watch_interval” to backend, where 3rd time from the end of array is the time before seeked is triggered. 
[Full code](https://github.com/micklinISgood/Movie-Scene-Recommend/blob/master/Http-render/static/js/home.js)
```js
data["watch_interval"]=start+":"+last_m[last_m.length-3];
```

###In-memory Random recommendation list by Flask: 
We load our 36 movie meta [data](https://github.com/micklinISgood/Movie-Scene-Recommend/blob/master/Http-render/static/joined.csv) which is already joined with MovieLen’s id  to memory and  generate a random list from it. Here is our schema {“category”,“snapshot”,“name”,”vid”,“length”,“S3 playable url”, “mid”}. For each category, we have 4 movies. The random recommendation list’s input is mid, also the id in MovieLen, and it’s output is a list without itself. To keep the list relevant, we set the first element of the list is one from the same category and the rest of 4 elements are picked from the rest of 34 videos randomly. 
[Code Section](https://github.com/micklinISgood/Movie-Scene-Recommend/blob/master/Http-render/application.py#L130-L169)

##Websocket-engine 
###Multi-session broadcast: 
We utilized the Flask socketIO to broadcast the asynchronous response from the recommender based on a user id which may have several sessions online. The main issue for this part initially is that we only consider that a user can only have a session at a time. In this scenario, only one session, one tab, will receive the response from the recommender if there are two tabs with the same user id browsing our application. Here is the best practice to solve this issue, where room=uid, line 7, means that emit the message to a room named uid which contains all the sessions of uid. SidToUid is a dictionary to track which session belongs which uid. 
[Full code](https://github.com/micklinISgood/Movie-Scene-Recommend/blob/master/websocket-engine/app.py)
```python
def sendRecommendation(uid, rec_list):
   if uid in SidToUid.values():
       data = {}
       data["action"] = "rec"
       data["rec_list"] = rec_list
       try:                 
            emit('message',json.dumps(data),room=uid)
       except Exception as e:
           cleanUserByUid(uid)
           print e
```

###Event sourcing via SNS+SQS: 
we take advantage of AWS queue service to pass out the user event data to SQS from a SNS. One SQS worker will persist all the user log for historical query if needed. The other SQS worker directly processed the event data and invoke the spark ALS recommender to give the recommendation response. 
[Code Section](https://github.com/micklinISgood/Movie-Scene-Recommend/blob/master/websocket-engine/app.py#L71-L74)

##Recommender through spark ALS
###In-memory rating accumulation & multi-thread recommendation per event: 
we defined a global dictionary to store the converted ratings collectively. Then, for each valid event, we will send the accumulated ratings lists of list per uid to the spark instance. 
[Full code](https://github.com/micklinISgood/Movie-Scene-Recommend/blob/master/recommender/rating.py)

###Spark ALS recommendation: 
For responsiveness sake, we use movieLen small dataset to recompute the ALS model per event. Since ALS needs to give out the recommendation of unseen movies, we need to feed new rating table of a user to it after every event. Then, recompute the model to get the recommendation list. There are 9125 movies in the MovieLen small dataset. Therefore, we present the string updation in the front end because we only got 36 of them hosted. 
[Code Section](https://github.com/micklinISgood/Movie-Scene-Recommend/blob/master/recommender/engine.py#L129-L155)
