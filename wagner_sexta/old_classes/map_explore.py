from pygame_plug import Escene, Configure
from street_plug import Mapping
import math
import pygame
import numpy as np
from PIL import Image
import threading
import time

# Inicialização dos componentes
mapping = Mapping(cache='cache', mCache_limit=4000)
confs = Configure(
    title="Mapa",
    icon='assets/Icon.svg'
)
escene = Escene(configure=confs)

class MapRenderer:
    def __init__(self, size=(800, 600)):
        self.size = size
        self.current_surface = None
        self.background_thread = None
        self.is_generating = False
        self.pending_update = None
        
        # Buffer para o mapa atual (para zoom suave)
        self.current_array = None
        self.current_lat = None
        self.current_lon = None
        self.current_zoom = None
        
        # Offset para arrastar suave
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
    def numpy_to_surface(self, np_array):
        """Converte numpy array para pygame Surface"""
        try:
            if len(np_array.shape) == 3:
                np_array = np.transpose(np_array, (1, 0, 2))
            surface = pygame.surfarray.make_surface(np_array)
            return surface
        except Exception as e:
            print(f"Erro ao converter numpy para Surface: {e}")
            surface = pygame.Surface(self.size)
            surface.fill((128, 128, 128))
            return surface

    def latlon_to_tile(self, lat, lon, zoom):
        """Converte coordenadas lat/lon para coordenadas de tile"""
        lat_rad = math.radians(lat)
        n = 2 ** zoom
        xtile = (lon + 180.0) / 360.0 * n
        ytile = (1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n
        return xtile, ytile

    def generate_map_background(self, lat, lon, zoom):
        """Gera mapa em thread separada"""
        try:
            print(f"Gerando mapa em background: lat={lat:.4f}, lon={lon:.4f}, zoom={zoom}")
            
            # Validação de parâmetros
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180) or not (0 <= zoom <= 18):
                return None
            
            # Tile inicial (centro do mapa)
            center_x, center_y = self.latlon_to_tile(lat, lon, zoom)
            tile_size = 256
            
            # Quantos tiles precisamos? (com margem extra para arrastar)
            tiles_x = math.ceil(self.size[0] / tile_size) + 3  # +3 para margem
            tiles_y = math.ceil(self.size[1] / tile_size) + 3
            
            # Coordenadas iniciais
            start_x = int(center_x - tiles_x // 2)
            start_y = int(center_y - tiles_y // 2)
            
            # Cria array numpy maior (com margem)
            map_array = np.full((tiles_y * tile_size, tiles_x * tile_size, 3), 200, dtype=np.uint8)
            
            # Download e colagem dos tiles
            for dx in range(tiles_x):
                for dy in range(tiles_y):
                    if not self.is_generating:  # Se cancelou, para
                        return None
                        
                    tile_x = start_x + dx
                    tile_y = start_y + dy
                    
                    max_tile = 2 ** zoom
                    if 0 <= tile_x < max_tile and 0 <= tile_y < max_tile:
                        try:
                            tile_array = mapping.get_tile(x=tile_x, y=tile_y, zoom=zoom)
                            
                            if tile_array is not None and tile_array.size > 0:
                                start_row = dy * tile_size
                                end_row = start_row + tile_size
                                start_col = dx * tile_size
                                end_col = start_col + tile_size
                                
                                if tile_array.shape[:2] == (256, 256):
                                    map_array[start_row:end_row, start_col:end_col] = tile_array
                        except Exception as e:
                            print(f"Erro ao carregar tile ({tile_x}, {tile_y}): {e}")
            
            return map_array
            
        except Exception as e:
            print(f"Erro ao gerar mapa: {e}")
            return None

    def crop_map(self, map_array, offset_x=0, offset_y=0):
        """Recorta o mapa com offset para arrastar"""
        if map_array is None:
            return np.full((self.size[1], self.size[0], 3), 128, dtype=np.uint8)
        
        map_height, map_width = map_array.shape[:2]
        
        # Calcula posição central com offset
        center_x = map_width // 2 + offset_x
        center_y = map_height // 2 + offset_y
        
        # Calcula área de recorte
        left = max(0, center_x - self.size[0] // 2)
        top = max(0, center_y - self.size[1] // 2)
        right = min(map_width, left + self.size[0])
        bottom = min(map_height, top + self.size[1])
        
        cropped = map_array[top:bottom, left:right]
        
        # Se menor que o esperado, preenche com cinza
        if cropped.shape[:2] != (self.size[1], self.size[0]):
            final_array = np.full((self.size[1], self.size[0], 3), 128, dtype=np.uint8)
            h, w = cropped.shape[:2]
            final_array[:h, :w] = cropped
            return final_array
        
        return cropped

    def zoom_surface_smooth(self, surface, zoom_factor, center_pos=None):
        """Aplica zoom suave na surface atual"""
        if surface is None:
            return None
        
        try:
            # Converte surface para array numpy
            w, h = surface.get_size()
            surface_array = pygame.surfarray.array3d(surface)
            surface_array = np.transpose(surface_array, (1, 0, 2))
            
            # Calcula novo tamanho
            new_w = int(w * zoom_factor)
            new_h = int(h * zoom_factor)
            
            # Usa PIL para redimensionar com boa qualidade
            pil_img = Image.fromarray(surface_array)
            pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            resized_array = np.array(pil_img)
            
            # Se aumentou, recorta do centro
            if zoom_factor > 1:
                start_x = (new_w - w) // 2
                start_y = (new_h - h) // 2
                cropped = resized_array[start_y:start_y+h, start_x:start_x+w]
            else:
                # Se diminuiu, centraliza na tela
                cropped = np.full((h, w, 3), 128, dtype=np.uint8)
                start_x = (w - new_w) // 2
                start_y = (h - new_h) // 2
                cropped[start_y:start_y+new_h, start_x:start_x+new_w] = resized_array
            
            return self.numpy_to_surface(cropped)
            
        except Exception as e:
            print(f"Erro no zoom suave: {e}")
            return surface

    def update_map_async(self, lat, lon, zoom):
        """Atualiza o mapa de forma assíncrona"""
        # Cancela thread anterior se existir
        if self.background_thread and self.background_thread.is_alive():
            self.is_generating = False
            self.background_thread.join(timeout=0.1)
        
        # Inicia nova geração
        self.is_generating = True
        self.pending_update = (lat, lon, zoom)
        
        def background_worker():
            try:
                new_array = self.generate_map_background(lat, lon, zoom)
                
                if self.is_generating and new_array is not None:
                    # Atualiza apenas se ainda é a mesma requisição
                    if self.pending_update == (lat, lon, zoom):
                        self.current_array = new_array
                        self.current_lat = lat
                        self.current_lon = lon
                        self.current_zoom = zoom
                        self.drag_offset_x = 0
                        self.drag_offset_y = 0
                        
                        # Atualiza a tela
                        cropped = self.crop_map(new_array)
                        self.current_surface = self.numpy_to_surface(cropped)
                        escene.frame = self.current_surface
                        
                        print(f"Mapa atualizado: {lat:.4f}, {lon:.4f}, zoom={zoom}")
                
            except Exception as e:
                print(f"Erro na thread de background: {e}")
            finally:
                self.is_generating = False
        
        self.background_thread = threading.Thread(target=background_worker)
        self.background_thread.daemon = True
        self.background_thread.start()

    def get_current_surface_with_offset(self):
        """Retorna a surface atual com offset aplicado"""
        if self.current_array is None:
            return self.current_surface
        
        try:
            cropped = self.crop_map(self.current_array, self.drag_offset_x, self.drag_offset_y)
            return self.numpy_to_surface(cropped)
        except:
            return self.current_surface

# Instância global do renderizador
renderer = MapRenderer()

# Variáveis globais para controle
lat = -23.5505  # São Paulo
lon = -46.6333  # São Paulo
zoom = 10
dragging = False
last_mouse_pos = None
drag_threshold = 50  # pixels - só regenera após arrastar muito

def pixels_to_latlon(dx, dy, zoom):
    """Converte movimento de pixels para mudança em lat/lon"""
    scale_factor = 0.001 * (2 ** (10 - zoom))
    # CORREÇÃO: inverter sinais para coordenadas geográficas corretas
    dlat = dy * scale_factor   # dy positivo = move pra baixo = lat menor
    dlon = -dx * scale_factor  # dx positivo = move pra direita = lon menor (no offset negativo)
    return dlat, dlon

def event_handler(event):
    """Manipula eventos do pygame - versão otimizada"""
    global zoom, lat, lon, dragging, last_mouse_pos
    
    # SCROLL DO MOUSE (ZOOM SUAVE)
    if event.type == pygame.MOUSEWHEEL:
        old_zoom = zoom
        zoom_factor = 1.0
        
        if event.y > 0:  # Zoom in
            zoom = min(zoom + 1, 18)
            zoom_factor = 2.0
        elif event.y < 0:  # Zoom out
            zoom = max(zoom - 1, 1)
            zoom_factor = 0.5
        
        if zoom != old_zoom:
            print(f"Zoom: {old_zoom} → {zoom}")
            
            # Aplica zoom suave IMEDIATAMENTE na surface atual
            if renderer.current_surface:
                zoomed_surface = renderer.zoom_surface_smooth(renderer.current_surface, zoom_factor)
                if zoomed_surface:
                    escene.frame = zoomed_surface
            
            # Gera nova versão em background
            renderer.update_map_async(lat, lon, zoom)
    
    # INÍCIO DO ARRASTAR
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            dragging = True
            last_mouse_pos = event.pos
            renderer.drag_offset_x = 0
            renderer.drag_offset_y = 0
    
    # FIM DO ARRASTAR
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            if dragging:
                # Se arrastou muito, atualiza coordenadas e regenera
                total_offset = abs(renderer.drag_offset_x) + abs(renderer.drag_offset_y)
                if total_offset > drag_threshold:
                    # CORREÇÃO: usar offset direto (já está na direção certa)
                    dlat, dlon = pixels_to_latlon(renderer.drag_offset_x, renderer.drag_offset_y, zoom)
                    lat += dlat
                    lon += dlon
                    
                    # Mantém limites
                    lat = max(-85, min(85, lat))
                    lon = (lon + 180) % 360 - 180
                    
                    print(f"Finalizando arrasto: nova pos lat={lat:.4f}, lon={lon:.4f}")
                    renderer.update_map_async(lat, lon, zoom)
                
            dragging = False
            last_mouse_pos = None
    
    # MOVIMENTO DO MOUSE (ARRASTAR SUAVE)
    elif event.type == pygame.MOUSEMOTION and dragging:
        if last_mouse_pos is not None:
            dx = event.pos[0] - last_mouse_pos[0]
            dy = event.pos[1] - last_mouse_pos[1]
            
            # INVERSÃO CORRIGIDA: arrastar pra direita = mover mapa pra esquerda
            renderer.drag_offset_x -= dx  # Invertido
            renderer.drag_offset_y -= dy  # Invertido
            
            # Atualiza surface com offset IMEDIATAMENTE
            offset_surface = renderer.get_current_surface_with_offset()
            if offset_surface:
                escene.frame = offset_surface
            
            last_mouse_pos = event.pos
    
    # TECLAS (navegação)
    elif event.type == pygame.KEYDOWN:
        step = 0.01 * (2 ** (10 - zoom))
        needs_update = False
        
        if event.key == pygame.K_UP:
            lat += step
            needs_update = True
        elif event.key == pygame.K_DOWN:
            lat -= step
            needs_update = True
        elif event.key == pygame.K_LEFT:
            lon -= step
            needs_update = True
        elif event.key == pygame.K_RIGHT:
            lon += step
            needs_update = True
        elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
            zoom = min(zoom + 1, 18)
            needs_update = True
        elif event.key == pygame.K_MINUS:
            zoom = max(zoom - 1, 1)
            needs_update = True
        
        if needs_update:
            lat = max(-85, min(85, lat))
            lon = (lon + 180) % 360 - 180
            print(f"Tecla: nova posição lat={lat:.4f}, lon={lon:.4f}, zoom={zoom}")
            renderer.update_map_async(lat, lon, zoom)

def main():
    """Função principal otimizada"""
    global lat, lon, zoom
    
    try:
        # Garante inicialização do pygame
        try:
            pygame.init()
            pygame.font.init()
        except:
            pass  # Pode já estar inicializado pelo pygame_plug
        
        print("Iniciando visualizador de mapa otimizado...")
        print("Controles:")
        print("- Scroll: zoom")
        print("- Arrastar: mover mapa")
        print("- Setas: navegação")
        print("- +/-: zoom")
        
        # Gera mapa inicial
        print(f"Carregando mapa inicial: {lat:.4f}, {lon:.4f}, zoom={zoom}")
        
        # Surface temporária enquanto carrega
        temp_surface = pygame.Surface(renderer.size)
        temp_surface.fill((64, 64, 64))
        
        # Tenta adicionar texto de loading
        try:
            if pygame.font.get_init():
                font = pygame.font.Font(None, 36)
                text = font.render("Carregando mapa...", True, (255, 255, 255))
                text_rect = text.get_rect(center=(renderer.size[0]//2, renderer.size[1]//2))
                temp_surface.blit(text, text_rect)
            else:
                print("Font não disponível, usando tela simples")
        except Exception as font_error:
            print(f"Erro com font: {font_error}")
            # Surface simples sem texto
            pass
            
        escene.frame = temp_surface
        
        # Define manipulador de eventos
        escene.handle_event = event_handler
        
        # Inicia geração do mapa inicial
        renderer.update_map_async(lat, lon, zoom)
        
        # Inicia aplicação
        print("Aplicação iniciada!")
        escene.run()
        
    except Exception as e:
        print(f"Erro crítico: {e}")

if __name__ == "__main__":
    main()