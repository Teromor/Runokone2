'''Alkuperäinen ohjelmointi ja englanninkieliset kommentit: Mehrab Jamee
'''
import random
import sys
import time
from urllib.request import urlopen

def slowprint(s):
    for c in s + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(1./50)

def tervehdysAlkuun():
    slowprint("--Laita klassikot kohtaamaan! Tervetuloa runokokeiluun!--")
    print(" ")
    
print(" ")
tervehdysAlkuun()

def runokone():
    def tokenize_poems(poems):
        # Poistaa numerot, pilkkoo sanat ja palauttaa ne listana
        poems = ''.join([char if char.isalnum() or char.isspace() else ' ' for char in poems])
        return poems.split()
    
    # Lue tiedostot ja käsittele ne tokeneiksi
    poems1 = tokenize_poems(urlopen("https://raw.githubusercontent.com/Teromor/Runokone2/refs/heads/main/kailas_runot.txt").read().decode('utf-8'))
    poems2 = tokenize_poems(urlopen("https://raw.githubusercontent.com/Teromor/Runokone2/refs/heads/main/lonerva_runot.txt").read().decode('utf-8'))
    poems3 = tokenize_poems(urlopen("https://raw.githubusercontent.com/Teromor/Runokone2/refs/heads/main/hellaakoski_runot.txt").read().decode('utf-8'))

    # Käyttäjän valinta runojen lähteistä
    print("Valitse runojen lähteet, valitse yhteensä kaksi:")
    print("1: Uuno Kailas")
    print("2: L.Onerva")
    print("3: Aaro Hellaakoski")
    selected_sources = input("Anna valinnat pilkulla eroteltuna (esim. 1,3): ").split(',')

    selected_poems = []
    if '1' in selected_sources:
        selected_poems += poems1
    if '2' in selected_sources:
        selected_poems += poems2
    if '3' in selected_sources:
        selected_poems += poems3

    poems = selected_poems

    # Kysy käyttäjältä halutun runon pituus
    while True:
        try:
            count = int(input("Anna numero 20 ja 200 väliltä: "))
        except ValueError:
            print("En tunnistanyt antamaasi syötettä. Yritä uudestaan ja anna tällä kertaa jokin numero 20-200 välillä kiitos!")
            continue
        if count <= 19 or count > 200:
            print("Anna numero 20:n ja 200:n väliltä")
            continue
        else:
            break

    # Luo sanakirja ketjuttamista varten 3-grammin perusteella
    chain: dict[tuple[str, str, str], list[str]] = {}
    for i in range(len(poems) - 3):  # Käy läpi kaikki mahdolliset 3-grammit
        key = (poems[i], poems[i + 1], poems[i + 2])  # Kolmen sanan yhdistelmä
        next_word = poems[i + 3]  # Seuraava sana
        if key in chain:
            chain[key].append(next_word)
        else:
            chain[key] = [next_word]

    # Generoi runo Markovin ketjulla
    word1, word2, word3 = random.choice(list(chain.keys()))  # Satunnainen 3-grammi aloitukseen
    message = ' '.join([word1.capitalize(), word2, word3])  # Aloita runo 3-grammilla
    seen_keys = set()  # Pidetään kirjaa aiemmista avaimista

    while len(message.split(' ')) < count:
        key = (word1, word2, word3)  # Nykyinen 3-grammi
        if key in seen_keys:  # Jos avain on jo nähty, valitaan uusi satunnainen avain
            word1, word2, word3 = random.choice(list(chain.keys()))
            continue
        seen_keys.add(key)  # Merkitään avain käytetyksi
        
        if key in chain and chain[key]:
            next_word = random.choice(chain[key])  # Valitse seuraava sana
            message += ' ' + next_word
            word1, word2, word3 = word2, word3, next_word  # Päivitä seuraava 3-grammi
        else:
            word1, word2, word3 = random.choice(list(chain.keys()))  # Ketju jatkuu satunnaisesti

    # Formatointi: Lisää rivivälit ja sisennykset
    formatted_message = ''
    for word in message.split(' '):
        if word.istitle():  # Jos sana alkaa isolla kirjaimella
            formatted_message += '\n' * random.randint(1, 3)  # Satunnainen riviväli
            formatted_message += ' ' * random.randint(0, 3)  # Satunnainen sisennys
        formatted_message += word + ' '

    slowprint("\n" + formatted_message.strip())


    check = input("Haluatko kokeilla uudestaan? Paina K saadaksesi uuden runon:")
    if check.upper() == "K":
        runokone()
    else:
        print(" ")
        print("Kiitos runokoneen käytöstä!")
    
runokone()