<?php

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

function create_warning_windows ($text)
{
    $button = '<button id="close-window"  type="button" class="close" aria-label="Close"><span aria-hidden="true" style="position: fixed;left: 95%;top: 0%;">&times;</span></button>';
    echo '<div id = "windows-inform"
    class="container w-25 shadow-lg rounded m-auto p-5 bg-warning text-white text-center window_fadeout"
    style="position: fixed; z-index: 10; left: 50%; transform: translate(-50%, -30%);"
    > '.$button.''.$text.'</div>';

}

?>