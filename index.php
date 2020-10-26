<!DOCTYPE html>
<html>
    <head>
        <title>Calescador</title>
    </head>
    <body>
        <?php
            session_start();
            if (!isset($_SESSION['id'])) {
                $_SESSION['id'] = 1;
            } else {
                $_SESSION['id'] += 1;
            }
            echo 'Hello World ' . $_SESSION['id'];
        ?>
    </body>
</html>
