import re
import copy

# Funkcja do ladnego printowania planszy
def print_plansza():
  for i in range(0, n):
    for j in range(0, n):
      if j == n-1:
        if plansza[i][j] == 'X':
          print('🟩')
        elif plansza[i][j] == 'B':
          print('⬛')
        elif plansza[i][j] == 'W': 
          print('⬜')
        else:
          print(plansza[i][j])
      else:
        if plansza[i][j] == 'X':
          print('🟩', end='')
        elif plansza[i][j] == 'B':
          print('⬛', end='')
        elif plansza[i][j] == 'W': 
          print('⬜', end='')
        else:
          print(plansza[i][j], end='')
  print('==============')

# Funkcja sprawdzajaca czy wszystkie domkniete wyspy sa prawidlowe (jeszcze niedomkniete pomija)
def weryfikuj_wyspy(x, y):
  global checked
  global rozmiar_wyspy
  global liczby_wyspy
  global error

  if x < n and y < n and x >= 0 and y >= 0 and checked[x][y] == False:
    checked[x][y] = True
    if plansza[x][y] == 'W' or re.compile("^ [0-9]$").match(plansza[x][y]):
      rozmiar_wyspy = rozmiar_wyspy+1

      if re.compile("^ [0-9]$").match(plansza[x][y]):
        liczby_wyspy.append(plansza[x][y])

      weryfikuj_wyspy(x, y - 1) # Lewo
      weryfikuj_wyspy(x, y + 1) # Prawo
      weryfikuj_wyspy(x - 1, y) # Góra
      weryfikuj_wyspy(x + 1, y) # Dół

      if error: # Ktorys z podprogramow wykryl niedomkniecie wyspy
        rozmiar_wyspy = 0
        liczby_wyspy = []
        return
    elif plansza[x][y] == 'X':
      error = True # Nie jest to jeszcze domknieta wyspa
      return
    else:
      return # Granica wyspy, czarne pole
    #else:
    #  return # Pole juz sprawdzane było
  else:
    return # Index out of range albo pole juz sprawdzane było

  if len(liczby_wyspy) == 1:
    if rozmiar_wyspy == int(liczby_wyspy[0].strip()):
      return 'dobra_wyspa'
    else:
      return 'zla_wyspa' # Zly rozmiar wyspy
  else:
    return 'zla_wyspa' # Zla ilosc cyfr w wyspie (0 albo wiecej niż 1)

# Funkcja sprawdzajaca czy nie ma w jeziorze kwadratow 2x2 albo wiekszych prostokatow
def weryfikuj_jezioro(x, y):
  if x+1 < n and y+1 < n:
    if plansza[x][y] == 'B':
      if plansza[x][y+1] == 'B':
        if plansza[x+1][y] == 'B':
          if plansza[x+1][y+1] == 'B':
            return 'zle_jezioro'
  return 'ok_jezioro'

# Funkcja pomagajaca sprawdzac czy istnieje tylko jedno ciagle jezioro
def weryfikuj_ciaglosc_jeziora_v2(x, y):
  global checked_jezioro
  global rozmiar_jeziora

  if x < n and y < n and x >= 0 and y >= 0 and checked_jezioro[x][y] == False:
    checked_jezioro[x][y] = True
    if plansza[x][y] == 'B':
      rozmiar_jeziora = rozmiar_jeziora+1

      weryfikuj_ciaglosc_jeziora_v2(x, y - 1) # Lewo
      weryfikuj_ciaglosc_jeziora_v2(x, y + 1) # Prawo
      weryfikuj_ciaglosc_jeziora_v2(x - 1, y) # Góra
      weryfikuj_ciaglosc_jeziora_v2(x + 1, y) # Dół

    else:
      return # Granica jeziora
  else:
    return # Index out of range albo pole juz sprawdzane było

  return rozmiar_jeziora

