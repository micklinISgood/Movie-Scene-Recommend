import sys

from pyspark import SparkContext


from HTMLParser import HTMLParser

es_host = 'https://search-test-qmyiuzwgkz4c6jmlzhhy6p2t7y.us-east-1.es.amazonaws.com'
es_index = 'watch_interval'
es_type = 'test-type'

es_resource=es_index + "/" + es_type

print (es_resource)

sc = SparkContext()
conf={ "es.resource" : es_resource,
       "es.nodes" : es_host,
       "es.port" : "443"
     }

es_rdd = sc.newAPIHadoopRDD(
 inputFormatClass="org.elasticsearch.hadoop.mr.EsInputFormat",
 keyClass="org.apache.hadoop.io.NullWritable",
 valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
 conf=conf)
print(es_rdd.first())
output = es_rdd.collect()
for (k, v) in output:
    print((k, v))

sc.stop()
