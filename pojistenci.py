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

class EvidencePojistencu:
      
      @staticmethod
      def vlozeni_do_databaze(objekt): # vloží novou osobu do databáze
            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pojistenci (jmeno, prijmeni, vek, tel_cislo, email) VALUES (?, ?, ?, ?, ?)", (objekt.get_jmeno(), objekt.get_prijmeni(), objekt.get_vek(), objekt.get_tel_cislo(), objekt.get_email()))
            conn.commit()
            cursor.close()
            conn.close() 
      
      @staticmethod
      def vlozeni_do_databaze_hesel(heslo: str):# vkládá heslo do databáze
            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO hesla (heslo) VALUES (?)", (heslo,))
            conn.commit()
            cursor.close()
            conn.close()
      
      
      @staticmethod
      def hash_hesla(heslo: str): # metoda pro hash hesla přes sha256
        # ! hodit někam jinam 
        hash_objekt = hashlib.sha256()
        hash_objekt.update(heslo.encode('utf-8'))
        hash_hodnota = hash_objekt.hexdigest()

        return hash_hodnota
      
      @staticmethod      
      def kontrola_prihlaseni(email: str, heslo: str):# metoda pro kontrolu přihlášení - vrací True/False
            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM pojistenci  JOIN hesla  ON id = id_osoby WHERE email = ? AND heslo = ?", (email, heslo))
            vysledek = cursor.fetchone() is not None
            conn.close()
            return vysledek
      
      @staticmethod
      def kontrola_admin(email: str): # metoda pro kontrolu, jestli je přihlášená osoba admin
            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute("SELECT admin FROM pojistenci WHERE email = ?", (email,))
            vysledek = cursor.fetchone() 
            conn.close()
            if vysledek == ('ne',):
                    return ("ne")
            return ("ano")
      
      @staticmethod
      def vytvor_objekt_z_datab(email: str): # metoda pro vytvoření objektu z databáze, vrací objekt ze třídy Pojistenci 
            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute("SELECT jmeno, prijmeni, vek, tel_cislo, email FROM pojistenci WHERE email = ? ", (email,))
            vysledek = cursor.fetchone() 
            conn.close()
            nova_osoba = Pojistenec(vysledek[0], vysledek[1], vysledek[2], vysledek[3], vysledek[4])
            return nova_osoba
      
      
      
      @staticmethod      
      def zmena_udaju_v_datab(email, sloupec, novy_udaj):# metoda pro změnu údajů v databázi, něco jako podmetoda metody "zmena_udaju"
            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute(f"UPDATE pojistenci SET {sloupec} = ? WHERE email = ?", (novy_udaj, email))
            conn.commit()
            conn.close()

      @staticmethod
      def zmena_hesla(email, novy_udaj):# metoda pro změnu hesla
            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE hesla SET heslo = ? WHERE id_osoby = (SELECT id FROM pojistenci WHERE email = ?)", (novy_udaj, email))
            conn.commit()
            conn.close()

      @staticmethod
      def vrat_druhy_pojisteni():# vypíše všechny pojištění u přihlášené osoby
            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute("SELECT druh_pojisteni FROM druhy_pojisteni")
            vysledek = cursor.fetchall() 
            conn.close()
            druhy_pojisteni = [vysledek[0] for vysledek in vysledek]
            return druhy_pojisteni
      
      @staticmethod
      def pridej_druh_pojisteni(id_pojisteni, predmet_pojisteni, hodnota_pojisteni, osoba):# metoda pro možnost přidání pojištění pro přihlášenou osobu 

            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM pojistenci WHERE email = ?", (osoba.get_email(),))
            id_osoby = cursor.fetchone()[0]
            cursor.execute("INSERT INTO osoby_druhy_pojisteni (id_osoby, id_druhu_pojisteni, predmet_pojisteni, hodnota_pojisteni) VALUES (?, ?, ?, ?)", (id_osoby,int(id_pojisteni), predmet_pojisteni, hodnota_pojisteni))
            conn.commit()
            conn.close()
            return ("Vaše pojištění bylo úspěšně přidáno")
      
      @staticmethod
      def vypis_pojisteni(osoba):# vypíše druhy pojištění pro rozhraní 

            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM pojistenci WHERE email = ?", (osoba.get_email(),))
            id_osoby = cursor.fetchone()[0]  

            cursor.execute("SELECT druh_pojisteni, predmet_pojisteni, hodnota_pojisteni FROM osoby_druhy_pojisteni JOIN druhy_pojisteni ON id_druhu_pojisteni = druhy_pojisteni.id WHERE id_osoby = ?", (id_osoby,))
            pojisteni = cursor.fetchall()
            conn.close()

            return '\n'.join(str(pojisteni[polozka]) for polozka in range(len(pojisteni)))

      @staticmethod
      def zmena_udaju_v_datab_pojisteni(osoba):# změna údajů u zdravotního pojištění při změně údajů osoby
            predmet_pojisteni = osoba.get_jmeno() + " " + osoba.get_prijmeni()
            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM pojistenci WHERE email = ?", (osoba.get_email(),))
            id_osoby = cursor.fetchone()[0]
            cursor.execute("UPDATE osoby_druhy_pojisteni SET predmet_pojisteni = ? WHERE id_osoby = ? AND id_druhu_pojisteni = ?", (predmet_pojisteni, id_osoby, 3))
            conn.commit()
            conn.close()

      @staticmethod
      def vypis_vsech_pojistencu():# metoda pro výpis všech pojištěnců z databáze, kteří nejsou admin
            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pojistenci WHERE admin = 'ne' ")
            pojistenci = cursor.fetchall()
            conn.commit()
            conn.close()
            vypis_vsech = ""
            for osoba in pojistenci:
                  nova_osoba = Pojistenec(osoba[1], osoba[2], osoba[3], osoba[4], osoba[5])
                  vypis_vsech += str(nova_osoba) + "\n"
            return vypis_vsech
      
      @staticmethod
      def pridej_admin(nova_osoba): # metoda pro přidání admina
            conn = sqlite3.connect("databaze_projekt.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pojistenci (jmeno, prijmeni, vek, tel_cislo, email, admin) VALUES (?, ?, ?, ?, ?, ?)", (nova_osoba.get_jmeno(), nova_osoba.get_prijmeni(), nova_osoba.get_vek(), nova_osoba.get_tel_cislo(), nova_osoba.get_email(), "ano"))
            conn.commit()
            cursor.close()
            conn.close()
            return f"Admin {nova_osoba.kratky_popis()} byl vytvořen"
      