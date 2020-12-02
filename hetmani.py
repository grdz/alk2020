import time
import os

# Funkcja do printowania
def printszachownica(rozwiazanie, first, krzyzyk):
  global n; rozmiar = n
  if dynamic:
    os.system('clear')
  for i in range(0, rozmiar):
    for j in range(0, rozmiar):
      if j < rozmiar-1:
        if (dynamic and j != ostatniakolumna[-1] and i != ostatniwiersz[-1]) or (dynamic and first) or rozwiazanie:
          print(szachownica[i][j]," ", end='')
        else:
          if krzyzyk and j == ostatniakolumna[-1] and i == ostatniwiersz[-1] and dynamic:
            print('X  ', end='')
          else:
            if dynamic:
              print(0," ", end='')
      else:
        if (dynamic and j != ostatniakolumna[-1] and i != ostatniwiersz[-1]) or (dynamic and first) or rozwiazanie:
          print(szachownica[i][j])
        else:
          if krzyzyk and j == ostatniakolumna[-1] and i == ostatniwiersz[-1] and dynamic:
            print('X  ')
          else:
            if dynamic:
              print(0)
  if rozwiazanie:
    print("-----------")
    if dynamic:
      print("Znaleziono rozwiązanie"); time.sleep(3)

# Funkcja właściwa, znajdująca rozwiązania metodą powrotów, rekurencyjnie
def hetman(rozmiar, wiersz):
  global ostatniwiersz; global ostatniakolumna

  if wiersz == rozmiar:  
    # Jesteśmy w ostatnim wierszu, więc mamy rozwiązanie i robimy jego print
    printszachownica(rozwiazanie=True, first=False, krzyzyk=False)
    printszachownica(rozwiazanie=False, first=False, krzyzyk=True)
    if dynamic:
      print("\nSzukam kolejnych rozwiazan - POWROT"); time.sleep(delay)
    ostatniakolumna.pop(); ostatniwiersz.pop()

    return
  else:
    printszachownica(rozwiazanie=False, first=True, krzyzyk=False)
  if dynamic:
    time.sleep(delay)      

  # Sprawdzamy każde pole (kolumna) w danym wierszu - czy można na nim postawić hetmana?
  for kolumna in range(0, rozmiar):
    # Na początku zakładamy, że można postawić w danym miejscu hetmana
    czy_mozliwe = True

    # Sprawdzamy w tym samym wierszu, na lewo od pola obecnego, czy nie ma kolizji z innym hetmanem postawionem wcześniej
    i = wiersz-1
    while i >= 0:
      if(szachownica[i][kolumna] == 1):
        # Jeśli kolizja znaleziona, to wycofujemy założenie że na tym polu można postawić hetmana
        czy_mozliwe = False
      i = i-1
    
    # Sprawdzamy po ukosie w lewo do góry
    i = wiersz-1; j = kolumna-1
    while i >= 0 and j >= 0:
      if szachownica[i][j] == 1:
        # tak samo, jeśli jest kolizja, uznajemy, że nie można tu postawić hetmana
        czy_mozliwe = False
      i = i-1
      j = j-1

    # Po ukosie w prawo do góry (bo hetman mógł być postawione we wcześniejszym, wyższym wierszu, ale w kolumnie bardziej na prawo)
    i = wiersz-1; j = kolumna+1
    while i >= 0 and j < n:
      if szachownica[i][j] == 1:
        czy_mozliwe = False
      i = i-1
      j = j+1

    if czy_mozliwe:
      # Jeśli można, to stawiamy tutaj hetmana i wywołujemy rekurencyjnie funkcję hetman,
      # by kontynuowała sprawdzanie obecnie badanego rozwiązania (przesuwamy się do następnego wiersza)
      szachownica[wiersz][kolumna] = 1
      ostatniwiersz.append(wiersz); ostatniakolumna.append(kolumna)
      hetman(rozmiar, wiersz+1)
    # jeśli wykryto kolizję, to hetmana nie stawiamy i wycofujemy się/backtrack (w linijce 103 jest "return" po printach)
    szachownica[wiersz][kolumna] = 0

  printszachownica(rozwiazanie=False, first=False, krzyzyk=True)
  if dynamic:
    print("\nSlepa uliczka - POWROT"); time.sleep(delay)
  printszachownica(rozwiazanie=False, first=False, krzyzyk=False); ostatniakolumna.pop(); ostatniwiersz.pop()
  if dynamic:
    time.sleep(delay)
  if wiersz == 0:
    print("\n--Nie znaleziono kolejnego rozwiązania. Koniec--")

  # Sprawdzilismy wszystkie pola w danym wierszu i nie postawilismy hetmana. Jest to ślepa uliczka
  # Nie sprawdzamy dalej tej gałęzi drzewa, wycofujemy się/backtrack
  # (lub znaleziono już rozwiązanie i wycofujemy się by szukać kolejnego)
  return

# Rozmiar szachownicy
n = 8

# dynamic ustawione na False oznacza wypisanie na ekran od razu wszystkich znalezionych rozwiązań
# dynamic ustawione na True pokazuje działanie algorytmu i szukanie rozwiązań
dynamic = True

# Przy dynamic = True określa przerwę między printowaniem kolejnych kroków algorytmu, w sekundach (np 0.1, 0.5, 1, 2)
delay = 0.1

# Pomocniczo, do outputu
ostatniwiersz = []; ostatniwiersz.append(-1)
ostatniakolumna = []; ostatniakolumna.append(-1)

# Dwuwymiarowa tablica, zainicjalizowana zerami
szachownica = [[0 for i in range(n)] for j in range(n)]

hetman(n, 0)
