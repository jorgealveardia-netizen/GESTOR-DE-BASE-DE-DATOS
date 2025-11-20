<?php
/**
 * Archivo: logout.php
 * Propósito: Cierra la sesión activa del usuario.
 */

// 1. Iniciar la sesión (necesario para acceder a las variables de sesión)
session_start();

// 2. Destruir todas las variables de sesión
$_SESSION = array();

// 3. Si se desea destruir la cookie de sesión, también se debe eliminar
// la cookie de la sesión. Nota: Esto destruirá la sesión y no solo los datos de la sesión.
if (ini_get("session.use_cookies")) {
    $params = session_get_cookie_params();
    setcookie(session_name(), '', time() - 42000,
        $params["path"], $params["domain"],
        $params["secure"], $params["httponly"]
    );
}

// 4. Finalmente, destruir la sesión
session_destroy();

// 5. Redirigir al usuario a la página de inicio (login)
header("location: index.php");
exit;
?>