<html>
<body>
<?php

$host="localhost"; // Host name 
$username="root"; // Mysql username 
$password="Rajsmitmadhumay"; // Mysql password 
$db_name="Quize1_281"; // Database name 
$tbl_name="members"; // Table name 

// Connect to server and select databse.
$connection=mysql_connect($host, $username, $password)or die("cannot connect"); 
if (!$connection) { 
    die('Could not connect: ' . mysql_error()); 
} 

$db=mysql_select_db($db_name)or die("cannot connect");
ini_set('mysql.connect_timeout', 500000);
// username and password sent from form 
$myusername=$_POST['form-username']; 
$mypassword=$_POST['form-password']; 
$role=$_POST['role_name'];

//$username=$_POST['username'];
//$password=$_POST['password'];

// To protect MySQL injection (more detail about MySQL injection)
$myusername = stripslashes($myusername);
$mypassword = stripslashes($mypassword);
$myusername = mysql_real_escape_string($myusername);
$mypassword = mysql_real_escape_string($mypassword);
//$role=stripslashes($role);
//$role = mysql_real_escape_string($role);

$query = mysql_query("select * from members where password='$mypassword' AND username='$myusername' AND role='$role'", $connection);

//$sql="SELECT * FROM members" ; 


// Mysql_num_row is counting table row
$rows = mysql_num_rows($query);


// If result matched $myusername and $mypassword, table row must be 1 row
if($rows==1){

	if($role=="System Admin")
		header("location:dashboardSysAdmin.html");
	if($role=="CIO")	
		header("location:dashboardCIO.html");

}
else {
	header("location:forms.html");
}

mysql_close($connection); 
?>

</body>
</html>
