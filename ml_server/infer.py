import os
from typing import Optional
import torch
from PIL import Image
import torchvision.transforms as T

from model import Encoder, Decoder, StyleEmbedding


class InferencePipeline:
    def __init__(self, ckpt_dir: str, num_styles: int = 25, device: str = "auto"):
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        self.device = device
        self.encoder = Encoder().to(self.device).eval()
        self.decoder = Decoder().to(self.device).eval()
        self.style_emb = StyleEmbedding(num_styles=num_styles).to(self.device).eval()
        # TODO: 가중치 로드 (여기서는 랜덤 초기화 상태)

        self.pre = T.Compose([
            T.Grayscale(num_output_channels=1),
            T.Resize((128, 128)),
            T.ToTensor(),
        ])

    @torch.inference_mode()
    def infer_image(self, pil_image: Image.Image, target_style_id: int = 0) -> Image.Image:
        x = self.pre(pil_image).unsqueeze(0).to(self.device)
        z = self.encoder(x)
        s = self.style_emb(torch.tensor([target_style_id], device=self.device))
        y = self.decoder(z, s)
        y = (y.squeeze(0).cpu() * 255.0).clamp(0, 255).byte().numpy()[0]
        return Image.fromarray(y, mode="L")


