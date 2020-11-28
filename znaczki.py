#!/usr/bin/env python3
# gdzieminski / 225112

# "x" to ilość różnych znaczków które rozpatrujemy i jednocześnie "głębokość" drzewa przez które przechodzi algorytm
def powrot(x, y):
  # Potrzebne by program korzystał ze zmiennej zdefiniowanej poza tą funkcją, a nie uważał jej za zmienną lokalną dla tej funkcji
  global maximum_postage

  # Pierwszy znaczek jest o wartości 1 i może posłużyć do stworzenia listów o wartości 1..m (bo m*1)
  # drugi znaczek musi być o wartości od 2 (bo znaczek o wartości 1 już mamy) do m+1, bo gdyby był m+2 to nie mógłby być wykorzystany
  # stworzenia listu o takiej cenie która zapewniałaby ciągłość (bo znaczek o wartości m+2 dodany do m znaczków o wartości 1 skutkowałby
  # ceną większą o 2 od poprzedniej, byłaby "luka")
  # Trzeci znaczek musi być conajmniej o wartości takiej jaką mogą osiągnąć wspólnie poprzednie dwa znaczki.
  for i in range(0, (current_solution[x-1]*m)+1): # "+1" są dodane czasem na końcu dlatego, że funkcja range() w Pythonie nie zwraca zakresu włącznie z ostatnim elementem, tylko do przedostatniego
    # Możemy mieć maksymalnie tyle znaczków ile jest miejsc na kopercie (czyli "m")
    if number_of_stamps_for_value[i] < m:
      for j in range(1,(m-number_of_stamps_for_value[i])+1):
        # Upewnianie się, że w tablicy posiadamy najmniejszą możliwą ilość znaczków do osiągnięcia danej ceny listu
        # jeśli jest możliwa kombinacja z mniejszą ilością znaczków, to ją wykorzystujemy
        if number_of_stamps_for_value[i]+j < number_of_stamps_for_value[i+current_solution[x]*j]:
          number_of_stamps_for_value[i+current_solution[x]*j] = number_of_stamps_for_value[i]+j

  while number_of_stamps_for_value[y] < 99999:
    # y - najdroższy list który można opłacić zachowując ciągłość, przy obecnych wartościach znaczków
    # Szuka do momentu aż natrafi w tablicy na element "99999" (trochę brzydko to zrobiłem, gdyż "99999" przyjęto jako "wypełniacz" tablicy w miejscach nie wypełnionych)
    y = y+1

  # Jeśli x == n to mamy do czynienia z liściem w drzewie przez które algorytm przechodzi
  if x == n:
    # Jesli na tym liściu maksymalna wartość listu wieksza niz poprzedni "maximum_postage" to aktualizujemy optymalne wartości znaczków (optimal_stamps_values)
    # i najdroższy list jaki możemy opłacić (maximum_postage)
    if y-1 > maximum_postage:
      print("Znaleziono nowe optymalne wartości znaczków:")
      for i in range (1, n+1):
        print(current_solution[i])
        optimal_stamps_values[i] = current_solution[i]
      print("Znaleziono nową maksymalną cenę listu:")
      print(y-1)
      print("---")
      maximum_postage = y-1
    return

  # Zachowujemy poprzednią tablice "number_of_stamps_for_value" do tablicy "previous"
  previous = [0] * 1000
  for i in range (0, 1000):
    previous[i] = number_of_stamps_for_value[i]

  # Wykonujemy algorytm dla następnej "warstwy"
  for i in range(current_solution[x]+1, y+1):
    current_solution[x+1] = i
    #print("x = ", x, ", i = ", i)
    # x+1, bo "dodawany" jest kolejny znaczek
    powrot(x+1, y-1)
    # Podczas wracania z funkcji "powrot" (backtracking/"traverse" po drzewie) odtwarzamy "poprzednią"" tablicę do tablicy "number_of_stamps_for_value"
    for j in range(0, 1000):
      number_of_stamps_for_value[j] = previous[j]

#--- koniec funkcji "powrot", poniżej program główny ---#

# Maksymalna ilość rodzajów znaczków
n = 6
# Ilość miejsc na znaczek na kopercie
m = 3
# Sprawdzane w danym momencie wartości znaczków. Na początku wypełnione zerami
current_solution = [0] * 100
# Tablica w której będziemy zapisywać optymalne wartości znaczków które powinny być w sprzedaży. Na początku wypełniona zerami
optimal_stamps_values = [0] * 100
# Tablica w której zapisujemy ile znaczków potrzeba by opłacic list o danej wartości
# Przy większej ilości znaczków może być potrzeba większej tablicy, w przeciwnym wypadku napotkamy "out of index error w funkcji powrot()"
number_of_stamps_for_value = [0] * 1000
for i in range(1,1000):
  number_of_stamps_for_value[i] = 99999

# Pierwszy znaczek jest o wartości "1"
current_solution[1]=1

maximum_postage = 0

# Wartości początkowe. 1 oznacza jeden znaczek, a 0 oznacza początkową maksymalną wartość listu który można opłacić
powrot(1, 0)

# "Brzydki" kod, wymagający usunięcia na koniec z tablicy wartości 99999 które "wypełniają" puste pola.
# Usuwam je po to, by pozyskać z tej tablicy ilość znaczków którymi można zrealizować list o najwyższej cenie. Ilość ta jest wypisana w ostatniej linijce programu
number_of_stamps_for_value = list(filter((99999).__ne__, number_of_stamps_for_value))

print("\n\n\nOptymalne wartosci znaczków to:")
for i in range(1, n+1):
  print(optimal_stamps_values[i])
print("Największa możliwa wartość listu z zachowaniem ciągłości:");
print(maximum_postage)
print("Może ona zostać osiągnięta przez użycie", max(number_of_stamps_for_value), "znaczków")
