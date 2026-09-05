<?php
/**
 * Two servers, one per account, so phpMyAdmin can reach the database as either the read-only `demo`
 * user or the full-privilege `admin` user. phpMyAdmin's own image builds $cfg['Servers'] from
 * PMA_HOST/PMA_USER and gives every server the *same* credentials, which is why this file exists:
 * it is included last (see the "Include User Defined Settings Hook" at the end of
 * /etc/phpmyadmin/config.inc.php) and can therefore set each server separately.
 *
 * The passwords come from the environment so that .env stays the single place they are written; the
 * defaults match the image's baked accounts, so this works with no .env at all.
 */
$host = getenv('PMA_HOST') ?: 'mysql';
$port = getenv('PMA_PORT') ?: '3306';

$accounts = [
    1 => ['megasamples (read-only)',   'demo',  getenv('DEMO_PASSWORD')  ?: 'demo'],
    2 => ['megasamples (full access)', 'admin', getenv('ADMIN_PASSWORD') ?: 'admin'],
];

foreach ($accounts as $i => [$label, $user, $password]) {
    $cfg['Servers'][$i]['host'] = $host;
    $cfg['Servers'][$i]['port'] = $port;
    $cfg['Servers'][$i]['verbose'] = $label;
    // 'config' signs in without a login form; the server selector switches between the accounts.
    $cfg['Servers'][$i]['auth_type'] = 'config';
    $cfg['Servers'][$i]['user'] = $user;
    $cfg['Servers'][$i]['password'] = $password;
    $cfg['Servers'][$i]['AllowNoPassword'] = false;
}

// Land on the read-only account: the safe one should be the one you get by default.
$cfg['ServerDefault'] = 1;
