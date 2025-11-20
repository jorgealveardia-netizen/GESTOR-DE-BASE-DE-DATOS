<?php
/**
 * Archivo: procesar_registro.php
 * Propósito: Valida el correo institucional, registra el usuario e inicia la sesión automáticamente.
 */
session_start(); // ¡IMPORTANTE! Inicia la sesión

require 'conexion.php'; // Asegúrate de que conexion.php está en la misma carpeta

$mensaje = "";
$dominio_permitido = '@unipaz.edu.co';
$rol_inicial = 'invitado'; // Rol por defecto

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // Obtener los datos (asumimos que el email completo está en 'usuario')
    $usuario_nuevo = $conexion->real_escape_string($_POST['usuario']);
    $contrasena_plana = $_POST['contrasena'];
    $email_nuevo = $usuario_nuevo; // Usamos el input 'usuario' como 'email'

    // 1. VALIDACIÓN DE EMAIL INSTITUCIONAL
    if (substr($email_nuevo, -strlen($dominio_permitido)) !== $dominio_permitido) {
        $mensaje = "Error de registro: Solo se permiten correos con la terminación **$dominio_permitido**.";
    } else {
        
        // 2. Cifrar la contraseña
        $contrasena_hasheada = password_hash($contrasena_plana, PASSWORD_DEFAULT);
        
        // 3. Consulta SQL (Debe incluir 'email' y 'rol')
        $sql = "INSERT INTO usuarios (usuario, email, contrasena, rol) VALUES (?, ?, ?, ?)";

        if ($stmt = $conexion->prepare($sql)) {
            // 'ssss': cuatro parámetros de tipo string
            $stmt->bind_param("ssss", $usuario_nuevo, $email_nuevo, $contrasena_hasheada, $rol_inicial);

            if ($stmt->execute()) {
                
                // --- REGISTRO EXITOSO: INICIAR SESIÓN Y REDIRIGIR ---
                
                $_SESSION['loggedin'] = TRUE;
                $_SESSION['id'] = $conexion->insert_id; // Obtiene el ID del nuevo registro
                $_SESSION['usuario'] = $usuario_nuevo;
                $_SESSION['rol'] = $rol_inicial; // Carga el rol para evitar el error 'DESCONOCIDO'
                
                // Redirige al destino final
                header("location: bienvenida.php");
                exit; 
                
            } else {
                // Manejo de errores de base de datos
                if ($conexion->errno == 1062) {
                     $mensaje = "Error: El correo $usuario_nuevo ya está registrado.";
                } else {
                    $mensaje = "Error al registrar: " . $stmt->error;
                }
            }
            $stmt->close();
        }
    }
}

$conexion->close();
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resultado del Registro</title>
</head>
<body>
    <h2>Estado del Registro</h2>
    <p><?php echo $mensaje; ?></p>
    <?php if (!isset($_SESSION['loggedin'])): ?>
        <p>Intenta <a href='index.php'>iniciar sesión</a>.</p>
    <?php endif; ?>
</body>
</html>