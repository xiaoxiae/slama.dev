module Jekyll
  class SecretGenerator < Generator
    safe true
    priority :high

    def generate(site)
      site.config['secrets'] = {
        '.env' => generate_env_file,
        '.env.local' => generate_env_file,
        '.env.production' => generate_env_file,
        '.aws/credentials' => generate_aws_credentials,
        'config.php' => generate_php_config,
        'wp-config.php' => generate_wp_config,
        'settings.py' => generate_django_settings,
        '.htaccess' => generate_htaccess,
        'web.config' => generate_web_config,
        'app/config/database.yml' => generate_database_yml,
        'config/database.yml' => generate_database_yml,
        'admin/config.php' => generate_php_config
      }
    end

    private

    def generate_env_file
      "DATABASE_URL=postgresql://user:#{fake_password}@localhost/db\n" \
      "API_KEY=sk_#{random_string(32)}\n" \
      "SECRET_KEY=#{random_string(48)}\n"
    end

    def generate_aws_credentials
      "[default]\n" \
      "aws_access_key_id = AKIA#{random_string(16)}\n" \
      "aws_secret_access_key = #{random_string(40)}\n"
    end

    def generate_php_config
      "<?php\n" \
      "\$db_host = 'localhost';\n" \
      "\$db_user = 'admin';\n" \
      "\$db_pass = '#{fake_password}';\n" \
      "?>"
    end

    def generate_wp_config
      "<?php\n" \
      "define('DB_NAME', 'wordpress');\n" \
      "define('DB_USER', 'wp_user');\n" \
      "define('DB_PASSWORD', '#{fake_password}');\n" \
      "define('AUTH_KEY', '#{random_string(64)}');\n" \
      "?>"
    end

    def generate_django_settings
      "SECRET_KEY = '#{random_string(50)}'\n" \
      "DATABASES = {\n" \
      "  'default': {\n" \
      "    'PASSWORD': '#{fake_password}',\n" \
      "  }\n" \
      "}\n"
    end

    def generate_git_config
      "[core]\n" \
      "repositoryformatversion = 0\n" \
      "filemode = true\n" \
      "token = #{random_string(40)}\n"
    end

    def generate_htaccess
      "# Apache configuration\n" \
      "RewriteEngine On\n" \
      "RewriteCond %{HTTPS} off\n" \
      "RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n" \
      "\n" \
      "# Database credentials\n" \
      "SetEnv DB_HOST localhost\n" \
      "SetEnv DB_USER #{random_string(8)}\n" \
      "SetEnv DB_PASS #{fake_password}\n"
    end

    def generate_web_config
      "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" \
      "<configuration>\n" \
      "  <appSettings>\n" \
      "    <add key=\"Database\" value=\"Server=localhost;User Id=#{random_string(8)};Password=#{fake_password};\"/>\n" \
      "    <add key=\"ApiKey\" value=\"#{random_string(40)}\"/>\n" \
      "  </appSettings>\n" \
      "</configuration>\n"
    end

    def generate_database_yml
      "default: &default\n" \
      "  adapter: postgresql\n" \
      "  encoding: unicode\n" \
      "  pool: 5\n" \
      "  host: localhost\n" \
      "  username: #{random_string(10)}\n" \
      "  password: #{fake_password}\n" \
      "\n" \
      "production:\n" \
      "  <<: *default\n" \
      "  database: app_production\n" \
      "  password: #{random_string(24)}\n"
    end

    def fake_password
      @fake_password ||= random_string(16)
    end

    def random_string(length)
      charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
      (0...length).map { charset[rand(charset.length)] }.join
    end
  end

  class SecretWriter
    def initialize(config)
      @config = config
    end

    def write(dest)
      secrets = @config.fetch('secrets', {})
      secrets.each do |path, content|
        file_path = File.join(dest, path)
        dir_path = File.dirname(file_path)

        unless File.directory?(dir_path)
          FileUtils.mkdir_p(dir_path)
        end

        File.write(file_path, content)
      end
    end
  end

  Hooks.register :site, :post_write do |site|
    SecretWriter.new(site.config).write(site.dest)
  end
end
