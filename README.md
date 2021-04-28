# Testovanie mboxer servera

## Čo urobiť pred testovaním

1. Pred použitím musíte nainštalovať `pyyaml`, ktorý sa možno volá vo Vašej distribúcii
   inak, možno `python3-yaml` alebo tak nejako.
2. Takisto je treba nainštalovať pythonovskú knižnicu `pygments`.

## Ako testovať hromadne všetky testy

3. Skopírujte do tohto adresára váš program a nazvite ho `mboxer.py`.
4. Spustite skript `runtests.sh`.
5. Spustia sa testy. Vznikne súbor `results.html`, ktorý si môžete otvoriť v browseri.
6. Pre každý test máte pod linkom uvedené, čo sa posielalo a v akom stave skončil.
7. Ak bol nejaký chybový výstup (niečo padlo), chybový výstup vidíte pod linkom err.

