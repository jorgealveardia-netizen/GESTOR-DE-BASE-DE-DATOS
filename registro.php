<?php 
/**
 * Archivo: registro.php
 * Propósito: Formulario para el registro de nuevos usuarios.
 */
session_start();

// Si un usuario ya está logueado, lo redirigimos a la página de bienvenida
if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === TRUE) {
    header("location: bienvenida.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro de Usuario - Emprendimiento UNIPAZ</title>
    
    <link rel="stylesheet" href="styles.css">
    <script defer src="script.js"></script>
    
</head>
<body>
    <div class="contenedor">
        
        <h2>Registro de Nuevo Usuario</h2>
        
        <form action="procesar_registro.php" method="POST">
            <label for="usuario">Correo Institucional (Usuario):</label>
            <input type="text" id="usuario" name="usuario" placeholder="ejemplo@unipaz.edu.co" required><br><br>

            <label for="contrasena">Contraseña:</label>
            <input type="password" id="contrasena" name="contrasena" required><br><br>

            <input type="submit" value="Registrarme">
        </form>
        
        <hr>
        <p>¿Ya tienes cuenta? <a href="index.php">Inicia Sesión</a></p>
    </div>
    </body>
</html>