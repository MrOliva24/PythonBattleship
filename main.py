# coding: cp1252
import random
import os
from multiprocessing import Process



class Casella():
    def __init__(self,coordenades,tipus):
        assert isinstance(coordenades, list) and len(coordenades) == 2 and all(isinstance(x, int) for x in coordenades), "Error: Valor de coordenades no es del tipus List[int, int]"
        assert isinstance(tipus, str), "Error: El tipus de la casella no es del tipus Str"
        assert tipus in ["A", "p", "c", "d", "f"], "Error: El tipus de casella no és A, p, c, f"
        #defincio dels parametres
        self.coordenades = coordenades
        self.tipus = tipus
        self.x = coordenades[0]
        self.y = coordenades[1]
    #getters i setters
    def get_tipus(self):
        return self.tipus
    def get_coordenades(self):
        return self.coordenades
    def set_tipus(self, tipus_2):
        assert isinstance(tipus_2, str) , "Error: El tipus de la casella no es del tipus Str"
        assert tipus_2 in ["A", "p", "c", "d", "f"] , "Error: El tipus de casella no és A, p, c, f"
        self.tipus = tipus_2

    def __str__(self):
        return (f"{self.tipus} en coordenades {self.x},{self.y}")


class Taulell():
    def __init__(self, X, Y):
        assert isinstance(X, int) and isinstance(Y, int), "Dimensions del taulell no son enters"  #Quitarlo en el codigo final solo para pruebas
        self.X = X
        self.Y = Y
        self.taulell = [[Casella([i, j], "A") for j in range(self.Y)] for i in range(self.X)]
        self.tipus_possibles = [ "p" , "c" , "d" , "f" ]
        self.vaixells = {
            "p": [1, 6],
            "f": [4, 2],
            "c": [2, 4],
            "d": [3, 3]
        }

        self.vaixells_colocats = {i: [ [] for j in range(self.vaixells[i][0]) ] for i in self.tipus_possibles}
        self.barcos_taulell = 0
        self.vaixells_pr = {
            "p": [1, 6],
            "f": [4, 2],
            "c": [2, 4],
            "d": [3, 3]
            
        } #Evitar ZeroDivisionError
        

    def restore_vaixells(self):

        self.taulell = [[Casella([i, j], "A") for j in range(self.Y)] for i in range(self.X)]

        self.vaixells = {
            "p": [1, 6],
            "f": [4, 2],
            "c": [2, 4],
            "d": [3, 3]
        }



        self.vaixells_pr  = {
            "p": [1, 6],
            "f": [4, 2],
            "c": [2, 4],
            "d": [3, 3]
            
        }
        #coordenades[0] controlan altura i coordenades[1] controlan longitud
    def controla_coordenada(self, coordenades, tipus, orientacio): #Esta fet d'aquesta manera ja que a la pràctica no s'especifica que els vaixells no puguin ser concurrents a uns altres
 
            try:
                assert orientacio in ["v_i", "v_s", "h_e", "h_d"], "Error: la direcció no està en [v_i, v_s, h_e, h_d]"
                assert isinstance(coordenades, list) and len(coordenades) == 2 and all(isinstance(x, int) for x in coordenades), "Error: Les coordenades que estàs intentant introduïr no són correctes"
                assert tipus in self.tipus_possibles, "Error: Has introduït un tipus erroni"
                assert all(0 <= coord < self.X for coord in coordenades), "Error: Les coordenades que estàs intentant introduïr no són correctes"
                assert self.taulell[coordenades[0]][coordenades[1]].get_tipus() == "A", "Error: Posició ja ocupada per un vaixell"
                if orientacio == 'v_i':
                    assert coordenades[0] + self.vaixells[tipus][1] - 1 < self.X, "Error: el vaixell no hi entra en aquesta direcció"
                    for i in range(coordenades[0], coordenades[0] + self.vaixells[tipus][1]):
                        if self.taulell[i][coordenades[1]].get_tipus() != "A":
                            raise AssertionError("Error: colocant aquest vaixell amb aquesta orientació et menjes un altre vaixell")
                elif orientacio == 'v_s':
                    assert coordenades[0] - self.vaixells[tipus][1] - 1 >= 0, "Error: el vaixell no hi entra en aquesta direcció"
                    for i in range(coordenades[0], coordenades[0] - self.vaixells[tipus][1], -1):
                        if self.taulell[i][coordenades[1]].get_tipus() != "A":
                            raise AssertionError("Error: colocant aquest vaixell amb aquesta orientació et menjes un altre vaixell")
                elif orientacio == 'h_d':
                    assert coordenades[1] + self.vaixells[tipus][1] - 1 < self.Y, "Error: el vaixell no hi entra en aquesta direcció"
                    for j in range(coordenades[1], coordenades[1] + self.vaixells[tipus][1]):
                        if self.taulell[coordenades[0]][j].get_tipus() != "A":
                            raise AssertionError("Error: colocant aquest vaixell amb aquesta orientació et menjes un altre vaixell")
                else:
                    assert coordenades[1] - self.vaixells[tipus][1] - 1 >= 0, "Error: el vaixell no hi entra en aquesta direcció"
                    for j in range(coordenades[1], coordenades[1] - self.vaixells[tipus][1], -1):
                        if self.taulell[coordenades[0]][j].get_tipus() != "A":
                            raise AssertionError("Error: colocant aquest vaixell amb aquesta orientació et menjes un altre vaixell")
                return True, None

            except AssertionError as error:
                return False, error
    

    
    def coloca_vaixell(self, coordenades, tipus, orientacio):

        if self.controla_coordenada(coordenades,tipus,orientacio)[0]:

            if orientacio == "v_i":
                for i in range(coordenades[0], coordenades[0] + self.vaixells[tipus][1]):  
                    self.taulell[i][coordenades[1]].set_tipus(tipus)
                    coords = [i, coordenades[1]]
                    if tipus in self.vaixells_colocats:
                        self.vaixells_colocats[tipus][(len(self.vaixells_colocats[tipus]) - 1) - (self.vaixells_pr[tipus][0]) ].append(coords)
                    else:
                        self.vaixells_colocats[tipus] = [[coordenades]]  
            
            elif orientacio == 'v_s':   
                for i in range(coordenades[0], coordenades[0] - self.vaixells[tipus][1], -1):  
                    self.taulell[i][coordenades[1]].set_tipus(tipus)
                    coords = [i, coordenades[1]]
                    if tipus in self.vaixells_colocats:
                        self.vaixells_colocats[tipus][(len(self.vaixells_colocats[tipus]) - 1) - (self.vaixells_pr[tipus][0]) ].append(coords)
                    else:
                        self.vaixells_colocats[tipus] = [[coordenades]]        
            elif orientacio == 'h_d':
                for j in range(coordenades[1], coordenades[1] + self.vaixells[tipus][1]):
                    self.taulell[coordenades[0]][j].set_tipus(tipus)
                    coords = [coordenades[0],j]
                    if tipus in self.vaixells_colocats:
                        self.vaixells_colocats[tipus][(len(self.vaixells_colocats[tipus]) - 1) - (self.vaixells_pr[tipus][0]) ].append(coords)
                    else:
                        self.vaixells_colocats[tipus] = [[coordenades]]
            else:
                for j in range(coordenades[1], coordenades[1] - self.vaixells[tipus][1], -1):
                    self.taulell[coordenades[0]][j].set_tipus(tipus)
                    coords = [coordenades[0],j]
                    if tipus in self.vaixells_colocats:
                        self.vaixells_colocats[tipus][(len(self.vaixells_colocats[tipus]) - 1) - (self.vaixells_pr[tipus][0]) ].append(coords)
                    else:
                        self.vaixells_colocats[tipus] = [[coordenades]]

        
            self.vaixells_pr[tipus][0] -= 1
            self.barcos_taulell += 1
        else:
            print(self.controla_coordenada(coordenades,tipus,orientacio)[1])

    def inicialitza(self):
        tipus = 0
        print("Inicialitza el Taulell:")
        while (tipus != "s" and self.barcos_taulell < 10):
            try:
                #Inicialitzacio visual del taulell
                print(" ")
                print("Els tipus de barcos son: fragates (f), (d), cuirassats (c), portaavions (p)")
                print(" ")
                print(f"De cada tipus t'en queden per col·locar: f: {self.vaixells_pr['f'][0]} | d: {self.vaixells_pr['d'][0]} | c: {self.vaixells_pr['c'][0]} | p: {self.vaixells_pr['p'][0]}")

                tipus = input("Introdueix el tipus del barco [f, d, c, p, (s per sortir)]: ")

                if tipus in self.tipus_possibles:
                    X = input("Introdueix la Fila (A-H): ")
                    Y = int(input("Introdueix la Columna (0-7): ")) 
                    orientacio = input("Introdueix l'orientació [v_i, v_s, h_e, h_d]: ")
                    legal = self.controla_coordenada([ord(X) - 65, Y], tipus, orientacio)
                    if legal[0]:
                        self.coloca_vaixell([ord(X) - 65,Y], tipus, orientacio)
                    else:
                        print(legal[1])
                else:
                    if tipus != "s":
                        raise AssertionError("Error: El tipus de vaixell que has introduit no existeix")
                    else:
                        print("Heu seleccionat sortir")
            except AssertionError as error:
                print(error)

    def inicialitza_random(self):
        
        try:
            self.restore_vaixells()
            barcos = ["f", "f", "f", "f", "d", "d", "d", "c", "c", "p"]
            possible_coords = [[i,j] for i in range(self.X) for j in range(self.Y)]
            used_coords = []
            while len(barcos) > 0:
                orientacio = random.choice(["v_i", "v_s", "h_e", "h_d"])
                coords_coloca = random.choice(possible_coords)
                legal = self.controla_coordenada(coords_coloca, barcos[0], orientacio)
                if legal[0]:
                    self.coloca_vaixell(coords_coloca, barcos[0], orientacio)
                    for i in self.vaixells_colocats[barcos[0]]:
                        for j in i:
                            if j not in used_coords:
                                possible_coords.remove(j)
                                used_coords.append(j)
                    barcos.remove(barcos[0])
            self.mostra_taulell()
        except:
            pass


    def Update(self, coordenades):
        cell = self.taulell[coordenades[0]][coordenades[1]]
        tipus = cell.get_tipus()
        if tipus !='A':
            cell.set_tipus('A')
            for ship in self.vaixells_colocats[tipus]:
                for pos in ship:
                    if pos[0] == coordenades[0] and pos[1] == coordenades[1]:
                        ship.remove(pos)
                        if ship == []:
                            self.vaixells_colocats[tipus].remove(ship)
                            self.barcos_taulell -= 1
                        
        return tipus

    def estat_del_taulell(self):
        vaixells_restants = self.barcos_taulell
    
        
        print(f"El nombre de Vaixells que queden en el taulell són: {vaixells_restants}")
    
        
        for tipus in self.vaixells:
            caselles_vives = 0
            for vaixells in self.vaixells_colocats[tipus]:
                for coordenades_vaixell in vaixells:
                    if self.taulell[coordenades_vaixell[0]][coordenades_vaixell[1]].get_tipus() != "A":
                        caselles_vives += 1
            percentage_vives = caselles_vives / (self.vaixells[tipus][1] * self.vaixells[tipus][0])* 100
            print(f"Queden {percentage_vives:.2f}% de caselles tipus {tipus} vives")
    
    def mostra_taulell(self): #__str__
        print(f"\nVAIXELLS COLOCATS: {self.vaixells_colocats}\n")
        rows = []
        rows.append("  " + "   " + " | ".join(str(i) for i in range(self.X)))
        for i in range(self.Y):
            row = f" {chr(i + 65)} | "
            row += " | ".join(cell.tipus for cell in self.taulell[i])
            rows.append(row)
        #self.estat_del_taulell() #Acabar codigo y probar esta parte
        print("\n".join(rows),"\n")

    
