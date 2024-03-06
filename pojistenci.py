import hashlib
import sqlite3
import getpass

class Pojistenec:

      def __init__(self, jmeno: str, prijmeni: str, vek: int, tel_cislo: str, email: str):

            self._jmeno = jmeno
            self._prijmeni = prijmeni
            self._vek = vek
            self._tel_cislo = tel_cislo
            self._email = email
      
      def get_jmeno(self):
            return self._jmeno
      
      def get_prijmeni(self):
            return self._prijmeni
      
      def get_vek(self):
            return self._vek
      
      def get_tel_cislo(self):
            return self._tel_cislo
      
      def get_email(self):
            return self._email

      def __str__(self) -> str:
            return f"Jméno:{self._jmeno}     Příjmení:{self._prijmeni}     Věk:{self._vek}     Tel.číslo:{self._tel_cislo}     Email:{self._email}"
      
      def kratky_popis(self):
            return f"{self._jmeno} {self._prijmeni}"

      def set_jmeno(self, nove_jmeno):
            self._jmeno = nove_jmeno

      def set_prijmeni(self, nove_prijmeni):
            self._prijmeni = nove_prijmeni

      def set_vek(self, novy_vek):
            self._vek = novy_vek

      def set_tel_cislo(self, nove_tel_cislo):
            self._tel_cislo = nove_tel_cislo

