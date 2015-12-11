#CMPE 272 Project Software Engineering San Jose State University 
#Filtering Log DataBase with relevant filters and parsing IP addresses for detected Security Events and Analytics over the same 

#hadopp Connector Plugin for Elasticsearch used to Connect to Elasticsearch Database via Python Script of SparkConf

#Script for Mapping breaches related to User-Priviledges-And-Permissions

from pyspark import SparkContext, SparkConf
import re
fields_list=["gl2_remote_ip","message"]
custom_query='{ "query" :  { "query_string" : { "fields" : ["message"], "query" : "user not in sudoers", "use_dis_max" : true, minimum_should_match : 70} }}'
domain="User-Priviledges-And-Permissions"
compliance_map="PCI"

#    exit()
#pattern = r"((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))"
pattern = r"((?:[0-9]{1,3}\.){3}[0-9]{1,3})"
if __name__ == "__main__":
    #string confstring = { 'es.nodes' : 'elasticsearch', 'es.port' : '9200', 'es.resource' : 'graylog2_0/message', 'es.query' : '""', "fields" : [ "message" ] } }}' }
    conf = SparkConf().setAppName("ESTest")
    sc = SparkContext(conf=conf)
    es_read_conf = {
        'es.nodes' : 'elasticsearch',
        'es.port' : '9200',
        'es.resource' : 'graylog2_*/message',
        'es.query' : '{"query": { "multi_match" : { "query" : ' ', "fields" : [ "message" ] } }}'
      } 
    es_read_conf['es.query'] = custom_query 
    es_rdd = sc.newAPIHadoopRDD(
        inputFormatClass="org.elasticsearch.hadoop.mr.EsInputFormat",
        keyClass="org.apache.hadoop.io.NullWritable", 
        valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
        conf=es_read_conf)
    es_write_conf = {
        'es.nodes' : 'elasticsearch',
        'es.port' : '9200',
        'es.resource' : 'spark_analytics/analytics'
    }
    es_write_conf_ip = {
        'es.nodes' : 'elasticsearch',
        'es.port' : '9200',
        'es.resource' : 'spark_analytics/analytics'
    }
    doc = es_rdd.first()[1]
#    print es_rdd.collect()
#    exit()
    for field in doc:
        if field in fields_list:
         message=es_rdd.map(lambda message: message)
   #      print "##########################################################"
  #       print message.take(1)
 #        print message.collect()
         value_counts = es_rdd.map(lambda item: item[1][field])
     #    value_timestamp = es_rdd.map(lambda item: item[1]['timestamp'])
    #     print doc 
#         if field=="messageu":
#          value_counts1 = es_rdd.map(lambda ipddress: tuple(re.findall(pattern, ipddress[1][field])) )
#          value_counts1 = value_counts1.map(lambda word: (word, 1))
#          value_counts1 = value_counts1.reduceByKey(lambda a, b: a+b)
#          value_counts1 = value_counts1.filter(lambda item: item[1] > 1)  
#          print(value_counts1.collect()) 
#          value_counts1 = value_counts1.map(lambda item: ('key', {
#             'field': field,
#             'val': item[0],
#             'count': item[1],
#             'compliance': compliance_map,
#           #  'remote_ip': remote_ip
#             'query_string': custom_query_string
#          }))  
         if field=="message": 
          value_counts = value_counts.map(lambda word: (word, 1))
          value_counts = value_counts.reduceByKey(lambda a, b: a+b)
          value_counts = value_counts.filter(lambda item: item[1] > 1)
          remote_ip=""
          value_counts = value_counts.map(lambda item: ('key', { 
             'field': field, 
 #            'doc': value_timestamp,
             'val': item[0], 
             'count': item[1],
             'compliance': compliance_map,
           #  'remote_ip': remote_ip  
             'domain': domain
          }))
          print(field)
          print(value_counts.collect())
#exit()
          value_counts.saveAsNewAPIHadoopFile(
          path='-', 
          outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
          keyClass="org.apache.hadoop.io.NullWritable", 
          valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
          conf=es_write_conf)
#         value_counts1.saveAsNewAPIHadoopFile(
#         path='-',
#         outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
#         keyClass="org.apache.hadoop.io.NullWritable",
#         valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
#         conf=es_write_conf_ip)   



