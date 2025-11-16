import pygame
import os

# --- 1. Inicialização e Configurações da Tela ---
pygame.init()

LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Meu Mega Man Clássico")

# Cor de fundo
PRETO = (0, 0, 0)
# Cor Rosa (Magenta) para transparência (o fundo do sprite sheet)
MAGENTA = (255, 0, 255)

# Controle de FPS (Frames Por Segundo)
clock = pygame.time.Clock()
FPS = 60

# --- FUNÇÃO DE RECORTE DE SPRITES (Sprite Sheet Loader) ---
def get_sprite_frames(sheet_path, frames_coords, escala, cor_transparente):
    """
    Carrega frames de animação de uma única sprite sheet.
    """
    if not os.path.exists(sheet_path):
        print(f"ERRO: Arquivo da sprite sheet não encontrado em: {sheet_path}")
        return []

    # O carregamento só acontece se o arquivo for encontrado!
    sprite_sheet = pygame.image.load(sheet_path) 
    
    lista_frames = []

    for x, y, w, h in frames_coords:
        # Cria uma nova Surface com o tamanho exato do frame
        frame_surface = pygame.Surface((w, h)) 
        
        # Copia a área (x, y, w, h) da sprite sheet para o novo surface
        frame_surface.blit(sprite_sheet, (0, 0), (x, y, w, h))

        # Define a cor transparente (MAGENTA) no frame recortado
        frame_surface.set_colorkey(cor_transparente)
        
        # Converte para garantir a transparência
        frame_surface = frame_surface.convert_alpha() 

        # --- Bloco de Escala ---
        nova_largura = int(w * escala)
        nova_altura = int(h * escala)
        imagem_escalada = pygame.transform.scale(frame_surface, (nova_largura, nova_altura))
        
        lista_frames.append(imagem_escalada)

    return lista_frames

# --- 2. Classe do Jogador (Mega Man Clássico) ---
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        """ Método construtor - chamado uma vez quando o Jogador é criado. """
        super().__init__()
        
        # ### CONTROLE DE TAMANHO ###
        self.escala = 3.0 
        self.sprite_tamanho = 32 
        
        # 🟢 CORREÇÃO CRÍTICA FINAL: Ajusta o caminho para a subpasta
        # Usa os.path.join para compatibilidade entre sistemas operacionais
        SHEET_PATH = os.path.join("atividade008", "spritenova.jpg") 

        # --- Definição das Coordenadas dos Sprites ---
        frames_parado = [
            (0, 0, 32, 32), (32, 0, 32, 32), (64, 0, 32, 32)
        ]
        
        frames_correndo = [
            (0, 32, 32, 32), (32, 32, 32, 32), (64, 32, 32, 32), (96, 32, 32, 32),
            (128, 32, 32, 32), (160, 32, 32, 32), (192, 32, 32, 32)
        ]
        
        frames_pulando = [
            (32, 64, 32, 32) 
        ]
        
        frames_atirando_parado = [
            (0, 96, 32, 32), (32, 96, 32, 32), (64, 96, 32, 32)
        ]
        
        frames_atirando_correndo = [
            (0, 128, 32, 32), (32, 128, 32, 32), (64, 128, 32, 32), (96, 128, 32, 32),
            (128, 128, 32, 32), (160, 128, 32, 32), (192, 128, 32, 32)
        ]

        frames_atirando_pulando = [
            (128, 64, 32, 32) 
        ]

        # --- Carregamento e Escala dos Sprites ---
        self.anim_parado = get_sprite_frames(SHEET_PATH, frames_parado, self.escala, MAGENTA)
        self.anim_correndo = get_sprite_frames(SHEET_PATH, frames_correndo, self.escala, MAGENTA)
        self.anim_pulando = get_sprite_frames(SHEET_PATH, frames_pulando, self.escala, MAGENTA)
        self.anim_atirando_parado = get_sprite_frames(SHEET_PATH, frames_atirando_parado, self.escala, MAGENTA)
        self.anim_atirando_correndo = get_sprite_frames(SHEET_PATH, frames_atirando_correndo, self.escala, MAGENTA)
        self.anim_atirando_pulando = get_sprite_frames(SHEET_PATH, frames_atirando_pulando, self.escala, MAGENTA)
        
        self.anim_atirando = self.anim_atirando_parado

        # --- TRATAMENTO DE ERRO (Mantido para segurança) ---
        if not self.anim_parado:
             raise FileNotFoundError(f"O arquivo {SHEET_PATH} não foi encontrado ou carregado.")

        # --- Variáveis de Estado e Animação ---
        self.frame_atual = 0 
        self.image = self.anim_parado[self.frame_atual]
        self.rect = self.image.get_rect() 
        
        # --- Posição e Física ---
        self.rect.x = 100 
        self.rect.y = 400 
        self.vel_x = 0 
        self.vel_y = 0 
        self.gravidade = 0.8 
        self.forca_pulo = -15 
        self.velocidade_mov = 5 
        
        # --- Flags (Bandeiras) de Estado ---
        self.pulando = True 
        self.correndo = False
        self.atirando = False
        self.olhando_direita = True 
        
        # --- Controle de Tempo da Animação ---
        self.ultimo_update = pygame.time.get_ticks()
        self.velocidade_anim = 90 

    def update(self):
        """ Atualiza a lógica do jogador a cada frame. """
        
        # --- 1. Física e Gravidade ---
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y
        
        # --- 2. Simulação do "Chão" ---
        chao = 500 
        if self.rect.bottom > chao:
            self.rect.bottom = chao
            self.vel_y = 0
            self.pulando = False

        # --- 3. Movimento Horizontal ---
        self.rect.x += self.vel_x
        
        # --- 4. Seleção de Animação (Máquina de Estado) ---
        estado_anim = self.anim_parado
        
        if self.pulando:
            if self.atirando:
                estado_anim = self.anim_atirando_pulando
            else:
                estado_anim = self.anim_pulando
        
        elif self.atirando:
            if self.correndo:
                estado_anim = self.anim_atirando_correndo
            else:
                estado_anim = self.anim_atirando_parado
                
        elif self.correndo:
            estado_anim = self.anim_correndo
            
        else:
            estado_anim = self.anim_parado
            
        # --- 5. Chamar a função de Animar ---
        self.animar(estado_anim)

    def animar(self, lista_animacao):
        """ Controla a troca de frames (imagens). """
        if not lista_animacao:
             return 

        agora = pygame.time.get_ticks()
        
        if len(lista_animacao) == 1:
            self.frame_atual = 0
        elif agora - self.ultimo_update > self.velocidade_anim:
            self.ultimo_update = agora
            
            self.frame_atual = (self.frame_atual + 1) % len(lista_animacao)
            
        # Pega a nova imagem da lista de animação
        imagem_nova = lista_animacao[self.frame_atual]
        
        # Preserva o centro do personagem
        centro_antigo = self.rect.center
        
        # Vira a imagem (flip) se estiver olhando para a esquerda
        if not self.olhando_direita:
            imagem_nova = pygame.transform.flip(imagem_nova, True, False) 
            
        # Define a nova imagem e atualiza o retângulo
        self.image = imagem_nova
        self.rect = self.image.get_rect()
        
        # Restaura a posição do centro
        self.rect.center = centro_antigo
            
    def pular(self):
        """ Executa a ação de pular. """
        if not self.pulando:
            self.vel_y = self.forca_pulo
            self.pulando = True
            self.frame_atual = 0 

