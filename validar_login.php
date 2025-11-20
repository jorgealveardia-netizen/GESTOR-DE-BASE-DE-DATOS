<?php
/**
 * Archivo: validar_login.php
 * Propósito: Procesar el formulario de login y validar las credenciales.
 */

session_start();

if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === TRUE) {
    header("location: bienvenida.php");
    exit;
}

require 'conexion.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    $usuario_ingresado = $_POST['usuario'];
    $contrasena_ingresada = $_POST['contrasena'];

    // CORRECCIÓN CLAVE: Se selecciona 'rol'
    $sql = "SELECT id, contrasena, rol FROM usuarios WHERE usuario = ?";

    if ($stmt = $conexion->prepare($sql)) {
        $stmt->bind_param("s", $usuario_ingresado);
        
        if ($stmt->execute()) {
            $resultado = $stmt->get_result();

            if ($resultado->num_rows == 1) {
                $fila = $resultado->fetch_assoc();
                $hash_contrasena = $fila['contrasena'];

                if (password_verify($contrasena_ingresada, $hash_contrasena)) {
                    
                    $_SESSION['loggedin'] = TRUE;
                    $_SESSION['id'] = $fila['id'];
                    $_SESSION['usuario'] = $usuario_ingresado;
                    
                    // CORRECCIÓN CLAVE: Almacenar el rol
                    $_SESSION['rol'] = $fila['rol']; 

                    header("location: bienvenida.php");
                    exit;
                    
                } else {
                    $error_login = "Usuario o contraseña incorrectos.";
                }
            } else {
                $error_login = "Usuario o contraseña incorrectos.";
            }
        } else {
            $error_login = "Error del servidor al intentar buscar el usuario.";
        }

        $stmt->close();
    }
    $conexion->close();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Error de Login</title>
</head>
<body>
    <h2>Resultado de la Autenticación</h2>
    <?php if (isset($error_login)): ?>
        <p style="color: red;"><?php echo $error_login; ?></p>
        <p><a href="index.php">Volver al Login</a></p>
    <?php else: ?>
        <p>Ha ocurrido un error inesperado. Por favor, vuelve al <a href="index.php">Login</a>.</p>
    <?php endif; ?>
</body>
</html>