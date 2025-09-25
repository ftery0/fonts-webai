import os
import math
import argparse
from typing import Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from dataset import GlyphFolderDataset
from model import Encoder, Decoder, Discriminator, StyleEmbedding


def train(
    data_root: str,
    num_styles: int = 25,
    image_size: int = 128,
    batch_size: int = 32,
    epochs: int = 50,
    lr: float = 2e-4,
    device: str = "auto",
):
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    dataset = GlyphFolderDataset(data_root, image_size=image_size)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=2, pin_memory=True)

    encoder = Encoder().to(device)
    style_emb = StyleEmbedding(num_styles=num_styles).to(device)
    decoder = Decoder().to(device)
    disc = Discriminator(num_styles=num_styles).to(device)

    adv_loss = nn.BCEWithLogitsLoss()
    l1_loss = nn.L1Loss()
    cat_loss = nn.CrossEntropyLoss()

    g_params = list(encoder.parameters()) + list(style_emb.parameters()) + list(decoder.parameters())
    d_params = list(disc.parameters())

    opt_g = optim.Adam(g_params, lr=lr, betas=(0.5, 0.999))
    opt_d = optim.Adam(d_params, lr=lr, betas=(0.5, 0.999))

    for epoch in range(1, epochs + 1):
        encoder.train(); decoder.train(); disc.train(); style_emb.train()
        for i, (x, style_id) in enumerate(loader, 1):
            x = x.to(device)
            style_id = style_id.to(device)

            # target style 를 랜덤 샘플 (self-translation도 허용)
            target_style = torch.randint(low=0, high=num_styles, size=style_id.shape, device=device)

            # 1) Discriminator step
            opt_d.zero_grad(set_to_none=True)
            real_logits, real_cat = disc(x)
            real_y = torch.ones_like(real_logits)
            d_real = adv_loss(real_logits, real_y)
            d_cat = cat_loss(real_cat, style_id)

            z = encoder(x)
            s = style_emb(target_style)
            x_fake = decoder(z, s)
            fake_logits, _ = disc(x_fake.detach())
            fake_y = torch.zeros_like(fake_logits)
            d_fake = adv_loss(fake_logits, fake_y)

            d_loss = d_real + d_fake + 0.1 * d_cat
            d_loss.backward()
            opt_d.step()

            # 2) Generator step (Encoder+StyleEmb+Decoder)
            opt_g.zero_grad(set_to_none=True)
            fake_logits_g, fake_cat = disc(x_fake)
            g_adv = adv_loss(fake_logits_g, torch.ones_like(fake_logits_g))
            g_l1 = l1_loss(x_fake, x)  # 간단 베이스라인: 타겟=입력 (self)
            g_cat = cat_loss(fake_cat, target_style)
            g_loss = g_adv + 10.0 * g_l1 + 0.1 * g_cat
            g_loss.backward()
            opt_g.step()

            if i % 50 == 0:
                print(f"[Epoch {epoch}/{epochs}] [Iter {i}/{len(loader)}] D: {d_loss.item():.3f} | G: {g_loss.item():.3f}")

        # TODO: 체크포인트 저장/샘플 저장


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", required=True, type=str)
    parser.add_argument("--num-styles", type=int, default=25)
    parser.add_argument("--image-size", type=int, default=128)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--device", type=str, default="auto")
    args = parser.parse_args()

    train(
        data_root=args.data_root,
        num_styles=args.num_styles,
        image_size=args.image_size,
        batch_size=args.batch_size,
        epochs=args.epochs,
        lr=args.lr,
        device=args.device,
    )


