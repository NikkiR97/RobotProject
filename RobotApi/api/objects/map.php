<?php
class Map{

    private $conn;
    private $table_name = "map";

    public $map_id;
    public $x;
    public $y;
    public $detected;
    public $traveled;
    public $obstacle;

    public function __construct($db){
        $this->conn = $db;
    }

    // read products
    function read(){

        // select all query
        $query = "SELECT * FROM map";

        // prepare query statement
        $stmt = $this->conn->prepare($query);

        // execute query
        $stmt->execute();

        return $stmt;
  }

  // create product
  function create(){

      // query to insert record
      $query = "INSERT INTO map SET x=:x, y=:y, detected=:detected, traveled=:traveled, obstacle=:obstacle";

      // prepare query
      $stmt = $this->conn->prepare($query);

      // sanitize
      $this->x=htmlspecialchars(strip_tags($this->x));
      $this->y=htmlspecialchars(strip_tags($this->y));
      $this->detected=htmlspecialchars(strip_tags($this->detected));
      $this->traveled=htmlspecialchars(strip_tags($this->traveled));
      $this->obstacle=htmlspecialchars(strip_tags($this->obstacle));

      // bind values
      $stmt->bindParam(":x", $this->x);
      $stmt->bindParam(":y", $this->y);
      $stmt->bindParam(":detected", $this->detected);
      $stmt->bindParam(":traveled", $this->traveled);
      $stmt->bindParam(":obstacle", $this->obstacle);

      // execute query
      if($stmt->execute()){
          return true;
      }

      return false;

  }

  // used when filling up the update product form
  function readOne(){

      // query to read single record
      $query = "SELECT * FROM map WHERE map_id = ?";

      // prepare query statement
      $stmt = $this->conn->prepare( $query );

      // bind id of product to be updated
      $stmt->bindParam(1, $this->map_id);

      // execute query
      $stmt->execute();

      // get retrieved row
      $row = $stmt->fetch(PDO::FETCH_ASSOC);

      // set values to object properties
      $this->x = $row['x'];
      $this->y = $row['y'];
      $this->detected = $row['detected'];
      $this->traveled = $row['traveled'];
      $this->obstacle = $row['obstacle'];
  }

  // update the product
  function update(){

      // update query
      $query = "UPDATE
                  " . $this->table_name . "
              SET
                  x = :x,
                  y = :y,
                  detected = :detected,
                  traveled = :traveled,
                  obstacle = :obstacle
              WHERE
                  map_id = :map_id";

      // prepare query statement
      $stmt = $this->conn->prepare($query);

      // sanitize
      $this->x=htmlspecialchars(strip_tags($this->x));
      $this->y=htmlspecialchars(strip_tags($this->y));
      $this->detected=htmlspecialchars(strip_tags($this->detected));
      $this->traveled=htmlspecialchars(strip_tags($this->traveled));
      $this->obstacle=htmlspecialchars(strip_tags($this->obstacle));

      // bind new values
      $stmt->bindParam(':x', $this->x);
      $stmt->bindParam(':y', $this->y);
      $stmt->bindParam(':detected', $this->detected);
      $stmt->bindParam(':traveled', $this->traveled);
      $stmt->bindParam(':obstacle', $this->obstacle);

      // execute the query
      if($stmt->execute()){
          return true;
      }

      return false;
  }
}
?>
