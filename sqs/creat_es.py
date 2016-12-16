import json
from pyes import *
from dateutil import parser
from HTMLParser import HTMLParser
import ast



if __name__ == '__main__':

    conn = ES('https://search-test-qmyiuzwgkz4c6jmlzhhy6p2t7y.us-east-1.es.amazonaws.com/')
    try:  
        conn.indices.delete_index("watch_interval")
        conn.indices.delete_index("rec_list")
        conn.indices.delete_index("click_video")
        
    except:
        pass
    event_list = ["watch_interval", "rec_list", "click_video"]
    for event in event_list:
        conn.indices.create_index(event)
        if event == "watch_interval":
            mapping={"event":{"type": "string","index": "not_analyzed"},"watch_interval":{"type": "string"},"uid":{"type": "string"}, "remote_addr":{"type": "string"},
            "mid":{"type": "string"}, "epoch":{"type": "string"}}

        elif event == "rec_list":
            mapping={"event":{"type": "string","index": "not_analyzed"},"rec_list":{"type": "string"},"uid":{"type": "string"}, "remote_addr":{"type": "string"},
             "epoch":{"type": "string"}}

        else:
            mapping={"event":{"type": "string","index": "not_analyzed"},"uid":{"type": "string"}, "remote_addr":{"type": "string"},
            "mid":{"type": "string"}, "epoch":{"type": "string"}}



    # mapping={'longitude':{'store':'yes','type':'float'},'latitude':{'store':'yes','type':'float'},'message':{'store':'yes','type':'string'}}
        conn.indices.put_mapping("test-type",{'properties':mapping}, [event])



    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    

