import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # oyun ekranı ayarları

pygame.display.set_caption("Snake-Game")

clock = pygame.time.Clock()
# clock değişkenini oyunun fps'ini ayarlamak için kullanacağız

# oyunda kullanılacak renkler
orange = (255, 127, 0)
black = (0, 0, 0)
white = (255, 255, 255) # menüde kullanmak için

# snake
snake_size = 20  # 20 piksellik bir boy
snake_speed = 10  # yılanın hızı aynı zamanda fps değerimiz olacak
snake_x = WIDTH / 2  # ekranın ortasında yılanın x koordinatı
snake_y = HEIGHT / 2
# yılanı aşağıda pygame.draw.rect() kısmında çizdirelim

# aşağıda oluşturduğumuz iki değişken yılanın program başındaki hızı
snake_x_speed = 0
snake_y_speed = 0

# yılan kuyruğu:
snake_list = []  # program başında boş bir liste
snake_len = 1  # yılanın parçalarının sayısı yani uzunluğu

# ---------- Yılanın yiyebileceği yemler ----------
# 0 ile width - snake_size aralığında bir konum olsun ve bu değer snake_size katlarında olsun
# bu da yemi ara değerlere göndermekten ziyade yılanın gideceği güzergah üzerine oturmasını sağlar
cookie_x = random.randrange(0, WIDTH - snake_size, snake_size)
cookie_y = random.randrange(0, HEIGHT - snake_size, snake_size)
# yemi aşağıda pygame.draw.rect(screen)... kısmında çizdirelim

# Skor kısmı
skor = 0
font = pygame.font.Font(None, 35)  # yazı fontu: none, büyüklük 35
# aşağıda skor_text kısmında yazdıralım

# Ses efekti
eat_stx = pygame.mixer.Sound("C:/Users/Victus/Desktop/PyGame/snake-game/munch-sound-effect.mp3")

# Oyun Döngüsü ---
def game_loop():
    global snake_x, snake_y, snake_x_speed, snake_y_speed, snake_list, snake_len, cookie_x, cookie_y, skor

    snake_x = WIDTH / 2
    snake_y = HEIGHT / 2
    snake_x_speed = 0
    snake_y_speed = 0
    snake_list = []
    snake_len = 1
    cookie_x = random.randrange(0, WIDTH - snake_size, snake_size)
    cookie_y = random.randrange(0, HEIGHT - snake_size, snake_size)
    skor = 0

    game = True
    while game:  # oyun değişkeni true olduğu sürece
        screen.fill(black)  # pencereyi siyah renk yaptık

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # kullanıcı pencereyi kapatmaya çalışıyorsa
                pygame.quit()
                return

            # yılanın kontrollerini sağladığımız kısım:
            if event.type == pygame.KEYDOWN:  # eğer herhangi bir tuşa basılıyorsa

                if event.key == pygame.K_LEFT and snake_x_speed == 0:  # sol ok tuşuna basılıyorsa
                    snake_x_speed -= snake_size  # yılanın x koordinatını yılan boyu kadar azalt
                    snake_y_speed = 0  # y ekseninde hareket etmesin

                if event.key == pygame.K_RIGHT and snake_x_speed == 0:
                    snake_x_speed += snake_size
                    snake_y_speed = 0

                if event.key == pygame.K_UP and snake_y_speed == 0:
                    snake_x_speed = 0
                    snake_y_speed -= snake_size

                if event.key == pygame.K_DOWN and snake_y_speed == 0:
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

        # -------------- Etkileşimler -------------
        # ----- Yem yemek -----
        if snake_x == cookie_x and snake_y == cookie_y:  # yılan yeme temas etmiş
            cookie_x = random.randrange(0, WIDTH - snake_size, snake_size)
            cookie_y = random.randrange(0, HEIGHT - snake_size, snake_size)
            snake_len += 1
            skor += 1
            eat_stx.play()

        skor_text = font.render("Point: {}".format(skor), True, orange)
        # {} yerine format ile skor'u gönderiyoruz
        # True ile yazının kenarlarını biraz yumuşatıyoruz
        # yazı rengi orange
        # aşağıda "screen.blit()" ile ekrana yazdıralım

        # Yılanın ekran dışına çıkamaması için:
        if snake_x >= WIDTH or snake_x <= 0 or snake_y >= HEIGHT or snake_y <= 0:
            game = False  # Oyunu durdur

        for i in snake_list:
            pygame.draw.rect(screen, orange, [i[0], i[1], snake_size, snake_size])

        screen.blit(skor_text, (15, 15))

        pygame.draw.rect(screen, orange, [cookie_x, cookie_y, snake_size, snake_size])  # yemi çizdirelim

        pygame.display.update()  # oyun döngüsü içinde pencereyi güncellemek için
        clock.tick(snake_speed)  # oyunun fps'ini burada ayarlıyoruz

    return  # Game loop ends, return to menu

def show_menu():
    menu = True
    while menu:
        screen.fill(black)
        title_text = font.render("Snake Game", True, orange)
        play_text = font.render("Play", True, white)
        options_text = font.render("Options", True, white)
        quit_text = font.render("Quit", True, white)

        play_rect = play_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        options_rect = options_text.get_rect(center=(WIDTH / 2, HEIGHT / 1.5))
        quit_rect = quit_text.get_rect(center=(WIDTH / 2, HEIGHT / 1.2))

        screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 4))
        screen.blit(play_text, play_rect)
        screen.blit(options_text, options_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Oyundan çık
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Enter'a basılırsa oyunu başlat
                    return True  
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False  # ESC'ye basılırsa oyundan çık
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return True  # Oyunu başlat
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    return False  # Oyundan çık

    return False

def main():
    while True:
        if not show_menu():
            break
        game_loop()

if __name__ == "__main__":
    main()
