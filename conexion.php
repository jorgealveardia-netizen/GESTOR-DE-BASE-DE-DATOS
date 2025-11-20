<?php
/**
 * Archivo: conexion.php
 * Propósito: Establecer la conexión con la base de datos 'emprendimiento'.
 */

$servidor = "localhost"; // Servidor por defecto en XAMPP
$usuario = "root";       // Usuario por defecto en XAMPP
$contrasena = "";        // Contraseña por defecto en XAMPP (vacía)
$base_de_datos = "emprendimiento"; // ¡Tu base de datos!

// Crear la conexión
$conexion = new mysqli($servidor, $usuario, $contrasena, $base_de_datos);

// Verificar la conexión
if ($conexion->connect_error) {
    // Detener la ejecución si la conexión falla y mostrar el error.
    die("Conexión fallida: " . $conexion->connect_error);
}

// Opcional: Establecer el juego de caracteres a UTF-8
$conexion->set_charset("utf8");

// La conexión está lista para ser usada.
?>