class EvidencePojistencu:


      def __init__(self, jmeno_db = "databaze_projekt.db"):

            self.jmeno_db = jmeno_db
            self.conn = None
        
      def pripojeni_k_db(self):
            try:
                  self.conn = sqlite3.connect(self.jmeno_db)
                  self.cursor = self.conn.cursor()

            except sqlite3.Error as e:

                  return f"Připojení k databázi se nezdařilo: {e}"

      def odpojeni(self):

            if self.conn:
                  self.conn.commit()
                  self.cursor.close()
                  self.conn.close()
      
      def vlozeni_do_databaze(self, objekt): # vloží novou osobu do databáze

            self.pripojeni_k_db()
            self.cursor.execute("INSERT INTO pojistenci (jmeno, prijmeni, vek, tel_cislo, email) VALUES (?, ?, ?, ?, ?)", (objekt.get_jmeno(), objekt.get_prijmeni(), objekt.get_vek(), objekt.get_tel_cislo(), objekt.get_email()))
            self.odpojeni() 

      def vlozeni_do_databaze_hesel(self, heslo: str):# vkládá heslo do databáze

            self.pripojeni_k_db()

            self.cursor.execute("INSERT INTO hesla (heslo) VALUES (?)", (heslo,))

            self.odpojeni()
      
      
      @staticmethod
      def hash_hesla(heslo: str): # metoda pro hash hesla přes sha256
        # ! hodit někam jinam 
        hash_objekt = hashlib.sha256()
        hash_objekt.update(heslo.encode('utf-8'))
        hash_hodnota = hash_objekt.hexdigest()

        return hash_hodnota
      
           
      def kontrola_prihlaseni(self, email: str, heslo: str):# metoda pro kontrolu přihlášení - vrací True/False
            self.pripojeni_k_db()
            self.cursor.execute("SELECT 1 FROM pojistenci  JOIN hesla  ON id = id_osoby WHERE email = ? AND heslo = ?", (email, heslo))
            vysledek = self.cursor.fetchone() is not None
            self.odpojeni()

            return vysledek
      
      
      def kontrola_admin(self, email: str): # metoda pro kontrolu, jestli je přihlášená osoba admin
            self.pripojeni_k_db()
            self.cursor.execute("SELECT admin FROM pojistenci WHERE email = ?", (email,))
            vysledek = self.cursor.fetchone() 
            self.odpojeni()
            if vysledek == ('ne',):
                    return ("ne")
            return ("ano")
      
      
      def vytvor_objekt_z_datab(self, email: str): # metoda pro vytvoření objektu z databáze, vrací objekt ze třídy Pojistenci 
            
            self.pripojeni_k_db()
            self.cursor.execute("SELECT jmeno, prijmeni, vek, tel_cislo, email FROM pojistenci WHERE email = ? ", (email,))
            vysledek = self.cursor.fetchone() 
            self.odpojeni()

            nova_osoba = Pojistenec(vysledek[0], vysledek[1], vysledek[2], vysledek[3], vysledek[4])
            return nova_osoba
      
      
      
            
      def zmena_udaju_v_datab(self, email, sloupec, novy_udaj):# metoda pro změnu údajů v databázi, něco jako podmetoda metody "zmena_udaju"
            self.pripojeni_k_db()
            self.cursor.execute(f"UPDATE pojistenci SET {sloupec} = ? WHERE email = ?", (novy_udaj, email))
            self.odpojeni()


      def zmena_hesla(self, email, novy_udaj):# metoda pro změnu hesla
            self.pripojeni_k_db()
            self.cursor.execute("UPDATE hesla SET heslo = ? WHERE id_osoby = (SELECT id FROM pojistenci WHERE email = ?)", (novy_udaj, email))
            self.odpojeni()

      
      def vrat_druhy_pojisteni(self):# vypíše všechny pojištění u přihlášené osoby
            self.pripojeni_k_db()
            self.cursor.execute("SELECT druh_pojisteni FROM druhy_pojisteni")
            vysledek = self.cursor.fetchall() 
            self.odpojeni()

            druhy_pojisteni = [vysledek[0] for vysledek in vysledek]
            return druhy_pojisteni
      
      
      def pridej_druh_pojisteni(self, id_pojisteni, predmet_pojisteni, hodnota_pojisteni, osoba):# metoda pro možnost přidání pojištění pro přihlášenou osobu 

            self.pripojeni_k_db()
            self.cursor.execute("SELECT id FROM pojistenci WHERE email = ?", (osoba.get_email(),))
            id_osoby = self.cursor.fetchone()[0]
            self.cursor.execute("INSERT INTO osoby_druhy_pojisteni (id_osoby, id_druhu_pojisteni, predmet_pojisteni, hodnota_pojisteni) VALUES (?, ?, ?, ?)", (id_osoby,int(id_pojisteni), predmet_pojisteni, hodnota_pojisteni))
            self.odpojeni()
            return ("Vaše pojištění bylo úspěšně přidáno")
      
      
      def vypis_pojisteni(self, osoba):# vypíše druhy pojištění pro rozhraní 

            self.pripojeni_k_db()

            self.cursor.execute("SELECT id FROM pojistenci WHERE email = ?", (osoba.get_email(),))
            id_osoby = self.cursor.fetchone()[0]  

            self.cursor.execute("SELECT druh_pojisteni, predmet_pojisteni, hodnota_pojisteni FROM osoby_druhy_pojisteni JOIN druhy_pojisteni ON id_druhu_pojisteni = druhy_pojisteni.id WHERE id_osoby = ?", (id_osoby,))
            pojisteni = self.cursor.fetchall()
            self.odpojeni()

            return '\n'.join(str(pojisteni[polozka]) for polozka in range(len(pojisteni)))

    
      def zmena_udaju_v_datab_pojisteni(self, osoba):# změna údajů u zdravotního pojištění při změně údajů osoby

            self.pripojeni_k_db()
            self.cursor.execute("SELECT id FROM pojistenci WHERE email = ?", (osoba.get_email(),))
            id_osoby = self.cursor.fetchone()[0]
            self.cursor.execute("UPDATE osoby_druhy_pojisteni SET predmet_pojisteni = ? WHERE id_osoby = ? AND id_druhu_pojisteni = ?", (osoba.kratky_popis(), id_osoby, 3))
            self.odpojeni()

      
      def vypis_vsech_pojistencu(self):# metoda pro výpis všech pojištěnců z databáze, kteří nejsou admin
            self.pripojeni_k_db()
            self.cursor.execute("SELECT * FROM pojistenci WHERE admin = 'ne' ")
            pojistenci = self.cursor.fetchall()
            self.odpojeni()
            vypis_vsech = ""
            for osoba in pojistenci:
                  nova_osoba = Pojistenec(osoba[1], osoba[2], osoba[3], osoba[4], osoba[5])
                  vypis_vsech += str(nova_osoba) + "\n"
            return vypis_vsech
      
      
      def pridej_admin(self,nova_osoba): # metoda pro přidání admina
            self.pripojeni_k_db()
            self.cursor.execute("INSERT INTO pojistenci (jmeno, prijmeni, vek, tel_cislo, email, admin) VALUES (?, ?, ?, ?, ?, ?)", (nova_osoba.get_jmeno(), nova_osoba.get_prijmeni(), nova_osoba.get_vek(), nova_osoba.get_tel_cislo(), nova_osoba.get_email(), "ano"))
            self.odpojeni()
            return f"Admin {nova_osoba.kratky_popis()} byl vytvořen"
      