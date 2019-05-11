<?php
// required headers
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: access");
header("Access-Control-Allow-Methods: GET");
header("Access-Control-Allow-Credentials: true");
header('Content-Type: application/json');

// include database and object files
include_once '../config/database.php';
include_once '../objects/map.php';

// get database connection
$database = new Database();
$db = $database->getConnection();

// prepare product object
$map = new Map($db);

// set ID property of record to read
$map->map_id = isset($_GET['map_id']) ? $_GET['map_id'] : die();

// read the details of product to be edited
$map->readOne();

if($map->map_id!=null){
    // create array
    $map_arr = array(
        "map_id" =>  $map->map_id,
        "x" => $map->x,
        "y" => $map->y,
        "detected" => $map->detected,
        "traveled" => $map->traveled,
        "obstacle" => $map->obstacle
    );

    // set response code - 200 OK
    http_response_code(200);

    // make it json format
    echo json_encode($map_arr);
}

else{
    // set response code - 404 Not found
    http_response_code(404);

    // tell the user product does not exist
    echo json_encode(array("message" => "Map does not exist."));
}
?>
