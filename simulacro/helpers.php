<?php
include  'APICaller.php';


// Funciones para crear ventanas de lo resultados
function create_success_windows ($text)
{
    $button = '<button id="close-window"  type="button" class="close" aria-label="Close"><span aria-hidden="true" style="position: fixed;left: 95%;top: 0%;">&times;</span></button>';
    echo '<div id = "windows-inform"
    class="container w-25 shadow-lg rounded m-auto p-5 bg-success text-white text-center window_fadeout"
    style="position: fixed; z-index: 10; left: 50%; transform: translate(-50%, -30%);"
    > '.$button.''.$text.'</div>';
}


function create_danger_windows ($text)
{
    $button = '<button id="close-window"  type="button" class="close" aria-label="Close"><span aria-hidden="true" style="position: fixed;left: 95%;top: 0%;">&times;</span></button>';
    echo '<div id = "windows-inform"
    class="container w-25 shadow-lg rounded m-auto p-5 bg-danger text-white text-center window_fadeout"
    style="position: fixed; z-index: 10; left: 50%; transform: translate(-50%, -30%);"
    > '.$button.''.$text.'</div>';

}



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
    if ( array_key_exists("to_edit", $params)){
        $to_edit = $params['to_edit'];
    }

    // Funciones que no requieren intrinsicamente de una estructura especifica.

    if ( array_key_exists("success", $params)){ // Si se accede a la actualizacion de un dato
        $id_suc = $params['success'];
        if($id_suc != 0)
        {
            create_success_windows("Se ha actualizado la fila con id=".$id_suc." asociada.");
        }

    }

    if ( array_key_exists("delete_user", $params)){ // Si se ha solicitado la eliminacion de una fila
        $call = callAPI('DELETE', $URL_API.'/api/'.$tablename.'/'.$params['delete_user'], false);
        if(is_array(json_decode($call, true)))
        {
            create_success_windows("Se ha eliminado la fila con la id=".$params['delete_user']." asociada"); // Se ha borrado una fila
        }
        else
        {
            create_danger_windows("No se ha podido eliminar al usuario con id=".$params['delete_user']); // Ha ocurrido un error
        }
    }
}


function usuario_update_data($URL_API, $to_edit)
{
    $opciones = array('cost'=>12);
    

    $get_user = callAPI('GET', $URL_API.'/api/usuario/'.$to_edit,  false);
    $response_get = json_decode($get_user , true);

    if ($_POST['contrasena'] == $response_get['contrasena'])
    {
        $pwd_hashed = $_POST['contrasena'];
    }
    else{
        $pwd_hashed = password_hash($_POST['contrasena'], PASSWORD_BCRYPT, $opciones);
    }
    

    $data = array(  
        'nombre' => $_POST['nombre'], 
        'apellido' => $_POST['apellido'], 
        'correo' => $_POST['correo'], 
        'contrasena' => $pwd_hashed, 
        'pais' => $_POST['pais']
        );
    return $data;
}


function usuario_create_data($URL_API, $to_edit)
{
    $opciones = array('cost'=>12);
    $pwd_hashed = password_hash($_POST['cont'], PASSWORD_BCRYPT, $opciones);

    $data = array(  
        'nombre' => $_POST['nombre2'], 
        'apellido' => $_POST['ape'], 
        'correo' => $_POST['cor'], 
        'contrasena' => $pwd_hashed, 
        'pais' => $_POST['pais']
        );

    return $data;
}


// Estructura para actualizar y crear filas en las tablas
if(isset($_POST['update_button'])){ // Si se presiono el boton "Actualizar"
    
    switch($tablename)
    {
        case "usuario":
            $data = usuario_update_data($URL_API, $to_edit);
            break;
        default :
            $data = array();
            break;


    }
    
    // Llamar a API con estructura dada (NO ES NECESARIO CAMBIAR ESTO)
    $call_put = callAPI('PUT', $URL_API.'/api/usuario/'.$to_edit,  json_encode($data));
    $response_put = json_decode($call_put , true);
    if(is_array($response_put)) // si hay respuesta
    {
        header("Location: http://localhost/simulacro/usuario.html?success=".$to_edit);
    }
    else
    {
        create_danger_windows("Ha habido un error al actualizar al usuario ".$to_edit);
    }

}  


if(isset($_POST['create_button'])){ // Si se presiono el boton "Crear"

    switch($tablename)
    {
        case "usuario":
            $data = usuario_create_data($URL_API, $to_edit);
            break;
        default :
            $data = array();
            break;


    }
    
   

    // Llamar a API con estructura dada (NO ES NECESARIO CAMBIAR ESTO)
    $call_post = callAPI('POST', 'http://127.0.0.1:4996/api/usuario',  json_encode($data));
    $response_post = json_decode($call_post , true);
    if(is_array($response_post)) // si hay respuesta
    {
        header("Location: http://localhost/simulacro/usuario.html?success=".array_key_first($response_post));
    }
    else
    {
        create_danger_windows("Ha habido un error al crear al usuario ".$to_edit);
    }

  }  






// Conseguir todos las filas de la tabla actual
$make_call = callAPI('GET', $URL_API.'/api/'.$tablename, false);
$response = json_decode($make_call, true);


// Listener para cerrar ventana abierta.
echo '<script type="text/javascript">
document.getElementById("close-window").onclick = function () { document.getElementById("windows-inform").style.display = "none"; };
</script>';

?>