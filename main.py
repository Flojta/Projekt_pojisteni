from pojistenci import Pojistenec, EvidencePojistencu
from rozhrani import Rozhranistatic
from kontroly import Kontroly
import subprocess
import getpass
import time

login = True
menu = True
nova_osoba = None
install_knihoven = True
knihovna_email = True
knihovna_getpass3 = True
knihovny_pro_install = []


#-------------------------------------------------------------------------------------------------------------------------------------kontrola knihoven(0)
try:

    from validate_email import validate_email # kód zkusí importovat knihovnu validate_email

except ImportError:

    knihovna_email = "validate_email" # v případě chybějící knihovny se přepíše hodnota na jméno knihovny pro komunikaci s CMD
    knihovny_pro_install.append(knihovna_email) 
   #string se uloží do pole (v případě využití více knihoven se názvy jednotlivě pomocí for in cyklu přes příkaz pip nainstalují)
    
if knihovna_email == "validate_email": # upozornění uživatele na instalaci knihovny
    print("Pro spuštění programu je potřeba nainstalovat knihovnu validate_email.")
    volba = input("Přejete si pokračovat (ano/ne)? :")

    if volba == "ano":
        Rozhranistatic.vycisti_obrazovku()
        print(Kontroly.install_knihoven(knihovny_pro_install)) #---instalace knihoven
        Rozhranistatic.restart_program()#------restart kvůli instalaci, bez restartu nefungují právě nainstalované knihovny

    else:
        print("Bez knihovny program nelze spustit.")# ----- chybné zadání
        print(input("Stiskněte ENTER pro ukončení programu"))
        exit()
Rozhranistatic.vycisti_obrazovku()
#-------------------------------------------------------------------------------------------------------------------------------------login(1)
while login == True: 

    print(Rozhranistatic.hlavicka())
    print(Rozhranistatic.prihlaseni())


    akce_login = input("Vyberte možnost:")
    


    if akce_login == "1": #-------------------------------------Přihlášení
        email = input("Zadejte přihlašovací email:")
        heslo = EvidencePojistencu.hash_hesla(getpass.getpass("Zadejte heslo(z důvodu bezpečnosti se heslo nezobrazuje):"))

        if EvidencePojistencu().kontrola_prihlaseni(email, heslo): #----------kontrola zadaných údajů v databázi
            print("Přihlášení proběhlo v pořádku.")
            nova_osoba = EvidencePojistencu().vytvor_objekt_z_datab(email) # vytvoření objektu z databáze
            time.sleep(2)
            login = False
        
        else: 
            print("Nesprávný email nebo heslo") 
            time.sleep(2)
            Rozhranistatic.vycisti_obrazovku()

    elif akce_login == "2": #-----------------------------------Registrace

        osobni_udaje = Rozhranistatic.zadej_udaje_registrace() # zadání základních údajů až po email

        while validate_email(osobni_udaje["email"]) == False: #cyklus pro případ, kdyby zadaný email měl špatný formát
            print("Zadaný email nemá správný formát")
            osobni_udaje["email"] = input("Zadejte email znovu:")

        if Kontroly.databaze_email(osobni_udaje["email"]) == True: #zkontroluje, jestli se v databázi již nenachází stejný email

            nova_osoba = Rozhranistatic.zadani_hesla_dokonceni_registrace(osobni_udaje) # metoda pro zadání hesla přes double kontrolu a vytvoření objektu
            print(f"Účet pro osobu {nova_osoba.kratky_popis()} byl vytvořen")
            time.sleep(2)
            login = False


        else:
            print("Zadaný email již existuje") # chybné zadání
            print("Proveďte přihlášení, nebo se registrujte s jiným emailem.")
            time.sleep(2)
            Rozhranistatic.vycisti_obrazovku()
            akce_login = ""
        
    else:
        print("Špatné zadání, zkuste to znovu")
        time.sleep(1)
        Rozhranistatic.vycisti_obrazovku()
