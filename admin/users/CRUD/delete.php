<?php  include $_SERVER['DOCUMENT_ROOT'].'/db_config.php';
include '../../../include/navbar.html';

$actual_link = "http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
$pattern = "/.*=([0-9]+)/i";
preg_match($pattern, $actual_link, $re); 
$id = $re[1];

$plata = "SELECT * FROM usuario_tiene_moneda WHERE id_usuario =". $id;
$revisarplata = pg_query_params($dbconn, $plata,array());





if (pg_num_rows($revisarplata) != 0){

    $sql = "DELETE FROM usuario_tiene_moneda WHERE id_usuario=".$id;
    $ejecucion = pg_query($dbconn, $sql);

    if ($ejecucion) // Si no hay correos registrados
    {
        $sql2 = "DELETE FROM cuenta_bancaria WHERE id_usuario=".$id;
        $ejecucion2 = pg_query($dbconn, $sql2);
    
        $sql = "DELETE FROM usuario WHERE id=".$id;
        $ejecucion = pg_query($dbconn, $sql);
        if ($ejecucion  && $ejecucion2) // Si no hay correos registrados
        {
            $text = "Usuario tenia monedas. Eliminado correctamente.";
            $etiq = "success";
        } else {
            $text = "Se han eliminado las monedas del usuario. Pero hubo un problema al eliminar al usuario.";
            $etiq = "danger";
        }    

    } else {
        $text = "Ha ocurrido un error al eliminar las monedas del usuario.";
        $etiq = "danger";
    }    


}
else{
    $sql2 = "DELETE FROM cuenta_bancaria WHERE id_usuario=".$id;
    $ejecucion2 = pg_query($dbconn, $sql2);

    $sql = "DELETE FROM usuario WHERE id=".$id;
    $ejecucion = pg_query($dbconn, $sql);
    if ($ejecucion && $ejecucion2) // Si no hay correos registrados
    {
        $text = "Usuario Eliminado correctamente.";
        $etiq = "success";
    } else {
        $text = "Ha ocurrido un error al eliminar el usuario.";
        $etiq = "danger";
    }    
}



echo"<html>";
echo"   <body>";

echo '<div class="container-fluid">';
echo '<div class="row p-3">';
echo '<div class="col">';
echo '<div class="container shadow-lg rounded m-auto p-5">';


echo '<div class="pt-xl-3 pb-xl-5">';

echo '<h2 class="text-center text-'. $etiq .'">'. $text .'</h2>';


echo '</div>';

echo '</div>';
echo '</div>';

echo "</div>";
echo '</div>';

echo"   </body>";



















?>