# --- 3. Criação dos Objetos (Antes do Loop) ---
try:
    jogador = Jogador() 
except FileNotFoundError as e:
    print(f"\nERRO FATAL: {e}")
    pygame.quit()
    # Adicione uma pausa ou input para que a mensagem de erro seja vista
    input("Pressione Enter para sair...")
    exit()

# --- 4. Loop Principal do Jogo ---
rodando = True
while rodando:
    # Garante que o jogo rode no máximo a 60 FPS
    clock.tick(FPS) 

    # --- 4a. Processamento de Eventos (Inputs) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        # Evento: TECLA PRESSIONADA (apenas uma vez)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE: 
                jogador.pular()
            if evento.key == pygame.K_z: 
                jogador.atirando = True
                jogador.frame_atual = 0 
                
        # Evento: TECLA SOLTA
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_z:
                jogador.atirando = False 

    # --- 4b. Checagem de Teclas (para movimento contínuo) ---
    teclas = pygame.key.get_pressed()
    
    jogador.vel_x = 0
    jogador.correndo = False

    if teclas[pygame.K_LEFT]: 
        jogador.vel_x = -jogador.velocidade_mov
        jogador.correndo = True
        jogador.olhando_direita = False 
    elif teclas[pygame.K_RIGHT]: 
        jogador.vel_x = jogador.velocidade_mov
        jogador.correndo = True
        jogador.olhando_direita = True 
    
    # --- 4c. Atualização da Lógica ---
    jogador.update() 

    # --- 4d. Renderização (Desenho) ---
    
    # 1. Limpa a tela
    tela.fill(PRETO)
    
    # 2. Desenha o jogador na tela
    tela.blit(jogador.image, jogador.rect)
    
    # 3. Atualiza a tela para mostrar o que foi desenhado
    pygame.display.flip()

# --- 5. Finalização ---
pygame.quit()