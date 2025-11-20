<?php
/**
 * Archivo: index.php
 * Propósito: Página de login de la aplicación.
 */
session_start();

// Si el usuario ya está logueado, lo redirigimos a la página de bienvenida
if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === TRUE) {
    header("location: bienvenida.php");
    exit;
}

// Puedes añadir aquí la lógica para mostrar el error de login si viene de validar_login.php
// Por simplicidad, aquí solo mostramos el formulario.
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Iniciar Sesión - Emprendimiento UNIPAZ</title>
    
    <link rel="stylesheet" href="styles.css"> 
    <script defer src="script.js"></script>
    
</head>
<body>
    
    <div class="split-container">
        
        <div class="seccion-fondo">
            </div>

        <div class="seccion-login">
            <div class="contenedor formulario-login-card">
                <h2>Iniciar Sesión</h2>
                
                <form action="validar_login.php" method="POST">
                    <label for="usuario">Correo Institucional (Usuario):</label>
                    <input type="text" id="usuario" name="usuario" required>
                    
                    <label for="contrasena">Contraseña:</label>
                    <input type="password" id="contrasena" name="contrasena" required>
                    
                    <input type="submit" value="Entrar">
                </form>

                <hr>
                <p>¿No tienes cuenta? <a href="registro.php">Regístrate aquí</a></p>
            </div>
        </div>

    </div>
    
</body>
</html>