# Funkcja glowna
def nurikabe(x , y, kolor):
  # brzydkie rozwiazanie, mozna by uporzadkowac zmienne
  global checked, checked_jezioro, rozmiar_wyspy, liczby_wyspy, error, rozwiazania, rozmiar_jeziora
  # print_plansza()

  # Jesli jest to pierwsze wywolanie funkcji, korzen drzewa, uruchamiamy dwie galezie (1 i 0 czyli [B]lack i [W]hite)
  if kolor == '0':
    nurikabe(x, y, 'B')
    nurikabe(x, y, 'W')
  elif not re.compile("^ [0-9]$").match(plansza[x][y]):
    plansza[x][y] = kolor

  # Przyjmujemy na poczatku ze plansza jest poprawna - jesli ktorys z testow uzna, ze nie poprawna
  # to anulujemy to zalozenie
  is_plansza_poprawna = True

  # Weryfikowanie wysp - uruchamiane dla kazdego bialego pola i kazdego z cyfra
  for i in range(0, n):
    for j in range(0, n):
      if re.compile("^ [0-9]$").match(plansza[i][j]) or plansza[i][j] == 'W':
        checked = [[False for i in range(n)] for j in range(n)]
        rozmiar_wyspy = 0
        liczby_wyspy = []
        error = False
        return_code1 = weryfikuj_wyspy(i, j)
        if return_code1 == 'zla_wyspa':
          is_plansza_poprawna = False
  
  # Szukamy kwadratow 2x2 w jeziorze
  ile_czarnych = 0
  for i in range(0, n):
    for j in range(0, n):
      if plansza[i][j] == 'B':
        ile_czarnych = ile_czarnych + 1
        return_code2 = weryfikuj_jezioro(i, j)
        if return_code2 == 'zle_jezioro':
          is_plansza_poprawna = False
  if ile_czarnych == 0 and y == n-1 and x == n-1:
    is_plansza_poprawna = False
  
  # Sprawdzamy czy jezioro jest w jednej calosci, czy nie ma kilku jezior niepolaczonych
  rozmiar_wysp_lacznie = 0
  rozmiar_jeziora = 0
  rozmiar_planszy = n*n
  if is_plansza_poprawna and y == n-1 and x == n-1:
    if plansza not in rozwiazania:
      for i in range(0, n):
        for j in range(0, n):
          if re.compile("^ [0-9]$").match(plansza[i][j]):
            rozmiar_wysp_lacznie = rozmiar_wysp_lacznie + int(plansza[i][j].strip())
      for i in range(0, n):
        for j in range(0, n):
          if plansza[i][j] == 'B':
            checked_jezioro = [[False for i in range(n)] for j in range(n)]
            rozmiar_jeziora = weryfikuj_ciaglosc_jeziora_v2(i, j)
            break
        else:
          continue
        break
      if rozmiar_jeziora != rozmiar_planszy - rozmiar_wysp_lacznie:
        is_plansza_poprawna = False

  # Wszystkie testy przeszly wiec podazamy dalej ta galezia drzewa
  # lub drukujemy juz rozwiazanie jesli jestesmy na koncu planszy
  if is_plansza_poprawna:
    if y == n-1 and x < n-1:
      nurikabe(x+1, 0, 'B')
      nurikabe(x+1, 0, 'W')
    elif y == n-1 and x == n-1:
      if plansza not in rozwiazania:
        print("ROZWIAZANIE")
        print_plansza()
        print("==============")
        rozwiazania.append(copy.deepcopy(plansza))
      # Backtrack/powrot
      if not re.compile("^ [0-9]$").match(plansza[x][y]):
        plansza[x][y] = 'X'
      return
    else:
      nurikabe(x, y+1, 'B')
      nurikabe(x, y+1, 'W')
  else:
    # Backtrack/powrot
    if not re.compile("^ [0-9]$").match(plansza[x][y]):
      plansza[x][y] = 'X'
    return

n = 2
plansza = [['X' for i in range(n)] for j in range(n)]
rozwiazania = []

# przykladowe 2x2
plansza[0][0] = ' 2'

# przykladowe 3x3
#plansza[1][0]=' 2'

# przykladowe 4x4
#plansza[0][3]=' 4'
#plansza[3][3]=' 1'
#plansza[3][0]=' 3'

# inne 4x4
#plansza[0][3]=' 1'
#plansza[1][1]=' 3'
#plansza[3][0]=' 1'

# kolejne 4x4
#plansza[0][0]=' 1'
#plansza[2][0]=' 2'
#plansza[1][3]=' 3'
#plansza[3][3]=' 2'

# przykladowe 5x5 z PDFa
#plansza[0][1]=' 1'
#plansza[0][3]=' 1'
#plansza[2][0]=' 3'
#plansza[2][4]=' 3'
#plansza[4][0]=' 3'

# inne 5x5 'easy'
#plansza[0][3]=' 1'
#plansza[2][1]=' 2'
#plansza[3][0]=' 4'
#plansza[3][3]=' 2'

# 5x5 'hard'
#plansza[1][3]=' 1'
#plansza[2][1]=' 3'
#plansza[3][0]=' 2'
#plansza[3][4]=' 4'

# przykladowe 6x6 - juz za duze
#plansza[1][1]=' 1'
#plansza[2][0]=' 5'
#plansza[2][2]=' 3'
#plansza[4][2]=' 2'
#plansza[4][5]=' 6'

print("Poczatkowa plansza:")
print_plansza()

nurikabe(0, 0, '0')