class Jugador():
    def __init__(self,nom,X,Y):
        self.nom = nom
        self.historial = [ ]
        self.encertats = {i: [] for i in ["f", "c", "d", "p"]}
        self.taulell = Taulell(X,Y)
    def get_nom(self):
        return self.nom
    def get_encertats(self):
        return self.encertats
    def get_historial(self):
        return self.historial
    def set_nom(self, nom_2):
        self.nom = nom_2
    def inicialitza_taulell(self):
        self.taulell.inicialitza()
        #self.taulell.inicialitza_random() #Esta puesto asi para no tener que inicializar cada vez que probamos quitar para el codigo final
    def Atac(self, coordenades, oponent):
        self.historial.append(coordenades)
        if oponent.taulell.taulell[coordenades[0]][coordenades[1]].get_tipus() == "A":
            return False
        else:
            return True
    def reaccio(self, coordenades, resultat, oponent):
        tipus = oponent.taulell.taulell[coordenades[0]][coordenades[1]].get_tipus()
        if not resultat:
            print('Aigua!')
            return 0
        else:
            sunk = True
            while sunk:
                for vaixell in oponent.taulell.vaixells_colocats[tipus]:
                    for coords in vaixell:
                        if oponent.taulell.taulell[coords[0]][coords[1]].get_tipus() != "A":
                            sunk = False
            if sunk:
                print("Enfonsat!!")
                return 2
            else:
                print("Tocat!")
                return 1
    def __str__(self):
        return (f"Jugador: {self.nom}")
    def __repr__(self):
        return (f"Jugador: {self.nom}\nHistorial: {self.historial}\Encertats: {self.encertats}") #Entiendo que se refiere a esto con __rep__ 

