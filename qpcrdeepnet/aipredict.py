__author__ = "David J. Alouani, david.alouani@uhhospitals.org, david.j.alouani@gmail.com"
__date__ = "January 1, 2021 10:00:00 AM"

import os
import subprocess
from time import strftime
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from scipy import stats
from keras.models import load_model
from keras.preprocessing import image

class miniqPCRdeepNet(object):
    def __init__(self, runParameters):
        self.runParameters = runParameters

    def initialize(self):
        self.runParameters['image_size'] = [299,299]
        class_file = self.runParameters['trained_convnet_file'].replace('model_','classes_').replace('.h5','.tsv')
        self.runParameters['trained_model'] = load_model(self.runParameters['trained_convnet_file'])
        df = pd.read_csv(class_file,sep='\t')
        self.runParameters['class_dictionary'] = {int(v):df.loc[df['Key']==v]['channelClass'].values[0] for v in list(df['Key'].values)}
        self.runParameters['data_path'] = '/media/data'
        self.timeStamep = strftime("%a, %d %b %Y") + ', ' + strftime('%X %Z')
        self.timeStamep = self.timeStamep.replace(' ', '').replace(',', '_').replace(':', '_')
        self.NumbCyles = 40

    def generateImages(self):
        self.runParameters['images'] = []
        self.IdLabels = {}
        for fl in self.runParameters['RT-PCR Rn'].keys():
            df   = self.runParameters['RT-PCR Rn'][fl]
            clms = list(df.columns)
            ix0  = clms.index('Rn')
            Ids = clms[:ix0]
            it = 0
            Tmp = []
            fl = fl.split('.')[0]
            self.IdLabels[fl] = Ids
            for ID1,row in df.iterrows():
                try:
                   it += 1
                   filename = row[Ids[0]]
                   for idinc in Ids[1:]:
                       if row[idinc].strip()!='':
                           filename += '_'+row[idinc]
                   filename += '_'+fl+'.png'
                   filename = os.path.join(self.runParameters['data_path'],'images/'+filename)

                   rn = [row[clms[ix]] for ix in range(ix0,len(clms))]
                   rn = rn[0:min(len(rn),self.NumbCyles)]
                   rnZs = stats.zscore([float(i) for i in rn],ddof =1)

                   fig = plt.figure(1, figsize=(2.99,2.99))
                   plt.yticks([])
                   plt.xticks([])
                   plt.xlim([0, 39])
                   plt.hlines(0, 0, 39, colors='black', linestyles='dashed')
                   plt.plot(rnZs, color='black')
                   fig.savefig(filename)
                   plt.clf()
                   Tmp.append([fl]+[row[idinc] for idinc in Ids]+[filename]) 
                except:
                   pass
            if not Tmp:
                continue
            self.runParameters['images'].append(Tmp)    

    def prepare(self, img):
        test_image = image.load_img(img, target_size = (self.runParameters['image_size'][0],self.runParameters['image_size'][1]))
        test_image = image.img_to_array(test_image)
        test_image = test_image.astype('float32')/255.
        img = np.expand_dims(test_image, axis = 0)
        return img

    def findRnFiles(self):
        try:
           cmd = '''cd %s; ls'''%os.path.join(self.runParameters['data_path'],'input')
           files = [x for x in subprocess.check_output(cmd,shell=True).decode('utf-8').split('\n') if (x.strip()!='') and (x.endswith('.txt') or x.endswith('.tsv'))]
        except:
           print ('no rt-pcr rn value files found...exiting')
           exit()
        self.runParameters['RT-PCR Rn'] = {}
        for fl in files:
           try:
              self.runParameters['RT-PCR Rn'][fl] = pd.read_csv(os.path.join(self.runParameters['data_path'],'input/'+fl),sep='\t')
           except:
               pass
        if len(self.runParameters['RT-PCR Rn'])==0:
            print ('the rn value file either contain no data or are not in tab seperated text files...exiting')
            exit()

    def getPredictions(self):
        self.generateImages()
        for Set in self.runParameters['images']:
           Data = [] 
           for setfile, sampleid,geneid,assayid,img in Set:
               processedImage = self.prepare(img)
               predProbability= self.runParameters['trained_model'].predict(processedImage)
               predClass      = self.runParameters['class_dictionary'][1] if predProbability[0]>0.5 else self.runParameters['class_dictionary'][0]
               Data.append([sampleid,geneid,assayid,img,predClass])
           try:
               df  = pd.DataFrame(Data,columns=self.IdLabels[setfile]+['image','prediction']).set_index(self.IdLabels[setfile][0])
               filename = os.path.join(self.runParameters['data_path'],'output/'+setfile+'_aiprediction_'+self.timeStamep+'.tsv')
               df.to_csv(filename,sep='\t')
               print ('generated prediction file : ',filename)
           except:
              continue
        print ('done!')  

    def Run(self):
        self.initialize()
        self.findRnFiles()
        self.getPredictions()


if __name__ == '__main__':
    runParameters = {}
    runParameters['trained_convnet_file'] = '/home/qpcrdeepnet/model_trn_covidcdc-ctf_40_ims_299_net_1_rgb.h5'
    miniqPCRdeepNet(runParameters).Run()
