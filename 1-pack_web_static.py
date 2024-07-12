#!/usr/bin/python3
"""
Fabric script generates a  .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack.
Requirements:
  - Prototype: def do_pack():
  - All files in the folder web_static must be added to the final archive
  - All archives must be stored in the folder versions (your function should
    create this folder if it doesn’t exist)
  - The name of the archive created must be
    web_static_<year><month><day><hour><minute><second>.tgz
  - The function do_pack must return the archive path if the archive has been
    correctly generated. Otherwise, it should return None
"""
from invoke import local
from datetime import datetime
import os


def do_pack():
    """Function generates a tgz archive"""

    # Create versions folder, If not exists
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Get the time the archive is generated
    current = datetime.now()
    date_str = current.strftime("%Y%m%d%H%M%S")

    # Create the filename
    archive_name = "versions/web_static_{}.tgz".format(date_str)

    # Define local path -- web_static
    local_path = "web_static"

    # If local_path, not exists
    if not os.path.exists(local_path):
        return None

    # run command -- on the remote server
    result = local(f"tar -czvf {archive_name} {local_path}")

    # Handle result
    if result.return_code == 0:
        return archive_name
    else:
        return None
