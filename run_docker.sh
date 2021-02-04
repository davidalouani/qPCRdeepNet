#__author__ = "David J. Alouani, david.alouani@uhhospitals.org, david.j.alouani@gmail.com"
#__date__ = "January 1, 2021 10:00:00 AM"
# qPCRdeepNet

#!/bin/bash
if [ $# -eq 0 ];
then
	echo ""
        echo "================================================================="	
	echo "No argument given, you need to specify the path to the imge folder (see readme.txt file)"
	echo "================================================================="
	echo ""
	exit 1
fi	
path_to_image_folder=$1  # This is the folder where you will put your images and generate ai predictions (see readme.txt for details)

sudo docker build -t qpcrdeepnet .

sudo docker run -it --rm --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" -v $path_to_image_folder:/media/data\
                                                                                                      -v /etc/timezone:/etc/timezone\
                                                                                                      -v ~/.ssh:/root/.ssh:ro qpcrdeepnet

