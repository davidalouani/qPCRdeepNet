
#__author__ = "David J. Alouani, david.alouani@uhhospitals.org, david.j.alouani@gmail.com"
#__date__ = "January 1, 2021 10:00:00 AM"

# qPCRdeepNet

Building and running the qPCRdeepNet docker image:

1) create a folder where you will have you images, e.g.:
    /home/johnsmith/myimages. This folder needs to have 2 subfolders: input and output
    i.e.: /home/johnsmith/myimages/input    &  /home/johnsmith/myimages/output

2) copy your images to /home/johnsmith/myimages/input/

3) Download the qPCRdeepNet repository from GitHub

4) From your linux terminal window, go to the folder you just downloaded, and type: ./run_docker.sh path_to_main_images_folder
   this path (path_to_main_images_folder) is the same as (/home/johnsmith/myimages). This step simply linkes the image folder outside the container to a data folder inside the container.
   e.g.:   ./run_docker.sh  /home/johnsmith/myimages

5) Once the container is running and you can see a new terminal window (with root in the prompt). Type: ./runai.sh
   if there are any images under /home/johnsmith/myimages/input/ the code will generate text (.tsv file) under /home/johnsmith/myimages/output, with the class prediction for each image
   Note: The images must be in .png format. The image size needs to be 299x299 pixels, otherwise the code will resize it to 299x299 pixels.
