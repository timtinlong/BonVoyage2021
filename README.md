# BonVoyage2021 (Bon Voyage 2021 Hackathon)
https://github.com/timtinlong/BonVoyage2021

## Windows Environment Setup (Anaconda)
$ conda create --name BonVoyage2021 python=3.9  
$ conda update -n base -c defaults conda  
$ conda activate BonVoyage2021  

## Install Relevant Libraries
https://stackoverflow.com/questions/11087795/whitespace-gone-from-pdf-extraction-and-strange-word-interpretation/11087993  
$ conda install pdfminer  
$ conda install tensorflow-gpu keras scikit-learn matplotlib numpy imutils  
$ conda install -c conda-forge opencv  
$ pip install pickle-mixin  

### MainScript.py
contains functions to save pdf to variable and extract text from the PDF files  

### pdf2images.py 
contains code used to pre-process pdf files into images for figure/equation/table detection

### DNN.py 
multi-class: https://www.pyimagesearch.com/2020/10/12/multi-class-object-detection-and-bounding-box-regression-with-keras-tensorflow-and-deep-learning/  
contains code to train bounding box and figure/table/equation detection  


