from __future__ import print_function

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
import torchvision.models as models
from torchvision.utils import save_image
import sys
import copy

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class ContentLoss(nn.Module):

    def __init__(self, target,):
        super(ContentLoss, self).__init__()
        # we 'detach' the target content from the tree used
        # to dynamically compute the gradient: this is a stated value,
        # not a variable. Otherwise the forward method of the criterion
        # will throw an error.
        self.target = target.detach()

    def forward(self, input):
        self.loss = F.mse_loss(input, self.target)
        return input


class StyleLoss(nn.Module):

    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = gram_matrix(target_feature).detach()

    def forward(self, input):
        G = gram_matrix(input)
        self.loss = F.mse_loss(G, self.target)
        return input


class Normalization(nn.Module):
    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        # .view the mean and std to make them [C x 1 x 1] so that they can
        # directly work with image Tensor of shape [B x C x H x W].
        # B is batch size. C is number of channels. H is height and W is width.
        self.mean = torch.tensor(mean).view(-1, 1, 1)
        self.std = torch.tensor(std).view(-1, 1, 1)

    def forward(self, img):
        # normalize img
        return (img - self.mean) / self.std


def gram_matrix(input):
    a, b, c, d = input.size()  # a=batch size(=1)
    # b=number of feature maps
    # (c,d)=dimensions of a f. map (N=c*d)

    features = input.view(a * b, c * d)  # resise F_XL into \hat F_XL

    G = torch.mm(features, features.t())  # compute the gram product

    # we 'normalize' the values of the gram matrix
    # by dividing by the number of element in each feature maps.
    return G.div(a * b * c * d)


def get_style_model_and_losses(cnn, normalization_mean, normalization_std,
                               style_img, content_img,
                               style_layers=['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']):
    cnn = copy.deepcopy(cnn)

    # normalization module
    normalization = Normalization(normalization_mean, normalization_std).to(device)

    # just in order to have an iterable access to or list of content/syle
    # losses
    style_losses = []

    # assuming that cnn is a nn.Sequential, so we make a new nn.Sequential
    # to put in modules that are supposed to be activated sequentially
    model = nn.Sequential(normalization)

    i = 0  # increment every time we see a conv
    for layer in cnn.children():
        if isinstance(layer, nn.Conv2d):
            i += 1
            name = 'conv_{}'.format(i)
        elif isinstance(layer, nn.ReLU):
            name = 'relu_{}'.format(i)
            # The in-place version doesn't play very nicely with the ContentLoss
            # and StyleLoss we insert below. So we replace with out-of-place
            # ones here.
            layer = nn.ReLU(inplace=False)
        elif isinstance(layer, nn.MaxPool2d):
            name = 'pool_{}'.format(i)
        elif isinstance(layer, nn.BatchNorm2d):
            name = 'bn_{}'.format(i)
        else:
            raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))

        model.add_module(name, layer)

        if name in style_layers:
            # add style loss:
            target_feature = model(style_img).detach()
            style_loss = StyleLoss(target_feature)
            model.add_module("style_loss_{}".format(i), style_loss)
            style_losses.append(style_loss)

    # now we trim off the layers after the last content and style losses
    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
            break

    model = model[:(i + 1)]

    return model, style_losses


def get_input_optimizer(input_img):
    # this line to show that input is a parameter that requires a gradient
    optimizer = optim.LBFGS([input_img.requires_grad_()])
    return optimizer


def run_style_transfer(cnn, normalization_mean, normalization_std,
                       content_img, style_img,style_layers, num_steps=300):
    """Run the style transfer."""
    model, style_losses = get_style_model_and_losses(cnn,normalization_mean, normalization_std, style_img, content_img,style_layers)
    model(content_img)
    style_score = 0
    for sl in style_losses:
        style_score += sl.loss

    return style_score


def image_loader(image_name,imsize,device):
    loader = transforms.Compose([transforms.Resize((imsize,imsize)),transforms.ToTensor()])
    image = Image.open(image_name)
    
    # fake batch dimension required to fit network's input dimensions
    image = loader(image).unsqueeze(0)
    return image.to(device, torch.float)

def main():
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

	# desired size of the output image
	imsize = 512 if torch.cuda.is_available() else 128  # use small size if no gpu

	loader = transforms.Compose([
		transforms.Resize((imsize, imsize)),  # scale imported image
		transforms.ToTensor()])  # transform it into a torch tensor

	style_img = image_loader(sys.argv[1],imsize,device)
	content_img = image_loader(sys.argv[2],imsize,device)
	content_img = content_img[:, 0:3]

	cnn = models.vgg19(pretrained=True).features.to(device).eval()
	cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
	cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)
	content_layers_default = ['conv_4']
	style_layers_default = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']
	input_img = content_img.clone()

	#The commented code is for handling the relevant area in a png image through a mask.
    #transparency_map = content_img[:,3]
	#transparency_map = torch.unsqueeze(transparency_map,1)
	content_img = content_img[:,0:3]
	#mask_img = (content_img > 0.0005).float()
	output = run_style_transfer(cnn, cnn_normalization_mean, cnn_normalization_std, content_img, style_img, content_img)
	#output = output*mask_img
	#output = torch.cat((output,transparency_map),dim=1)
	#output = F.upsample(output,size=(137,137), mode='bilinear')
	save_image(output, 'output.png',format='png')

if __name__ == "__main__":
    main()