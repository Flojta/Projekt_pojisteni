import sqlite3
import getpass
import subprocess
from pojistenci import EvidencePojistencu
from rozhrani import Rozhranistatic
import time

class Kontroly:


         

    @staticmethod
    def databaze_email(email):
        conn = sqlite3.connect("databaze_projekt.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pojistenci WHERE email = ?", (email,))
        vysledek = cursor.fetchone()
        cursor.close()
        conn.close()

        if vysledek:
            return False
        return True
    
    @staticmethod
    def registrace_hesla(heslo, kontrola_hesla):
        while heslo != kontrola_hesla:
            heslo = EvidencePojistencu.hash_hesla(heslo = getpass.getpass("Hesla se neshodují, prosím zadejte heslo znovu:"))
            kontrola_hesla = EvidencePojistencu.hash_hesla(heslo = getpass.getpass("Zadejte heslo pro kontrolu:"))
        return heslo


    @staticmethod
    def install_knihoven(seznam_knihoven):

        for knihovna in seznam_knihoven:

            print(f"Instalace knihovny {knihovna} probíhá...")

            try:
                subprocess.check_call(["pip", "install", knihovna])
                print("Knihovna byla úspěšně nainstalována.")
                time.sleep(2)

            except subprocess.CalledProcessError:
                print("Instalace selhala. Ujistěte se, že máte nainstalovaný správce balíčků pip.")
                print(input("Stisknutím ENTER ukončíte program..."))
                exit()

            except Exception as e:
                print("Nastala chyba při instalaci knihovny:", e)
                print(input("Stisknutím ENTER ukončíte program..."))
                exit()

           

            

    
