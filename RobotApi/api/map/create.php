<?php
// required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

// get database connection
include_once '../config/database.php';

// instantiate product object
include_once '../objects/map.php';

$database = new Database();
$db = $database->getConnection();

$map = new Map($db);

// get posted data
$json = file_get_contents('php://input');
$data = json_decode($json);

echo $data->x;
echo $data->y;
echo $data->detected;
echo $data->traveled;
echo $data->obstacle;

// make sure data is not empty
if(1==1){

    // set product property values
    $map->x = $data->x;
    $map->y = $data->y;
    $map->detected = $data->detected;
    $map->traveled = $data->traveled;
    $map->obstacle = $data->obstacle;

    // create the product
    if($map->create()){

        // set response code - 201 created
        http_response_code(201);

        // tell the user
        echo json_encode(array("message" => "Map was created."));
    }

    // if unable to create the product, tell the user
    else{

        // set response code - 503 service unavailable
        http_response_code(503);

        // tell the user
        echo json_encode(array("message" => "Unable to create map."));
    }
}

// tell the user data is incomplete
else{

    // set response code - 400 bad request
    http_response_code(400);

    // tell the user
    echo json_encode(array("message" => "Unable to create map. Data is incomplete."));
}

?>
