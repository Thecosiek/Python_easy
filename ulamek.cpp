""" Implementation of 'ulamek' (in Polish fraction) in python with some easy tests """

import math 

class Ulamek:
    """ Konstruktor """
    def __init__(self, licznik, mianownik):
        
        assert mianownik != 0
        
        if mianownik < 0:
            licznik *= -1
            mianownik *= -1
        
        NWD = math.gcd(licznik, mianownik)
        
        self.licznik = licznik // NWD
        self.mianownik = mianownik // NWD
        
    """ Operatory arytmetyczne: +, -, *, / """
    def __add__(self, other):
        return Ulamek(self.licznik * other.mianownik + self.mianownik * other.licznik, self.mianownik * other.mianownik)
    
    def __sub__(self, other):
        other2 = Ulamek(other.licznik * -1, other.mianownik)
        return self + other2
    
    def __mul__(self, other):
        return Ulamek(self.licznik * other.licznik, self.mianownik * other.mianownik)
    
    def __truediv__(self, other):
        assert other.licznik != 0
        other2 = Ulamek(other.mianownik, other.licznik)
        return self * other2

    """ Operatory porównania: <, <=, ==, !=, >, >= """
    def __lt__(self, other):
        return self.licznik * other.mianownik < self.mianownik * other.licznik
    
    def __le__(self, other):
        return self.licznik * other.mianownik <= self.mianownik * other.licznik
        
    def __eq__(self, other):
        return self.licznik * other.mianownik == self.mianownik * other.licznik
    
    def __ne__(self, other):
        return self.licznik * other.mianownik != self.mianownik * other.licznik
    
    def __gt__(self, other):
        return self.licznik * other.mianownik > self.mianownik * other.licznik
    
    def __ge__(self, other):
        return self.licznik * other.mianownik >= self.mianownik * other.licznik
        
    """ Konwersje do napisu """
    def __str__(self):
        return f"{self.licznik} / {self.mianownik}"
    
    def __repr__(self):
        return f"Ulamek({self.licznik}, {self.mianownik})"
    
    
if __name__ == "__main__":
    
    """ Test: Wykrywanie 0 w mianowniku"""
    try:
        u0 = Ulamek(1, 0)
        print("Test nie powiódł się: brak wyjątku!")
    except AssertionError as e:
        print(f"Poprawnie Wykryto Błędny Ułamek")
    
    print()
        
    u1 = Ulamek(-2, -10)
    u2 = Ulamek(4, -6)
    u3 = Ulamek(0, 25)
    u4 = Ulamek(4, 7)
   
    """ Test: Konwersja ulamka w konstruktorze""" 
    
    print(u1)
    print("Powinno byc 1 / 5")
    print(u2)
    print("Powinno byc -2 / 3")
    print(u3)   
    print("Powinno byc 0 / 1")
    print(u4)
    print("Powinno byc 4 / 7")    
    print()
    
    """ Test: Dodawanie"""
    print(u1 + u4)
    print("Powinno byc 27 / 35")
    
    print(u3 + u4)
    print("Powinno byc 4 / 7")
    
    print(u1 + u2)
    print("Powinno byc -7 / 15")
    print()
    
    """ Test: Odejmowanie"""
    print(u1 - u4)
    print("Powinno byc -13 / 35")
    
    print(u3 - u4)
    print("Powinno byc -4 / 7")
    
    print(u1 - u2)
    print("Powinno byc 13 / 15")
    print()
    
    """ Test: Mnożenie"""
    print(u1 * u4)
    print("Powinno byc 4 / 35")
    
    print(u3 * u4)
    print("Powinno byc 0 / 1")
    
    print(u1 * u2)
    print("Powinno byc -2 / 15")
    print()
    
    """ Test: Dzielenie"""
    print(u1 / u4)
    print("Powinno byc 7 / 20")
    
    print(u3 / u4)
    print("Powinno byc 0 / 1")
    
    print(u1 / u2)
    print("Powinno byc -3 / 10")
    
    """Dzielenie Przez Zero"""
    try:
        print(u4 / u3)
        print("Test nie powiódł się: brak wyjątku!")
    except AssertionError as e:
        print(f"Poprawnie Wykryto Próbę Dzielenia przez 0")
    
    print()
    
    """ Test: Operatory Porównania"""
    
    assert u4 > u1
    assert u3 > u2
    assert u1 > u3
    
    assert u4 >= u1
    assert u3 >= u2
    assert u1 >= u3
    
    v1 = Ulamek(1 , 5)
    v3 = Ulamek(0, 100)
    v4 = Ulamek(8, 14)
    
    assert(u1 == v1)
    assert(u3 == v3)
    assert(u4 == v4)
    
    assert(u1 <= v1)
    assert(u3 <= v3)
    assert(u4 <= v4)
    
    assert(u1 >= v1)
    assert(u3 >= v3)
    assert(u4 >= v4)
    
    z1 = Ulamek(1, 6)
    assert(u1 != z1)
    
    assert u4 != u1
    assert u3 != u2
    assert u1 != u3
    
    assert u1 < u4
    assert u2 < u3
    assert u3 < u1
    
    assert u1 <= u4
    assert u2 <= u3
    assert u3 <= u1
    
    print("Testy Operatorów Porównania Zakończone Sukcesem")
    print()
    
    """ Test: Czy doszło do modyfikacji argumentów przy użyciu operatorów? """
    
    print(u1)
    print("Powinno byc 1 / 5")
    print(u2)
    print("Powinno byc -2 / 3")
    print(u3)   
    print("Powinno byc 0 / 1")
    print(u4)
    print("Powinno byc 4 / 7")    
    print()
    
    """ Test Reprezentacji"""
    assert(repr(u1) == "Ulamek(1, 5)")
    
    print("Poprawna reprezentacja")
    print()
    
    print("Testowanie Zakończone Sukcesem")
