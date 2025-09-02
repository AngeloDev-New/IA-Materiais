import requests
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import os
class Tile:
    def __init__(self, image):
        self.image = image
        self.count = 1
    def get_image(self):
        self.count += 1
        return self.image
    
    def __repr__(self):
        return f"Tile(image_shape={self.image.shape})"
    


class Mapping:
    def __init__(self, cache, mCache_limit):
        self.cache = cache
        self.mCache_limit = mCache_limit
        self.memory_cache = {}

    def internal_cache_size(self):
        """Calcula o tamanho total do cache em bytes"""
        total = 0
        for tile in self.memory_cache.values():
            img = tile.image
            if isinstance(img, np.ndarray):
                total += img.nbytes
            else:  # PIL.Image
                total += img.width * img.height * 3  # 3 bytes por pixel (RGB)
        return total
    def cach_size(self):
        """Calcula o tamanho total do cache em bytes"""
        return sum(os.path.getsize(os.path.join(self.cache, f)) for f in os.listdir(self.cache) if os.path.isfile(os.path.join(self.cache, f)))
    def __repr__(self):
        return f"Mapping(cache={self.cache}, mCache_limit={self.mCache_limit})"
    def add(self, img, zoom, x, y):
        # Se estourar o limite, remove o menos usado
        while self.internal_cache_size() > self.mCache_limit and self.memory_cache:
            key_to_remove = min(self.memory_cache, key=lambda k: self.memory_cache[k].count)
            print(f"Removendo {key_to_remove} (uso: {self.memory_cache[key_to_remove].count})")
            del self.memory_cache[key_to_remove]
        
        self.memory_cache[f'cache_{zoom}_{x}_{y}'] = Tile(img)
    def download_tile(self, x, y, zoom):
        print("""Baixa um tile específico do OpenStreetMap""")
        url = f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
        headers = {
            'User-Agent': 'Python Mapping Script 1.0'  # OSM requer User-Agent
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Converte bytes para imagem PIL e depois para numpy array (RGB)
            img = Image.open(io.BytesIO(response.content)).convert('RGB')
            self.add(img,zoom,x,y)
            return np.array(img)
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar tile {x},{y}: {e}")
            # Retorna tile cinza (256x256) se der erro
            return np.full((256, 256, 3), 128, dtype=np.uint8)
    def get_tile(self, x, y, zoom):
        # if tile := self.memory_cache[f'cache_{zoom}_{x}_{y}'] is not None:
        if (tile := self.memory_cache.get(f'cache_{zoom}_{x}_{y}')) is not None:
            return tile.get_image()
        
        if os.path.exists(f"{self.cache}/{zoom}/{x}_{y}.png"):
            img = np.array(Image.open(f"{self.cache}/{zoom}/{x}_{y}.png"))
            self.add(img,zoom,x,y)
            return img 
        else:
            tile = self.download_tile(x, y, zoom)
            if not os.path.exists(f"{self.cache}/{zoom}"):
                os.makedirs(f"{self.cache}/{zoom}")
            Image.fromarray(tile).save(f"{self.cache}/{zoom}/{x}_{y}.png")
            return tile

if __name__ == '__main__':
    mapping = Mapping(cache='cache', mCache_limit=4000)
    
    # Exemplo: tile mais geral do mundo
    m = mapping.get_tile(x=10, y=20, zoom=19)
    
    plt.figure(figsize=(8, 8))
    plt.imshow(m)
    plt.axis('off')  # Remove eixos
    plt.title('Mapa do OpenStreetMap - Tile (0,0) Zoom 0')
    plt.tight_layout()
    plt.show()
    
    # print(f"Imagem baixada com sucesso! Dimensões: {m.shape}")
