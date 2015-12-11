from pyspark import SparkContext, SparkConf
import re
fields_list=["gl2_remote_ip","message"]
custom_query='{"query": { "multi_match" : { "query" : "user unknown", "fields" : [ "message" ] } }}'
custom_query_string="user unknown"

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
        'es.resource' : 'graylog2_1/message',
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
        'es.resource' : 'spark_analytics/analytics',
#        'es.input.json':  'yes'
    }
    doc = es_rdd.first()[1]
    print(es_rdd.first())
#    exit()
    for field in doc:
        if field in fields_list:
         value_counts = es_rdd.map(lambda item: item[1][field])
         if field=="message":
          value_counts1 = es_rdd.map(lambda ipddress: tuple(re.findall(pattern, ipddress[1][field])) )
          print(value_counts1.collect())
          value_counts1 = value_counts1.map(lambda word: (word, 1))
        #  print(value_counts1.collect())
          value_counts1 = value_counts1.reduceByKey(lambda a, b: a+b)
          value_counts1 = value_counts1.filter(lambda item: item[1] > 1)
 
          print(value_counts1.collect()) 
          value_counts1 = value_counts1.map(lambda item: ('key', {
             'field': field,
             'val': item[0],
             'count': item[1],
             'compliance': 'PCI NIST FEDRAMP',
           #  'remote_ip': remote_ip
             'query_string': custom_query_string
          }))  
         value_counts = value_counts.map(lambda word: (word, 1))
         value_counts = value_counts.reduceByKey(lambda a, b: a+b)
         value_counts = value_counts.filter(lambda item: item[1] > 1)
         remote_ip=""
         value_counts = value_counts.map(lambda item: ('key', { 
             'field': field, 
             'val': item[0], 
             'count': item[1],
             'compliance': 'HIPAA',
           #  'remote_ip': remote_ip  
             'query_string': custom_query_string 
         }))

         print(field)
         print(value_counts1.collect())
#exit()
         value_counts.saveAsNewAPIHadoopFile(
         path='-', 
         outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
         keyClass="org.apache.hadoop.io.NullWritable", 
         valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
         conf=es_write_conf)
         value_counts1.saveAsNewAPIHadoopFile(
         path='-',
         outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
         keyClass="org.apache.hadoop.io.NullWritable",
         valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
         conf=es_write_conf_ip)   

#
#
