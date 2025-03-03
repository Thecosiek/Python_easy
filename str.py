""" Some misc python structures """

from itertools import tee, starmap
from operator import itemgetter

def trojki(pairs):
    pary = list(pairs)
    potegi = starmap(pow, pary)
    wynik = ((a, b, c) for (a, b), c in zip(pary, potegi))
    return wynik

pairs = [(2, 3), (3, 2), (4, 0)]
wynik = trojki(iter(pairs))
print(list(wynik))

#####################################################################################################################

def zrob_drzewo(n, iterable):
    items = iter(iterable)
    
    def zbuduj(size):
        if size == 0:
            return None
        lewy = size // 2
        prawy = size - lewy - 1
        lewy = zbuduj(lewy)
        korzen = next(items)
        prawy = zbuduj(prawy)
        return (lewy, korzen, prawy)
    
    return zbuduj(n)

tree = zrob_drzewo(7, "alakota")
print(tree)

def obejdź(tree, preorder=False, inorder=False, postorder=False):
    if sum([preorder, inorder, postorder]) != 1:
        raise ValueError("Dokładnie jeden z argumentów preorder, inorder, postorder musi być True.")
    
    if tree is None:
        return
    
    lewy, korzen, prawy = tree
    
    if preorder:
        yield korzen
        yield from obejdź(lewy, preorder=preorder)
        yield from obejdź(prawy, preorder=preorder)
    elif inorder:
        yield from obejdź(lewy, inorder=inorder)
        yield korzen
        yield from obejdź(prawy, inorder=inorder)
    elif postorder:
        yield from obejdź(lewy, postorder=postorder)
        yield from obejdź(prawy, postorder=postorder)
        yield korzen

print(list(obejdź(tree, inorder=True)))  # ['a', 'l', 'a', 'k', 'o', 't', 'a']
print(list(obejdź(tree, preorder=True)))  # ['k', 'l', 'a', 'a', 't', 'o', 'a']
print(list(obejdź(tree, postorder=True)))  # ['a', 'a', 'l', 'a', 'o', 't', 'k']

#####################################################################################################################

def odpluskw(func):
    def wrapper(*args, **kwargs):
        print(f"Wywołanie funkcji {func.__name__} z argumentami: args={args}, kwargs={kwargs}")
        wynik = func(*args, **kwargs)
        print(f"Wynik funkcji {func.__name__}: {wynik}")
        return wynik
    return wrapper

@odpluskw
def przyklad(a, b, c=10):
    return a + b + c

przyklad(1, 2, c=5)
