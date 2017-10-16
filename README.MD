
Used to display images for selection to a user and then report back their selection. 

It is important to update the IP of the server in settings.py

Web page is displayed at SERVER_IP specified in settings:
`http://SERVER_IP://IMAGE_SERVER_PORT`

Start by running `sh launch_server.sh` from the cloned directory. Then you can 
get a user selection using the module.

To update images shown to user and report back selection, call the function: 
`get_user_selection(directory_with_images_to_show_users)`
from  update_images.py. A user selection of the image name or "None" is returned
within the timeout period specified in settings.py.
