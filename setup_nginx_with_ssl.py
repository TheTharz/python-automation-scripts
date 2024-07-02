import os
import subprocess

def install_certbot():
    # Install Certbot if not already installed
    try:
        subprocess.run(["certbot", "--version"], check=True)
        print("Certbot is already installed.")
    except subprocess.CalledProcessError:
        print("Installing Certbot...")
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "certbot", "python3-certbot-nginx", "-y"], check=True)
        print("Certbot installed successfully.")

def generate_nginx_config(domain, port):
    nginx_config = f"""
server {{
    listen 80;
    server_name {domain};

    location / {{
        return 301 https://$host$request_uri;
    }}
}}

server {{
    listen 443 ssl;
    server_name {domain};

    ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {{
        proxy_pass http://localhost:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""

    config_path = f"/etc/nginx/sites-available/{domain}"
    with open(config_path, "w") as f:
        f.write(nginx_config)

    # Create a symbolic link to enable the site
    enabled_path = f"/etc/nginx/sites-enabled/{domain}"
    if not os.path.exists(enabled_path):
        os.symlink(config_path, enabled_path)

    print(f"NGINX configuration file for {domain} generated successfully.")

def reload_nginx():
    subprocess.run(["sudo", "systemctl", "reload", "nginx"], check=True)
    print("NGINX reloaded successfully.")

def obtain_ssl_certificate(domain):
    try:
        subprocess.run(["sudo", "certbot", "--nginx", "-d", domain], check=True)
        print(f"SSL certificate obtained and configured for {domain}.")
    except subprocess.CalledProcessError as e:
        print(f"Error obtaining SSL certificate: {e}")

if __name__ == "__main__":
    domain = input("Enter your domain name: ")
    port = input("Enter the port your application is running on (e.g., 3000): ")

    # Install Certbot
    install_certbot()

    # Generate the NGINX configuration file
    generate_nginx_config(domain, port)

    # Reload NGINX to apply the new configuration
    reload_nginx()

    # Obtain and install SSL certificate using Certbot
    obtain_ssl_certificate(domain)

    print("NGINX configuration with SSL support and HTTP to HTTPS redirection has been set up.")
