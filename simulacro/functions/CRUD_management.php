<?php
include  'APICaller.php';
include  'CU_data_models.php';
include  'windows_functions.php';

// Variables estandares para cualquier tabla
$actual_link = "http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
$url_components = parse_url($actual_link);
$pattern = "/\/(?:.*\/)*(.*).html/";
preg_match($pattern, $url_components['path'], $temp); 
$tablename = $temp[1];

// Inicializacion identificadores de accion
$to_edit = 0; // No hay id a modificar
$update_id = 0;
$borrado = 0; // No se ha eliminado a usuarios


// Gestionar parametros
if ( array_key_exists("query", $url_components))
{
    parse_str($url_components['query'], $params);
    if ( array_key_exists("to_edit", $params ) && !array_key_exists("second_edit", $params )){
        $to_edit = $params['to_edit'];
    }
    else if ( array_key_exists("to_edit", $params ) && array_key_exists("second_edit", $params )){
        $to_edit = $params['to_edit'];
        $second_edit = $params['second_edit'];
    }

    // Funciones que no requieren intrinsicamente de una estructura especifica.

    if ( array_key_exists("success", $params)){ // Si se accede a la actualizacion de un dato
        $id_suc = $params['success'];
        if($id_suc != 0)
        {
            create_success_windows("Se ha actualizado la fila con id=".$id_suc." asociada.");
        }

    }

    if ( array_key_exists("id_to_delete", $params)){ // Si se ha solicitado la eliminacion de una fila
        $call = callAPI('DELETE', $URL_API.'/api/'.$tablename.'/'.$params['id_to_delete'], false);
        if(is_array(json_decode($call, true)))
        {
            create_success_windows("Se ha eliminado la fila con la id=".$params['id_to_delete']." asociada"); // Se ha borrado una fila
        }
        else
        {
            create_danger_windows("No se ha podido eliminar al usuario con id=".$params['id_to_delete']); // Ha ocurrido un error
        }
    }



    
}

// Estructura para actualizar y crear filas en las tablas
if(isset($_POST['update_button'])){ // Si se presiono el boton "Actualizar"
    
    $msj = '';
    switch($tablename)
    {
        case "usuario":
            $data = usuario_update_data($URL_API, $to_edit);
            $msj = " al usuario ".$to_edit;
            break;
	    case "moneda":
            $data = moneda_update_data();
            $msj = " la moneda ".$to_edit;
            break;
        case "pais":
            $data = pais_update_data();
            break;
        case "cuenta_bancaria":
            $data = cuenta_bancaria_update_data();
            break;
        default :
            $data = array();
            break;


    }
    echo "in";
    
    // Llamar a API con estructura dada (NO ES NECESARIO CAMBIAR ESTO)
    $put_response = callAPI('PUT', $URL_API.'/api/'.$tablename.'/'.$to_edit,  json_encode($data));
    $put_response_array = json_decode($put_response , true);
    if(is_array($put_response_array)) // si hay respuesta
    {
        header("Location: http://localhost/simulacro/CRUD/".$tablename.".html?success=".$to_edit);
    }
    else
    {
        create_danger_windows("Ha habido un error al actualizar".$msj);
    }

}  


if(isset($_POST['create_button'])){ // Si se presiono el boton "Crear"
    switch($tablename)
    {
        case "usuario":
            $mensaje = "Ha habido un error al crear al usuario".$to_edit;
            $data = usuario_create_data();
            break;
	    case "moneda":
            $data = moneda_create_data();
            $mensaje = "Ha habido un error al crear la moneda".$to_edit;
            break;
        case "pais":
            $data = pais_create_data();
            $mensaje = "Ha habido un error al crear el pais".$to_edit;
            break;
        case "cuenta_bancaria":
            $data = cuenta_bancaria_create_data();
            $mensaje = "Ha habido un error al crear la cuenta bancaria id=".$to_edit;
            break;
        default :
            $data = array();
            break;


    }
    
   

    // Llamar a API con estructura dada (NO ES NECESARIO CAMBIAR ESTO)
    $call_post = callAPI('POST', 'http://127.0.0.1:4996/api/'.$tablename,  json_encode($data));
    $response_post = json_decode($call_post , true);
    if(is_array($response_post)) // si hay respuesta
    {
        header("Location: http://localhost/simulacro/CRUD/".$tablename.".html?success=".array_key_first($response_post));
    }
    else
    {
        create_danger_windows($mensaje);
    }

  }  






// Conseguir todos las filas de la tabla actual
$make_call = callAPI('GET', $URL_API.'/api/'.$tablename, false);
$response = json_decode($make_call, true);


// Listener para cerrar ventana abierta.
echo '<script type="text/javascript">
document.getElementById("close-window").onclick = function () { document.getElementById("windows-inform").style.display = "none"; };
</script>';

echo '
<script type="text/javascript">
    function redirect()
    {
    var url = "http://localhost/simulacro/CRUD/'.$tablename.'.html";
    location.href = url;
    }
    </script>';


?>