class JugadorMaquina(Jugador):
    def __init__(self, nom, X, Y):
        super().__init__(nom,X,Y)
        self.historial = [ ]
        self.encertats = {i: [] for i in [ "f", "c", "d", "p" ] }
        self.taulell = Taulell(X,Y)
        self.taulell_cobert = [["?" for j in range(X)] for i in range(Y)]
        self.coordenades_atac = [[i,j] for i in range(X) for j in range(Y)]
    def get_nom(self):
        return self.nom
    def get_encertats(self):
        return self.encertats
    def get_historial(self):
        return self.historial
    def set_nom(self, nom_2):
        self.nom = nom_2
    def inicialitza_random(self):
        action_process = Process(target=self.taulell.inicialitza_random)
        action_process.start()
        action_process.join(timeout=1)
        action_process.terminate() 

    def atac(self, coordenades, oponent):
        self.historial.append(coordenades)
        if oponent.taulell.taulell[coordenades[0]][coordenades[1]].get_tipus() == "A":
            return False
        else:
            return True
    def reaccio(self,coordenades,resultat,oponent):
        tipus = oponent.taulell.taulell[coordenades[0]][coordenades[1]].get_tipus()
        if not resultat:
            print('Aigua!')
            return 0
        else:
            sunk = True
            while sunk:
                for vaixell in oponent.taulell.vaixells_colocats[tipus]:
                    for coords in vaixell:
                        if oponent.taulell.taulell[coords[0]][coords[1]].get_tipus() != "A":
                            sunk = False
            if sunk:
                print("Enfonsat!!")
                return 2
            else:
                print("Tocat!")
                return 1
        
    def actualitza_taulell_cobert(self,coordenades,tipus):
        self.taulell_cobert[coordenades[0]][coordenades[1]] = str(tipus)
    def mostra_taulell_cobert(self):
        rows = []
        rows.append("  " + "   " + " | ".join(str(i) for i in range(self.taulell.X)))
        for i in range(self.taulell.Y):
            row = f" {chr(i + 65)} | "
            row += " | ".join(cell for cell in self.taulell_cobert[i])
            rows.append(row)
        return print("\n".join(rows))


