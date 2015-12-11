 <?php
        header('Access-Control-Allow-Origin: *');
        error_reporting(E_ALL);
        ini_set("display_errors", 1);
 //   exit();

    $value = $_POST['type'];
    $query = '';
    #$value =  'nistcount';

 if ($value == 'totalCount')
    {

      $res =get_latlan("elasticsearch","graylog2_*","ip_analytics",$query);
      echo json_encode($res);

      }
  else if ($value == 'unknownip')
    {

      $res =get_latlan("elasticsearch","spark_analytics/ip_analytics","ip_aanlytics",$query);
      echo json_encode($res);

     #  http://52.23.100.76:9200/spark_analytics/ip_analytics/_count
      }
  else if ($value == 'SeverLogCount')
   {

 #  undesiredEvents
    $res =get_latlan("elasticsearch","spark_analytics/severe_analytics","ip_aanlytics",$query);
     echo json_encode($res);

      }
   else if ($value == 'undesiredEvents')
    {

     $res =get_latlan("elasticsearch","spark_analytics","ip_aanlytics",$query);
     echo json_encode($res);



        }

   else if ($value == 'pcicount')
   {

         $query='{"query": { "multi_match" : { "query" : "PCI AND message ", "fields" : [ "compliance" ] } }}';

         $res =get_latlan("elasticsearch","spark_analytics/analytics","ip_aanlytics",$query);
         echo json_encode($res);

     }

  else if ($value == 'hipaacount')
   {
          $query='{"query": { "multi_match" : { "query" : "HIPAA AND message", "fields" : [ "compliance" ] } }}';

         $res =get_latlan("elasticsearch","spark_analytics/analytics","ip_aanlytics",$query);
         echo json_encode($res);


        }
else if ($value == 'nistcount')
   {
           $query='{"query": { "multi_match" : { "query" : "NIST AND message", "fields" : [ "compliance" ] } }}';

         $res =get_latlan("elasticsearch","spark_analytics/analytics","ip_aanlytics",$query);
         echo json_encode($res);


        }

 else if ($value == 'fedrampcount')
   {
           $query='{"query": { "multi_match" : { "query" : "FEDRAMP AND message", "fields" : [ "compliance" ] } }}';

         $res =get_latlan("elasticsearch","spark_analytics/analytics","ip_aanlytics",$query);
         echo json_encode($res);


        }


 #  curl -XGET elasticsearch:9200/spark_analytics/analytics/_count?pretty=true -d  '{"query": { "multi_match" : { "query" : "PCI", "fields" : [ "compliance" ] } }}'




     function get_latlan($hostname,$index,$type,$query)
        {
                $GLOBALS['ch'] = curl_init();
                curl_setopt($GLOBALS['ch'], CURLOPT_POSTFIELDS, $query);
                curl_setopt ($GLOBALS['ch'], CURLOPT_CONNECTTIMEOUT, 0);
                curl_setopt($GLOBALS['ch'], CURLOPT_HEADER, 0);
                curl_setopt ($GLOBALS['ch'], CURLOPT_RETURNTRANSFER, 1);
                curl_setopt($GLOBALS['ch'], CURLOPT_URL, $hostname.":9200/".$index."/_count?pretty=true");
                curl_setopt($GLOBALS['ch'], CURLOPT_HTTPHEADER, array(
                                        'Content-Type: application/json',
                                        'Content-Length: ' . strlen($query))
                                        );
                $res = curl_exec($GLOBALS['ch']);
                curl_close($GLOBALS['ch']);
                //$result=json_decode($res,true);
                return $res;
        }








?>

