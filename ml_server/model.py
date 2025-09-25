import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, in_channels: int = 1, latent_dim: int = 256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_channels, 32, 4, 2, 1), nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(32, 64, 4, 2, 1), nn.BatchNorm2d(64), nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 128, 4, 2, 1), nn.BatchNorm2d(128), nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(128, 256, 4, 2, 1), nn.BatchNorm2d(256), nn.LeakyReLU(0.2, inplace=True),
        )
        self.proj = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 8 * 8, latent_dim),
        )

    def forward(self, x):
        h = self.net(x)
        z = self.proj(h)
        return z


class Decoder(nn.Module):
    def __init__(self, latent_dim: int = 256, style_dim: int = 64, out_channels: int = 1):
        super().__init__()
        in_dim = latent_dim + style_dim
        self.fc = nn.Sequential(
            nn.Linear(in_dim, 256 * 8 * 8), nn.ReLU(inplace=True)
        )
        self.net = nn.Sequential(
            nn.ConvTranspose2d(256, 128, 4, 2, 1), nn.BatchNorm2d(128), nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, 4, 2, 1), nn.BatchNorm2d(64), nn.ReLU(True),
            nn.ConvTranspose2d(64, 32, 4, 2, 1), nn.BatchNorm2d(32), nn.ReLU(True),
            nn.ConvTranspose2d(32, out_channels, 4, 2, 1), nn.Sigmoid(),
        )

    def forward(self, z, style_vec):
        concat = torch.cat([z, style_vec], dim=1)
        h = self.fc(concat).view(-1, 256, 8, 8)
        x_hat = self.net(h)
        return x_hat


class Discriminator(nn.Module):
    def __init__(self, in_channels: int = 1, num_styles: int = 25):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 32, 4, 2, 1), nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(32, 64, 4, 2, 1), nn.BatchNorm2d(64), nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 128, 4, 2, 1), nn.BatchNorm2d(128), nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(128, 256, 4, 2, 1), nn.BatchNorm2d(256), nn.LeakyReLU(0.2, inplace=True),
        )
        self.flatten = nn.Flatten()
        self.adv_head = nn.Linear(256 * 8 * 8, 1)
        self.cat_head = nn.Linear(256 * 8 * 8, num_styles)

    def forward(self, x):
        h = self.features(x)
        f = self.flatten(h)
        real_fake = self.adv_head(f)
        cat_logits = self.cat_head(f)
        return real_fake, cat_logits


class StyleEmbedding(nn.Module):
    def __init__(self, num_styles: int = 25, style_dim: int = 64):
        super().__init__()
        self.embed = nn.Embedding(num_styles, style_dim)

    def forward(self, style_id):
        return self.embed(style_id)