#-------------------------------------------------------------------------------------------------------------------------------------menu(2)
Rozhranistatic.vycisti_obrazovku()
admin = EvidencePojistencu().kontrola_admin(nova_osoba.get_email()) #kontrola, zda je přihlášená osoba admin
while menu == True:

    print(Rozhranistatic.hlavicka_s_uzivatelem(nova_osoba.kratky_popis()))    
    if admin == "ne": #----------------------------------------------------------------------------------------------menu uživatele
        print(Rozhranistatic.menu())
        akce_menu = input("Vyberte možnost:")


        if akce_menu == "1": #Možnost přidání pojištění pro osobu
            Rozhranistatic.vycisti_obrazovku()
            print(Rozhranistatic.vyber_pojisteni_menu())
            vyber_pojisteni = input("Vyberte možnost:")

            if vyber_pojisteni in ["1", "2", "3"]:
                hodnoty_pojisteni = Rozhranistatic.vyber_druh_pojisteni(vyber_pojisteni, nova_osoba)
                print(EvidencePojistencu().pridej_druh_pojisteni(hodnoty_pojisteni["id_pojisteni"], hodnoty_pojisteni["predmet_pojisteni"], hodnoty_pojisteni["hodnota_pojisteni"], nova_osoba ))
                time.sleep(1)
                Rozhranistatic.vycisti_obrazovku()
            else:
                print("Špatné zadání")
                Rozhranistatic.vycisti_obrazovku()

        if akce_menu =="2": # Vypíše všechny pojištění přihlášené osoby

            Rozhranistatic.vycisti_obrazovku()
            print("Vaše pojištění:\n")
            print("Druh pojištění - Předmět pojištění - Hodnota pojištění\n")
            print(EvidencePojistencu().vypis_pojisteni(nova_osoba))
            print(input("Zpět (Stisknutím ENTER)"))
            Rozhranistatic.vycisti_obrazovku()

        elif akce_menu == "3": #Změna údajů osoby


            Rozhranistatic.vycisti_obrazovku()
            print(Rozhranistatic.vyber_udaj_na_opravu(nova_osoba))
            vyber_udaj = input("Vyberte možnost:")

            if vyber_udaj in ["1", "2", "3", "4", "5"]:
                print(Rozhranistatic.zmena_udaje(vyber_udaj, nova_osoba))
                time.sleep(1)
                Rozhranistatic.vycisti_obrazovku()

            else:
                print("Špatné zadání...")
                Rozhranistatic.vycisti_obrazovku()
            
        elif akce_menu == "4": # Vypíše osobní údaje 
            Rozhranistatic.vycisti_obrazovku()
            print(Rozhranistatic.vypis_osobni_udaje(nova_osoba))
            print(input("Zpět (Stisknutím ENTER)"))
            Rozhranistatic.vycisti_obrazovku()

        elif akce_menu == "5":
            Rozhranistatic.ukonceni_programu()
        else:
            print("Špatné zadání, zkuste to znovu..")
            Rozhranistatic.vycisti_obrazovku()


    else:
        print(Rozhranistatic.menu_admin())#-----------------------------------------------------------------menu admin
        akce_menu = input("Vyberte možnost:")

        if akce_menu == "1": # vypíše všechny pojištěnce z databáze, co nejsou admin 

            Rozhranistatic.vycisti_obrazovku()
            print(EvidencePojistencu().vypis_vsech_pojistencu())
            print(input("Zpět (Stisknutím ENTER)"))
            Rozhranistatic.vycisti_obrazovku()
            

        if akce_menu =="2": # možnost úpravy osobních údajů u kterékoli osoby

            email_osoby = input("Zadejte email osoby, u které chcete upravit údaje: ")
            osoba_na_zmenu = Kontroly.databaze_email(email_osoby) #nejprve se zadá email osoby, kterou chceš změnit
                                                                  #přes email se vyhledá zbytek údajů v databázi

            if osoba_na_zmenu == True: # email nenalezen

                print("Zadaná osoba není v databázi")
                print(input("Zpět (Stisknutím ENTER)"))

            else:

                osoba_na_zmenu = EvidencePojistencu().vytvor_objekt_z_datab(email_osoby)
                print(Rozhranistatic.vyber_udaj_na_opravu(osoba_na_zmenu))
                vyber_udaj = input("Vyberte možnost:")

                if vyber_udaj in ["1", "2", "3", "4", "5"]: 

                    print(Rozhranistatic.zmena_udaje(vyber_udaj, osoba_na_zmenu))
                    time.sleep(1)
                    Rozhranistatic.vycisti_obrazovku()

                else:

                    print("Špatné zadání...")

        elif akce_menu == "3": #možnost přidání dalšího administrátora

            print("Zadejte údaje dalšího administrátora:\n")
            udaje_admin = Rozhranistatic.zadej_udaje_registrace()
            novy_admin = Rozhranistatic.zadani_hesla_dokonceni_registrace(udaje_admin) 
            print(EvidencePojistencu().pridej_admin(novy_admin))
            time.sleep(1)
            Rozhranistatic.vycisti_obrazovku()

        elif akce_menu == "4": # konec programu

            Rozhranistatic.vycisti_obrazovku()
            Rozhranistatic.ukonceni_programu()
            
        else:

            print("Špatné zadání, zkuste to znovu..")
            Rozhranistatic.vycisti_obrazovku()