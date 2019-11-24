<?php

$data = file_get_contents("php://input");
$json = json_decode($data);
if(!$json || !$json->session) {
    die();    
}

file_put_contents("tracking/".(time()) . "_" . ($json->session).".log", json_encode($json, JSON_PRETTY_PRINT), FILE_APPEND);

?>