import os
from typing import List, Tuple
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as T


class GlyphFolderDataset(Dataset):
    """
    루트 디렉토리 구조 예시:
    root/
      000/ img1.png, img2.png, ...  (style_id=0)
      001/ ...                       (style_id=1)
      ...
    각 폴더 이름이 style/category id 로 간주됩니다.
    이미지 크기는 128x128 흑백으로 로드합니다.
    """

    def __init__(self, root_dir: str, image_size: int = 128):
        self.root_dir = root_dir
        self.samples: List[Tuple[str, int]] = []
        style_dirs = sorted([d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))])
        for style in style_dirs:
            style_path = os.path.join(root_dir, style)
            try:
                style_id = int(style)
            except ValueError:
                # 폴더명이 숫자가 아니어도 허용: 사전순 id 부여
                style_id = style_dirs.index(style)
            for fname in os.listdir(style_path):
                if not fname.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                    continue
                self.samples.append((os.path.join(style_path, fname), style_id))

        self.transform = T.Compose([
            T.Grayscale(num_output_channels=1),
            T.Resize((image_size, image_size), interpolation=T.InterpolationMode.BILINEAR),
            T.ToTensor(),  # [0,1]
        ])

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx: int):
        path, style_id = self.samples[idx]
        img = Image.open(path).convert("L")
        x = self.transform(img)  # (1, H, W)
        return x, style_id


