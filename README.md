# 3D Style Transfer using Neural Renderer

Conventionally, style transfer from 2D image to 3D object is done by mapping the texture from the image to the  3D surface. However, it is interesting to see if the shape of the object itself changes as per the style of the image.  We have used a neural renderer-based approach to transfer style from 2D image to 3D mesh. Here, by  style, we mean the changes in the texture and surface. A polygon mesh is a promising candidate for modeling the 3D world behind 2D images based upon its compactness and geometric properties. However, it is not straightforward to  model a polygon mesh from 2D images using neural networks because the conversion from a 3D model to an image,  or rendering, involves a discrete operation called rasterization, which prevents back-propagation. Thus, we have used  a neural renderer that approximates gradient for rasterization that enables the integration of rendering into neural networks. We have re-implemented the existing neural-renderer based 2D to 3D mesh editing and texture mapping approach using VGG-16 feature maps to transfer style onto 3D objects in PyTorch.

This repository contains implementation of the Final Project of Introduction to Deep Learning Systems at NYU Courant. <br>
Contributors: <br>
Nikhil Vinay Sharma (nv2095@nyu.edu) <br>
Vishv Shrava Sharma (vss7121@vss.edu) <br>

## System requirements
Tested on NYU Greene Cluster</br>
GPU </br>
Cuda 10.2 (Should work on higher cuda versions as well) </br>

## Setting up the environment
1. Activate new environment in which you want to test our code.
2. `pip install -r requirements.txt`
3. `pip3 install torch==1.8.1+cu102 torchvision==0.9.1+cu102 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html`
4. `cd style_transfer/src/neural_renderer`
5. `python setup.py install --user`
6. `bash ./style_transfer/src/scripts/run.sh`
7. Resulting `.gif` images will be available in the `scripts/data/results` folder. Output gif file will be `bunny_gogh2.gif`. Please note that we also apply texture mapping to our inputs for further results and the output for that will be `stylized_and_textured_bunny_gogh2.gif`.

The jupyter notebook file `Installation & first run.ipynb` takes you through the process of installing and running a few examples.

## To run examples
After installation, run `bash ./style_transfer/src/scripts/run.sh` and see the results in `scripts/data/results`

## Code Structure
The codebase has been divided into modules. All core code is present in the style_transfer/src folder. The following modules are present:
- `src/jupyter` contains .ipynb notebook files used for experimentation.
- `src/main` contains the driver code for running style transfer
- `src/scripts` contains bash scripts for running 
- `src/scripts/data` contains the data used - 3D models, style images and outputs
- `src/neural_renderer` contains the code for pytorch port of `3D Neural Mesh Renderer` by Hiroharu et al, which is used for backpropagation 

## Output

<div>
   <img src="https://raw.githubusercontent.com/nnnvs/3D-Style-Transfer-using-Neural-Renderer/main/style_transfer/src/scripts/data/styles/gris1.jpg" width="30%" height="30%">
   <img src="https://raw.githubusercontent.com/nnnvs/3D-Style-Transfer-using-Neural-Renderer/main/style_transfer/src/scripts/data/results/teapot.gif" width="30%" height="30%">
   <img src="https://raw.githubusercontent.com/nnnvs/3D-Style-Transfer-using-Neural-Renderer/main/style_transfer/src/scripts/data/results/unnamed_1.gif" width="30%" height="30%">
</div>
<div>
   <img src="https://raw.githubusercontent.com/nnnvs/3D-Style-Transfer-using-Neural-Renderer/main/style_transfer/src/scripts/data/styles/gogh2.jpg" width="30%" height="30%">
   <img src="https://raw.githubusercontent.com/nnnvs/3D-Style-Transfer-using-Neural-Renderer/main/style_transfer/src/scripts/data/results/teapot.gif" width="30%" height="30%">
   <img src="https://raw.githubusercontent.com/nnnvs/3D-Style-Transfer-using-Neural-Renderer/main/style_transfer/src/scripts/data/results/unnamed_2.gif" width="30%" height="30%">
</div>
<div>
   <img src="https://raw.githubusercontent.com/nnnvs/3D-Style-Transfer-using-Neural-Renderer/main/style_transfer/src/scripts/data/styles/coupland1.jpg" width="30%" height="30%">
   <img src="https://raw.githubusercontent.com/nnnvs/3D-Style-Transfer-using-Neural-Renderer/main/style_transfer/src/scripts/data/results/teapot.gif" width="30%" height="30%">
   <img src="https://raw.githubusercontent.com/nnnvs/3D-Style-Transfer-using-Neural-Renderer/main/style_transfer/src/scripts/data/results/unnamed.gif" width="30%" height="30%">
</div>


