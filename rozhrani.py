import os
import sys
from pojistenci import Pojistenec, EvidencePojistencu
import getpass
import time

class Rozhranistatic:

    @staticmethod
    def hlavicka():# metoda pro výpis hlavičky 
        return f"""
{30* "-"}\n
Evidence pojištěných\n  
{30*"-"}
        """
    
    @staticmethod
    def zadej_udaje_registrace(): # metoda pro zadání osobních údajů při registraci - vrací slovník
        jmeno = input("Zadejte křestní jméno:")
        prijmeni = input("zadejte příjmení:")
        vek = input("Zadejte věk:")
        tel_cislo = input("Zadejte tel. číslo:")
        email = input("Zadejte email:")
        udaje = {"jmeno": jmeno, "prijmeni":prijmeni, "vek":vek, "tel_cislo":tel_cislo, "email":email}
        return udaje
    
    @staticmethod
    def zadani_hesla_dokonceni_registrace(udaje_osoby_dict): # metoda pro zadání a kontrolu hesla a zároveň vytvoření objektu Pojistenci
        #! Rozdělit metodu
        from kontroly import Kontroly
        heslo = EvidencePojistencu.hash_hesla(getpass.getpass("Zadejte heslo(z důvodu bezpečnosti se heslo nezobrazuje):"))
        kontrola_hesla = EvidencePojistencu.hash_hesla(getpass.getpass("Zadejte heslo pro kontrolu:"))
        heslo = Kontroly.registrace_hesla(heslo, kontrola_hesla)

        nova_osoba = Pojistenec(udaje_osoby_dict["jmeno"], udaje_osoby_dict["prijmeni"], udaje_osoby_dict["vek"], udaje_osoby_dict["tel_cislo"], udaje_osoby_dict["email"])

        EvidencePojistencu.vlozeni_do_databaze(nova_osoba)
        EvidencePojistencu.vlozeni_do_databaze_hesel(heslo)

        return nova_osoba
    

    @staticmethod
    def vyber_udaj_na_opravu(nova_osoba):# výpis osobních údajů na opravu
        return f"""Který údaj chcete upravit:\n
        1 - Jméno:{nova_osoba.get_jmeno()}\n
        2 - Příjmení:{nova_osoba.get_prijmeni()}\n
        3 - Věk:{nova_osoba.get_vek()}\n
        4 - Telefonní číslo: {nova_osoba.get_tel_cislo()}\n
        5 - Heslo: #########
        """
    
    @staticmethod
    def vypis_osobni_udaje(osoba):# výpis osobních údajů 
        return f"""Vaše osobní údaje:\n
        Jméno:{osoba.get_jmeno()}\n
        Příjmení:{osoba.get_prijmeni()}\n
        Věk:{osoba.get_vek()}\n
        Telefonní číslo: {osoba.get_tel_cislo()}\n
        Email: {osoba.get_email()}
        """
    
    @staticmethod
    def menu(): # menu pro pojištěnce
        return """Vyber si akci: \n
        1 - Přidat pojištění \n
        2 - Vaše pojištění \n
        3 - Upravit osobní údaje \n
        4 - Zobrazit osobní údaje \n
        5 - Ukončit program"
    """
    @staticmethod
    def menu_admin():# menu pro admina
        return """Vyber si akci: \n
        1 - Vypsat všechny pojištěnce \n
        2 - Upravit pojištěnce \n
        3 - Přidat dalšího admin \n
        4 - Ukončit program"
    """
    @staticmethod
    def vyber_pojisteni_menu(): # výpis druhů pojištění 
        seznam_pojisteni = EvidencePojistencu.vrat_druhy_pojisteni()
        menu = "Které pojištění chcete přidat? \n"
        for index in range(len(seznam_pojisteni)):
                menu += f"{index + 1}-{seznam_pojisteni[index]}\n"
        return menu
    
    @staticmethod
    def vycisti_obrazovku():
        import os as _os
        _os.system('cls' if _os.name == 'nt' else 'clear')
    

    @staticmethod
    def prihlaseni():
        return """Zadejte akci, kterou chcete vykonat\n
        1 - Přihlášení\n
        2 - Registrace nového uživatele
        """
    
    @staticmethod
    def restart_program():
    # Restart programu po instalaci knihovny
        python = sys.executable
        os.execv(python, ["main.py"] + sys.argv)


    @staticmethod
    def hlavicka_s_uzivatelem(osoba): # hlavička včetně osobních údajů přihlášeného
        return f"""{30* "-"}\n
Evidence pojištěných\n  
Profil: {osoba}\n  
{30*"-"}
    """

    @staticmethod
    def ukonceni_programu():# animace pri ukončení programu
        for krok in range(3):
            
            print("Ukončuji program.")
            time.sleep(0.2)
            Rozhranistatic.vycisti_obrazovku()
            print("Ukončuji program..")
            time.sleep(0.2)
            Rozhranistatic.vycisti_obrazovku()
            print("Ukončuji program...")
            time.sleep(0.2)
            Rozhranistatic.vycisti_obrazovku()
        return exit()
    
    @staticmethod
    def zmena_udaje(vyber: str, nova_osoba):# metoda pro změnu údajů jak ve třídě, tak v databázi 

          if vyber == "1":# změna jména
                novy_udaj = input("Zadejte jméno:")
                nova_osoba.jmeno = novy_udaj
                sloupec = "jmeno"
                EvidencePojistencu.zmena_udaju_v_datab(nova_osoba.get_email(), sloupec, novy_udaj)
                EvidencePojistencu.zmena_udaju_v_datab_pojisteni(nova_osoba)#změna se provede zároveň i v tabulce u zdravotního pojištění

          elif vyber == "2":# změna příjmení
                novy_udaj = input("Zadejte příjmení:")
                nova_osoba.prijmeni = novy_udaj
                sloupec = "prijmeni"
                EvidencePojistencu.zmena_udaju_v_datab(nova_osoba.get_email(), sloupec, novy_udaj)
                EvidencePojistencu.zmena_udaju_v_datab_pojisteni(nova_osoba)#změna se provede zároveň i v tabulce u zdravotního pojištění

          elif vyber == "3":# změna věku
                novy_udaj = input("Zadejte věk:")
                nova_osoba.vek = novy_udaj
                sloupec = "vek"
                EvidencePojistencu.zmena_udaju_v_datab(nova_osoba.get_email(), sloupec, novy_udaj)

          elif vyber == "4":# změna tel. čísla
                novy_udaj = input("Zadejte telefonní číslo:")
                nova_osoba.tel_cislo = novy_udaj
                sloupec = "tel_cislo"
                EvidencePojistencu.zmena_udaju_v_datab(nova_osoba.get_email(), sloupec, novy_udaj)

          elif vyber == "5":# změna hesla
                novy_udaj = EvidencePojistencu.hash_hesla(getpass.getpass("Zadejte nové heslo(z důvodu bezpečnosti se heslo nezobrazuje):"))
                EvidencePojistencu.zmena_hesla(nova_osoba.get_email(), novy_udaj)

          return ("Váš udaj byl úspěšně změněn")
    
    @staticmethod
    def vyber_druh_pojisteni()