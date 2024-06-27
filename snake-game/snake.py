import pygame
import random


pygame.init()

WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # oyun ekranı ayarları

pygame.display.set_caption("Snake-Game")

clock = pygame.time.Clock()
# clock değişkenini oyunun fps'ini ayarlamak için kullanacağız


# oyunda kullanılacak renkler
orange = (255,127,0)
black = (0,0,0)


# snake
snake_size = 20 # 20 piksellik bir boy
snake_speed = 10 # yılanın hızı aynı zamanda fps değerimiz olacak
snake_x = WIDTH/2 # ekranın ortasında yılanın x koordinatı
snake_y = HEIGHT/2
# yılanı aşağıda pygame.draw.rect() kısmında çizdirelim

# aşağıda oluşturduğumuz iki değişken yılanın program başındaki hızı
snake_x_speed = 0
snake_y_speed = 0


# yılan kuyruğu:
snake_list = [] # program başında boş bir liste
snake_len = 1 # yılanın parçalarının sayısı yani uzunluğu




# ---------- Yılanın yiyebileceği yemler ----------
# 0 ile width - snake_size aralığında bir konum olsun ve bu değer snake_size katlarında olsun
# bu da yemi ara değerlere göndermekten ziyade yılanın gideceği güzergah üzerine oturmasını sağlar
cookie_x = random.randrange(0, WIDTH-snake_size, snake_size)
cookie_y = random.randrange(0, HEIGHT-snake_size, snake_size)
# yemi aşağıda pygame.draw.rect(screen)... kısmında çizdirelim




# Skor kısmı
skor = 0
font = pygame.font.Font(None, 35) # yazı fontu: none, büyüklük 35 
# aşağıda skor_text kısmında yazdıralım


# Ses efekti
eat_stx = pygame.mixer.Sound("C:/Users/Victus/Desktop/PyGame/snake-game/munch-sound-effect.mp3")


# Oyun Döngüsü ---
game = True # oyunun çalışıp çalışmadığını temsil edecek olan değişken

while game: # oyun değişkeni true olduğu sürece
    screen.fill(black) # pencereyi siyah renk yaptık
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # kullanıcı pencereyi kapatmaya çalışıyorsa
            game = False

        # yılanın kontrollerini sağladığımız kısım:
        if event.type == pygame.KEYDOWN: # eğer herhangi bir tuşa basılıyorsa

            if event.key == pygame.K_LEFT: # sol ok tuşuna basılıyorsa
                snake_x_speed -= snake_size # yılanın x koordinatını yılan boyu kadar azalt
                snake_y_speed = 0 # y ekseninde hareket etmesin

            if event.key == pygame.K_RIGHT:
                snake_x_speed += snake_size
                snake_y_speed = 0

            if event.key == pygame.K_UP:
                snake_x_speed = 0
                snake_y_speed -= snake_size
            
            if event.key == pygame.K_DOWN:
                snake_x_speed = 0
                snake_y_speed += snake_size
    
    # Yılan hareket - her seferinde yılanın konumunu yukarıdan gelen verilerle güncelle
    snake_x += snake_x_speed
    snake_y += snake_y_speed

    # yılanın x ve y koordinatları her değiştiğinde listeye ekliyoruz
    snake_list.append((snake_x, snake_y)) 

    # yani listede bu yılanın uzunluğuna dahil olmayan bir değer varsa silelim
    if len(snake_list) > snake_len:
        del snake_list[0]


    #-------------- Etkileşimler -------------
    # ----- Yem yemek -----
    if snake_x == cookie_x and snake_y == cookie_y: # yılan yeme temas etmiş
        cookie_x = random.randrange(0, WIDTH - snake_size, snake_size)
        cookie_y = random.randrange(0, HEIGHT - snake_size, snake_size)
        snake_len += 1
        skor += 1
        eat_stx.play()

    skor_text = font.render("Point: {}", format(skor), True, orange)
    # {} yerine format ile skor'u gönderiyoruz 
    # True ile yazının kenarlarını biraz yumuşatıyoruz
    # yazı rengi orange
    # aşağıda "screen.blit()" ile ekrana yazdıralım 


    # Yılanın ekran dışına çıkamaması için:
    if snake_x >= WIDTH or snake_x <= 0 or snake_y >= HEIGHT or snake_y <= 0:
        game = False # Oyunu durdur



    for i in snake_list:    
        # pygame.draw.rect(screen, orange, [snake_x, snake_y, snake_size, snake_size])
        # üstteki kod satırını for içine aldık ve ufak bir güncelleme yapalım

        pygame.draw.rect(screen, orange, [i[0], i[1], snake_size, snake_size])
        # yılanın x ve y konumunu i'nin 0 ve 1. yani snake_list içindeki değerlerden çektik

    screen.blit(skor_text, (15,15))

    pygame.draw.rect(screen, orange, [cookie_x, cookie_y, snake_size, snake_size]) # yemi çizdirelim
    # screen üzerinde
    # rengi orange olan
    # (x'i snake_x), (y'si snake_y) ve kare büyüklüğü (snake_size) olan bir kare çiz
    # snake_size iki kenarı da temsil ettiği için yani 20x20 olmasını istediğimiz için 2 kez yazdık





    pygame.display.update() # oyun döngüsü içinde pencereyi güncellemek için
    clock.tick(snake_speed) # oyunun fps'ini burada ayarlıyoruz



pygame.quit() # oyun çalışma döngüsünden çıktığında kapatıyoruz
