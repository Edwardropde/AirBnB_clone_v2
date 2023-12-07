#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Create necessary folders and files
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_text="location /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"
sudo sed -i "/^\s*server\s*{/a $config_text" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
