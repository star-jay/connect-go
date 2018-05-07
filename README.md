# 4x4 :4-op-een-rij #

Wedstrijd tussen verschillende bots die variaties van 4-op-een-rij spelen. 

### Een nieuwe Bot ###

Maak een bot aan die overerft van `Player` in bots.py.

    class Mybot(bots.Player):

Voeg daarna je bot toe in tornooi.py `Main()` function.

    players.append(MyBot())

Run daarna tornooi.py. Elke bot speelt een bepaald aantal games tegen elkaar. Wie op het einde van het tornooi de hoogste ELO-ranking heeft wint. Er is ook een ranking op tijd en originaliteit.

### Bot ontwerp ###

Het grootste bulk van je code speelt zich af in de `makeMove(self,game_state,moves)` functie. 
Hierin komt je code die bepaalt welke kolom je bot speelt. Bij een ongeldige kolom verlies je de huidige game. 
`game_state` is een list met alle mogelijke velden. Tijdens het spel veranderen de waardes van neutraal naar het teken van de spelers.
 `moves` is een lijst van alle opeenvolgende moves die gemaakt zijn. Andere belangrijke functies zijn `startgame(self,sign)` en `endgame(self,winorlose,game_state,moves)`. Deze worden op opgeroepen voor en na een game tussen twee bots. Je bot zelf wordt één keer aangemaakt bij de start van het tornooi.
 
### Game-logic ###
De game-logic vind je terug in vieropeenrij.py. Deze functies kan je gebruiken bij het ontwerp van je bot.

Volgende constanten bepalen hoe een spel gespeeld wordt :

    #DIMENSIONS
    ROWS = 6
    COLS = 7
    MAX_RANGE = ROWS * COLS
    TARGET = 4