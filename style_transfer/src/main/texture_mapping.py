from __future__ import division
import os
import argparse
import glob

import torch
import torch.nn as nn
import numpy as np
from skimage.io import imread, imsave
from skimage.transform import resize
import tqdm
import imageio

import neural_renderer as nr

current_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_dir, 'data')

class Model(nn.Module):
    def __init__(self, filename_obj, filename_ref):
        super(Model, self).__init__()
        vertices, faces = nr.load_obj(filename_obj)
        self.register_buffer('vertices', vertices[None, :, :])
        self.register_buffer('faces', faces[None, :, :])

        # create textures
        texture_size = 4
        textures = torch.zeros(1, self.faces.shape[1], texture_size, texture_size, texture_size, 3, dtype=torch.float32)
        self.textures = nn.Parameter(textures)

        # load reference image
        image_ref = torch.from_numpy(resize((imread(filename_ref).astype('float32') / 255.), (256, 256))).permute(2,0,1)[None, ::]
        self.register_buffer('image_ref', image_ref)

        # setup renderer
        renderer = nr.Renderer(camera_mode='look_at')
        renderer.perspective = False
        renderer.light_intensity_directional = 0.0
        renderer.light_intensity_ambient = 1.0
        self.renderer = renderer


    def forward(self):
        self.renderer.eye = nr.get_points_from_angles(2.732, 0, np.random.uniform(0, 360))
        image, _, _ = self.renderer(self.vertices, self.faces, torch.tanh(self.textures))
        loss = torch.sum((image - self.image_ref) ** 2)
        return loss


def make_gif(filename):
    with imageio.get_writer(filename, mode='I') as writer:
        for filename in sorted(glob.glob('/tmp/_tmp_*.png')):
            writer.append_data(imageio.imread(filename))
            os.remove(filename)
    writer.close()

class MapTexture():
    def __init__(self, filename_obj, filename_ref, filename_output_gif):
        self.filename_obj = filename_obj
        self.texture_map_image = filename_ref
        self.filename_output_gif = filename_output_gif

    def train(self):
        model = Model(self.filename_obj, self.texture_map_image)
        model.cuda()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.1, betas=(0.5,0.999))
        loop = tqdm.tqdm(range(300))
        for _ in loop:
            loop.set_description('Optimizing')
            optimizer.zero_grad()
            loss = model()
            loss.backward()
            optimizer.step()

        # draw object
        loop = tqdm.tqdm(range(0, 360, 4))
        for num, azimuth in enumerate(loop):
            loop.set_description('Drawing')
            model.renderer.eye = nr.get_points_from_angles(2.732, 0, azimuth)
            images, _, _ = model.renderer(model.vertices, model.faces, torch.tanh(model.textures))
            image = images.detach().cpu().numpy()[0].transpose((1, 2, 0))
            imsave('/tmp/_tmp_%04d.png' % num, image)
        make_gif(self.filename_output_gif)

        self.model = model

    def save_obj(self, filename):
        vertices = self.model.vertices
        faces = self.model.faces
        textures = self.model.textures
        nr.save_obj(filename, torch.squeeze(vertices), torch.squeeze(faces), torch.squeeze(textures))