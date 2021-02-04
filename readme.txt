#__author__ = "David J. Alouani, david.alouani@uhhospitals.org, david.j.alouani@gmail.com"
#__date__ = "January 1, 2021 10:00:00 AM"
# qPCRdeepNet


1) Create a main data folder, e.g.: /home/johnsmith/my_rtpcr_data. This folder needs to have 3 subfolders: input, output, images i.e.: /home/johnsmith/my_rtpcr_data/input,& /home/johnsmith/my_rtpcr_data/output, /home/johnsmith/my_rtpcr_data/images

2) Create text file(s) (tab separated) with Rn values (see examples/input/ folder for sample file). In this file each row represents a series of Ids and list or Rn values, eg.

id1	id2	id2	Rn																																													
sample1	gene1	Assay1	683415.94	686510.56	691409.06	690424.75	690410.8	691440.4	692370.3	692140.7	693066.1	694507	691851.9	693472.75	692769	696196.2	694141.25	694287.2	693789.9	693828.94	693252.1	692890.7	692911.2	693599.6	694958.25	694134	694648.56	693575.25	696802.2	693848.25	692493.8	691407.9	691325	690727.56	691741.1	691339	691134.25	691257.94	690766.94	690680.56	689835.2	690221.94	693917.5	691789.44	689851.3	691586.6	692019.56	690964.8

Note: user specific column labels (eg. sampleID, wellID, etc..) can be used in these tab seperated files, however, the last labeled column must be labeled "Rn"


3) To build and run qPCRdeepNet docker image, download the qPCRdeepNet repository from GitHub

4) From your linux terminal window, go to the folder you just downloaded from GitHub, and type: ./run_docker.sh path_to_main_images_folder this path (path_to_main_images_folder) is the same as (/home/johnsmith/my_rtpcr_data). This step simply links the data folder outside the container to a data folder inside the container. e.g.: ./run_docker.sh /home/johnsmith/my_rtpcr_data

Once the container is runs, it will automatically process all Rn text files, and generate both normalized images and ai predictions under /home/johnsmith/my_rtpcr_data/images and /home/johnsmith/my_rtpcr_data/output respectively

Note: qPCRdeepNet does not require gpu to run and generate predictions. It will run on cpu machine ( the option CUDA_VISIBLE_DEVICES="" is set by default).
