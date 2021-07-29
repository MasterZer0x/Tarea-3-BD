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
$second_edit = 0; // Segundo id primario
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

    if ( array_key_exists("id_to_delete", $params) && !array_key_exists("id2delete", $params)){ // Si se ha solicitado la eliminacion de una fila
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
    if ( array_key_exists("id_to_delete", $params) && array_key_exists("id2delete", $params)){ // Si se ha solicitado la eliminacion de una fila
        
        $paramms = $params['id_to_delete'].'/'.$params['id2delete'];
        $correct_time = str_replace(' ', '%20', $params['id_to_delete']);
        $paramms =  $correct_time . '/' .$params['id2delete'];
        $call = callAPI('DELETE', $URL_API.'/api/'.$tablename.'/'.$paramms, false);
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
    $urlp = '';
    switch($tablename)
    {
        case "usuario":
            $data = usuario_update_data($URL_API, $to_edit);
            $msj = " al usuario ".$to_edit;
            $urlp = $to_edit;
            break;
	    case "moneda":
            $data = moneda_update_data();
            $msj = " la moneda ".$to_edit;
            $urlp = $to_edit;
            break;
        case "pais":
            $data = pais_update_data();
            $msj = " el pais".$to_edit;
            $urlp = $to_edit;
            break;
        case "cuenta_bancaria":
            $urlp = $to_edit;
            $msj = " la cuenta bancaria".$to_edit;
            $data = cuenta_bancaria_update_data();
            break;
        case "usuario_tiene_moneda":
            $urlp = $to_edit.'/'.$second_edit;
            $msj = " el balance del usuario".$to_edit;
            $data = usuario_tiene_moneda_update_data();
            break;
        default :
            $data = array();
            break;


    }
    echo "in";
    
    // Llamar a API con estructura dada (NO ES NECESARIO CAMBIAR ESTO)
    $put_response = callAPI('PUT', $URL_API.'/api/'.$tablename.'/'.$urlp,  json_encode($data));
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
        case "usuario_tiene_moneda":
            $data = usuario_tiene_moneda_create_data();
            $mensaje = "Ha habido un error al agregar la moneda al usuario id=".$to_edit;
            $mensaje2 = "El usuario ya tiene la moneda";
            break;
        case "precio_moneda":
                $data = precio_moneda_create_data();
                $mensaje = "Ha habido un error al agregar el nuevo valor a la moneda id=".$to_edit;
                break;
        default :
            $data = array();
            break;


    }
    
   

    // Llamar a API con estructura dada (NO ES NECESARIO CAMBIAR ESTO)
    $call_post = callAPI('POST', 'http://127.0.0.1:4996/api/'.$tablename,  json_encode($data));
    $response_post = json_decode($call_post , true);
    if(is_array($response_post) && !(array_key_first($response_post) == 'message')) // si hay respuesta
    {

        header("Location: http://localhost/simulacro/CRUD/".$tablename.".html?success=".array_key_first($response_post));
    }
    elseif ($response_post['message'] == "Esta creado")
    {
        create_warning_windows($mensaje2);
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

