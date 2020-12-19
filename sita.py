# Funkcja ta zaznacza wizualnie liczbe ktora jest obecnie sprawdzana sitem.
# Robi to umieszczajac ja pomiedzy ostrymi nawiasami '< >'
def print_ciag(ciag, n):
  print("[", end='')
  for i in range(0, len(ciag)):
    if i != n:
      print(str(ciag[i]), end='')
    else:
      print("<" + str(ciag[i]) + ">", end='')
    if i < len(ciag)-1:
      print(", ", end='')
  print("]")

def sito_brak_pary(ciag, n):
  # n jest liczone od 0
  print_ciag(ciag, n); print("Sito 'czy para istnieje' dla n =",n , end=' | ')
  para=False
  for i in range(n):
    for j in range(i+1, n):
      if ciag[i] + ciag[j] == ciag[n]:
        para=True
  if not para:
    print("Brak pary. Usuwam element o indeksie " + str(n) + " (liczba " + str(ciag[n]) +")\n")
    del ciag[n]
    return True
  print("Ok\n")

def sito_wiele_par(ciag, n):
  # n jest liczone od 0
  print_ciag(ciag, n); print("Sito 'czy za dużo par' dla n =",n , end=' | ')
  para=0
  for i in range(n):
    for j in range(i+1, n):
      if ciag[i] + ciag[j] == ciag[n]:
        para = para + 1
  if para > 1:
    print("Za dużo par. Usuwam element o indeksie " + str(n) + " (liczba " + str(ciag[n]) +")\n")
    del ciag[n]
    return True
  print("Ok\n")

# Generujemy ciag poczatkowy, im dluzszy tym dluzszy ciag liczb Ulama uzyskamy
ciag = list(range(1, 40))

# Dla kazdej pozycji w ciagu uruchamiamy obydwa sita
i = 2
while i < len(ciag):
  if (sito_brak_pary(ciag, i)) and i > 2:
    # Jesli sito wyeliminowalo jakis element to cofamy sie o jedno miejsce
    # by uniknac "pominietych" elementow ktore nie zostana sprawdzone przez jedno z sit
    i = i-1
  if (sito_wiele_par(ciag, i)) and i > 2:
    i = i-1
  i = i+1

print("--- Wynik, liczby Ulama ---\n" + str(ciag))