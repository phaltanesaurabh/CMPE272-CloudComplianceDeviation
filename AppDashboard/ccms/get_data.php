 <?php
         header('Access-Control-Allow-Origin: *');
        error_reporting(E_ALL);
        ini_set("display_errors", 1);


        ##sample Query to Match all documents in elasticsearch

        $query = '';

        $res =get_latlan("elasticsearch","spark_analytics","ip_analytics",$query);

        echo json_encode($res);

        function get_latlan($hostname,$index,$type,$query)
        {
                $GLOBALS['ch'] = curl_init();
                curl_setopt($GLOBALS['ch'], CURLOPT_POSTFIELDS, $query);
                curl_setopt ($GLOBALS['ch'], CURLOPT_CONNECTTIMEOUT, 0);
                curl_setopt($GLOBALS['ch'], CURLOPT_HEADER, 0);
                curl_setopt ($GLOBALS['ch'], CURLOPT_RETURNTRANSFER, 1);
                curl_setopt($GLOBALS['ch'], CURLOPT_URL, $hostname.":9200/".$index."/".$type."/_search?size=500&pretty=true");
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
