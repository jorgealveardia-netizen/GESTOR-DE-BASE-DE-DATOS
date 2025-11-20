<?php
/**
 * Archivo: bienvenida.php
 * Propósito: Página de destino después del login/registro. Muestra contenido por rol.
 */
session_start();

// Si el usuario no está logueado, lo redirigimos a la página de login
if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== TRUE) {
    header("location: index.php");
    exit;
}

// 1. CORRECCIÓN: Evita el error "Undefined array key" y resuelve el rol DESCONOCIDO.
$rol = 'desconocido'; 
if (isset($_SESSION['rol'])) {
    $rol = $_SESSION['rol']; 
}

// Mapea el rol a una clase CSS para darle color:
$clase_rol = 'rol-' . strtolower($rol);
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Bienvenido a Emprendimiento UNIPAZ</title>
    
    <link rel="stylesheet" href="styles.css"> 
    <script defer src="script.js"></script>
    
</head>
<body>
    
    <div class="contenedor contenedor-bienvenida"> 
        <h1>¡Hola, <?php echo htmlspecialchars($_SESSION['usuario']); ?>!</h1>
        
        <h3 class="rol-status <?php echo $clase_rol; ?>">Tu Rol Actual es: <?php echo strtoupper($rol); ?></h3>
        <hr>

        <?php if ($rol === 'invitado'): ?>
            <h2>Zona de Invitados</h2>
            <p>Como **USUARIO INVITADO**, solo puedes ver y navegar entre los emprendimientos. Para poder interactuar o ser emprendedor, necesitas cambiar tu rol a **'normal'**.</p>
        <?php elseif ($rol === 'normal'): ?>
            <h2>Zona de Usuario Normal</h2>
            <p>Como **USUARIO NORMAL**, puedes interactuar con los emprendimientos. Si deseas publicar tu propio proyecto, haz la solicitud:</p>
            <button class="boton">Solicitar Rol de Emprendedor</button>
        <?php elseif ($rol === 'emprendedor'): ?>
            <h2>Panel de Emprendedor</h2>
            <p>¡Felicidades, **EMPRENDEDOR**! Tienes permisos para publicar y gestionar tus emprendimientos.</p>
            <button class="boton">Publicar Nuevo Emprendimiento</button>
        <?php elseif ($rol === 'administrador'): ?>
            <h2 style="color: red;">ADMINISTRADOR DEL SISTEMA</h2>
            <p>Tienes acceso total. Puedes gestionar usuarios y aprobar solicitudes de emprendedores.</p>
            <button class="boton">Ir a Panel de Administración</button>
        <?php else: ?>
            <p>Lo sentimos, no se pudo identificar tu rol. Por favor, contacta a soporte.</p>
        <?php endif; ?>

        <hr>
        
        <br> 
        <a href="logout.php" class="boton">Cerrar Sesión</a>
    </div>
    </body>
</html>