class Partida():
    def __init__(self, nom1, nom2,X,Y):
        self.jugador1 = Jugador(nom1,X,Y)
        self.jugador2 = JugadorMaquina(nom2,X,Y)
    def estat_partida(self):
        barcos_1 = self.jugador1.taulell.barcos_taulell
        barcos_2 = self.jugador2.taulell.barcos_taulell
        print("Al jugador " + str(self.jugador1.nom) + " li queden " + str(self.jugador1.taulell.barcos_taulell) + " barcos vius al taulell\n" )
        print("Al jugador " + str(self.jugador2.nom) + " li queden " + str(self.jugador2.taulell.barcos_taulell) + " barcos vius al taulell\n" )
        if barcos_1 > barcos_2:
            print(f"El jugador amb més proabilitats de guanyar és {self.jugador1.nom}")
        elif barcos_2 > barcos_1:
            print(f"El jugador amb més proabilitats de guanyar és {self.jugador2.nom}")
        else:
            print(f"En aquest moment tant {self.jugador2.nom} com {self.jugador1.nom} tenen les mateixes probabilitats de guanyar")
    def Guanyador(self):
        barcos_1 = self.jugador1.taulell.barcos_taulell
        barcos_2 = self.jugador2.taulell.barcos_taulell
        if barcos_1 > barcos_2:
            return 1
        elif barcos_2 == barcos_1:
            return 0
        else:
            return -1
    def Comenca_partida(self):
        self.jugador1.inicialitza_taulell()
        self.jugador2.taulell.inicialitza_random()
        continuar = 's'
        while (continuar.lower() == 's' and self.jugador1.taulell.barcos_taulell > 0 and self.jugador2.taulell.barcos_taulell > 0) :
            try:
                #Torn jugador humà
                os.system('cls')
                print(f"\nTorn de: {self.jugador1.nom}\n")
                print("El teu taulell és: \n")
                self.jugador1.taulell.mostra_taulell()
                print("El taulell del rival és: \n")
                self.jugador2.mostra_taulell_cobert()
                #self.jugador2.taulell.mostra_taulell() #Solo para pruebas quitar del codigo final
                print("Introdueix les coordenades per l'atac\n")
                coordX = input(f"Introdueix fila A-{chr(self.jugador2.taulell.X + 64)} ")
                assert (len(coordX) == 1 and ( 0 <= ord(coordX)-65 < self.jugador2.taulell.X)), f"La columna ha de ser una lletra majúscula entre la A i la {chr(self.jugador2.taulell.X + 64)}"
                coordY = input("Introdueix columna (0-7) ")
                assert (len(coordY) == 1 and 0<= int(coordY) < self.jugador2.taulell.Y ) , f"La fila ha de ser un enter entre el 0 i el {self.jugador2.taulell.X - 1}"
                xy = [int(ord(coordX) - 65) ,int(coordY)]
                resultat = self.jugador1.Atac(xy, self.jugador2)
                reaccio = self.jugador1.reaccio(xy, resultat, self.jugador2)
                tipus = self.jugador2.taulell.taulell[xy[0]][xy[1]].get_tipus()
                if reaccio != 0:
                    tipus = self.jugador2.taulell.Update(xy)
                    self.jugador1.encertats[tipus].append(xy)
                self.jugador2.actualitza_taulell_cobert(xy,tipus)
                os.system('cls')
                print("\nDesprés d'aquesta jugada el taulell rival és:\n")
                self.jugador2.mostra_taulell_cobert()
                #Torn jugador màquina
                print(f"\n Torn de {self.jugador2.nom}")
                xy_m = random.choice(self.jugador2.coordenades_atac)
                self.jugador2.coordenades_atac.remove(xy_m) 
                resultat = self.jugador2.Atac(xy_m, self.jugador1)
                reaccio = self.jugador2.reaccio(xy_m, resultat, self.jugador1)
                if reaccio != 0:
                    tipus = self.jugador1.taulell.Update(xy_m)
                    self.jugador2.encertats[tipus].append(xy_m)
                print(f"\nEl jugador màquina ha atacat a la posicio {chr(xy_m[0] + 65)}-{xy_m[1]} del teu taulell\nA aquesta posicio hi havia una casella del tipus {tipus if reaccio != 0 else 'A'}\n")

                
                self.estat_partida()
                continuar = input("Introdueix s/S si desitges continuar la partida: ")
            except AssertionError as error: 
                print(error)
        if self.Guanyador() == 1:
            print(f"El guanyador ha estat {self.jugador1.nom}")
        elif self.Guanyador() == 2:
            print(f"El guanyador ha estat {self.jugador2.nom}")
        else:
            print("La partida ha acabat en empat")
        print(f"\nL'historial de jugades de {self.jugador1.nom} ha estat {self.jugador1.historial}\nL'historial de jugades de {self.jugador2.nom} ha estat {self.jugador2.historial}")


#Partida("Marc", "David", 8,8).Comenca_partida()



if __name__ == "__main__":
	Partida("Marc", "David", 8,8).Comenca_partida()















