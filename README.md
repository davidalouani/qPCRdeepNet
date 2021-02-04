
#__author__ = "David J. Alouani, david.alouani@uhhospitals.org, david.j.alouani@gmail.com"
#__date__ = "January 1, 2021 10:00:00 AM"

# qPCRdeepNet

Building and running qPCRdeepNet docker image:

1) Create a folder where you will have you images, e.g.:
    /home/johnsmith/myimages. This folder needs to have 2 subfolders: input and output
    i.e.: /home/johnsmith/myimages/input    &  /home/johnsmith/myimages/output

2) Copy your images to /home/johnsmith/myimages/input/
   note: images must be in (.png) format. The image size needs to be 299x299 pixels, otherwise the code will resize it to 299x299 pixels.

3) Download the qPCRdeepNet repository from GitHub

4) From your linux terminal window, go to the folder you just downloaded, and type: ./run_docker.sh path_to_main_images_folder
   this path (path_to_main_images_folder) is the same as (/home/johnsmith/myimages). This step simply linkes the image folder outside the container to a data folder inside the container.
   e.g.:   ./run_docker.sh  /home/johnsmith/myimages

5) Once the container is runs it will automatically process any images under the input folder, and generate an output text (.tsv) file (time stamped) under /home/johnsmith/myimages/output   
