<?php

// Estructa de datos necesarios para create/update.


// CREATES


function usuario_create_data()
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

function moneda_create_data()
{

    $data = array(  
        'nombre' => $_POST['nom'], 
        'sigla' => $_POST['sig'], 
        );

    return $data;
}


function pais_create_data()
{
    $data = array(  
        'nombre' => $_POST['nombre_cre']
        );

    return $data;
}


function cuenta_bancaria_create_data()
{
    $data = array(  
        'id_usuario' => $_POST['iduser2'], 
        'balance' => $_POST['balance2']
        );

    return $data;
}

// -------------------------------------------------------------------------------
// UPDATES

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


function moneda_update_data()
{
    $data = array(  
        'sigla' => $_POST['sig'], 
        'nombre' => $_POST['nom']
        );

    return $data;
}

function pais_update_data()
{
    $data = array(  
        'nombre' => $_POST['nombre_upt']
        );

    return $data;
}
function cuenta_bancaria_update_data()
{
    $data = array(  
        'balance' => $_POST['balance']
        );

    return $data;
}

?>