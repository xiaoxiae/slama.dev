#!/usr/bin/env python3
"""
Generate fake credential files as honeypots.
These catch bots scanning for exposed secrets.
"""

import random
import string
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "public"


def random_string(length: int) -> str:
    charset = string.ascii_letters + string.digits
    return "".join(random.choice(charset) for _ in range(length))


def fake_password() -> str:
    return random_string(16)


def generate_env_file() -> str:
    return (
        f"DATABASE_URL=postgresql://user:{fake_password()}@localhost/db\n"
        f"API_KEY=sk_{random_string(32)}\n"
        f"SECRET_KEY={random_string(48)}\n"
    )


def generate_aws_credentials() -> str:
    return (
        "[default]\n"
        f"aws_access_key_id = AKIA{random_string(16)}\n"
        f"aws_secret_access_key = {random_string(40)}\n"
    )


def generate_php_config() -> str:
    return (
        "<?php\n"
        "$db_host = 'localhost';\n"
        "$db_user = 'admin';\n"
        f"$db_pass = '{fake_password()}';\n"
        "?>"
    )


def generate_wp_config() -> str:
    return (
        "<?php\n"
        "define('DB_NAME', 'wordpress');\n"
        "define('DB_USER', 'wp_user');\n"
        f"define('DB_PASSWORD', '{fake_password()}');\n"
        f"define('AUTH_KEY', '{random_string(64)}');\n"
        "?>"
    )


def generate_django_settings() -> str:
    return (
        f"SECRET_KEY = '{random_string(50)}'\n"
        "DATABASES = {\n"
        "  'default': {\n"
        f"    'PASSWORD': '{fake_password()}',\n"
        "  }\n"
        "}\n"
    )


def generate_htaccess() -> str:
    return (
        "# Apache configuration\n"
        "RewriteEngine On\n"
        "RewriteCond %{HTTPS} off\n"
        "RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n"
        "\n"
        "# Database credentials\n"
        "SetEnv DB_HOST localhost\n"
        f"SetEnv DB_USER {random_string(8)}\n"
        f"SetEnv DB_PASS {fake_password()}\n"
    )


def generate_web_config() -> str:
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<configuration>\n"
        "  <appSettings>\n"
        f'    <add key="Database" value="Server=localhost;User Id={random_string(8)};Password={fake_password()};"/>\n'
        f'    <add key="ApiKey" value="{random_string(40)}"/>\n'
        "  </appSettings>\n"
        "</configuration>\n"
    )


def generate_database_yml() -> str:
    return (
        "default: &default\n"
        "  adapter: postgresql\n"
        "  encoding: unicode\n"
        "  pool: 5\n"
        "  host: localhost\n"
        f"  username: {random_string(10)}\n"
        f"  password: {fake_password()}\n"
        "\n"
        "production:\n"
        "  <<: *default\n"
        "  database: app_production\n"
        f"  password: {random_string(24)}\n"
    )


SECRETS = {
    ".env": generate_env_file,
    ".env.local": generate_env_file,
    ".env.production": generate_env_file,
    ".aws/credentials": generate_aws_credentials,
    "config.php": generate_php_config,
    "wp-config.php": generate_wp_config,
    "settings.py": generate_django_settings,
    ".htaccess": generate_htaccess,
    "web.config": generate_web_config,
    "app/config/database.yml": generate_database_yml,
    "config/database.yml": generate_database_yml,
    "admin/config.php": generate_php_config,
}


def main():
    if not OUTPUT_DIR.exists():
        print(
            f"ERROR: Output directory {OUTPUT_DIR} does not exist. Run hugo build first."
        )
        return 1

    for path, generator in SECRETS.items():
        file_path = OUTPUT_DIR / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(generator())
        print(f"Generated {path}")

    print(f"\nGenerated {len(SECRETS)} honeypot files.")
    return 0


if __name__ == "__main__":
    exit(main())
