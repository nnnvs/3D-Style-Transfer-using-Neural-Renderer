# 3D Style Transfer using Neural Renderer

This repository contains implementation of the Final Project of Introduction to Deep Learning Systems at NYU Courant. <br>
Contributors: <br>
Nikhil Vinay Sharma (nv2095@nyu.edu) <br>
Vishv Shrava Sharma (vss7121@vss.edu) <br>

# System requirements
Tested on NYU Greene Cluster</br>
GPU </br>
Cuda 10.2 (Should work on higher cuda versions as well) </br>

# Setting up the environment
1. Activate new environment in which you want to test our code.
2. `pip install -r requirements.txt`
3. `pip3 install torch==1.8.1+cu102 torchvision==0.9.1+cu102 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html`
4. `cd style_transfer/src/neural_renderer`
5. `python setup.py install --user`
6. `bash ./style_transfer/src/scripts/run.sh`
7. Resulting `.gif` images will be available in the examples/data/results folder. Output gif file will be `bunny_gogh2.gif`. Please note that we also apply texture mapping to our inputs for further results and the output for that will be `stylized_and_textured_bunny_gogh2.gif`.
