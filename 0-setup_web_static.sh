#!/usr/bin/env bash
# Script sets up your web servers for the deployment of web_static.
# Requirements:
#  - Install Nginx if it not already installed
#  - Create the folder /data/ if it doesn’t already exist
#  - Create the folder /data/web_static/ if it doesn’t already exist
#  - Create the folder /data/web_static/releases/ if it doesn’t already exist
#  - Create the folder /data/web_static/shared/ if it doesn’t already exist
#  - Create the folder /data/web_static/releases/test/ if it doesn’t already exist
#  - Create a fake HTML file /data/web_static/releases/test/index.html (with simple
#    content, to test your Nginx configuration)
#  - Create a symbolic link /data/web_static/current linked to the
#    /data/web_static/releases/test/ folder. If the symbolic link already exists,
#    it should be deleted and recreated every time the script is ran.
#  - Give ownership of the /data/ folder to the ubuntu user AND group (you can
#    assume this user and group exist). This should be recursive; everything inside
#    should be created/owned by this user/group.
#  - Update the Nginx configuration to serve the content of 
#    /data/web_static/current/ to hbnb_static (ex:
#    https://mydomainname.tech/hbnb_static). Don’t forget to restart Nginx after
#    updating the configuration:
#  - Use alias inside your Nginx configuration

# Update apt-get
sudo apt-get update

# Install nginx
sudo apt-get -y install nginx

# Create necessary directories and files
mkdir -p /data/web_static/{releases/test,shared}

# Create an empty index file -- add simple text to test config
sudo touch /data/web_static/releases/test/index.html
echo "Hello Word!" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Delete symbolic link, If exits
sudo rm -rf /data/web_static/current

# Create a symbolic link
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Change ownership of /data/ to 'ubuntu' user
sudo chown -R ubuntu:ubuntu /data

# Update Nginx config
replace_string="server_name _;\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current\/;\n\t\tautoindex off;\n\t}"
sudo sed -i "s/server_name _;/$replace_string/" /etc/nginx/sites-enabled/default

# Restart service
sudo service nginx restart
