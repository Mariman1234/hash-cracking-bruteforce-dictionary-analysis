import itertools
import time
import os
from hash_functions import hash_password_salted, verify_password_salted #Senza decifrare l'hash, questa funzione permette all'attaccante di verificare se un tentativo di password è corretto. L'attacco è essenzialmente un ciclo continuo di chiamate a questa funzione.

def run_brute_force_attack(hashed_users_to_attack, char_set, max_len):
    """
    Tenta un attacco brute-force contro un elenco di hash di password.
    hashed_users_to_attack: Lista di {'username', 'hash', 'salt'}
    char_set: Set di caratteri da usare (es. "abc" o "abcdefghijklmnopqrstuvwxyz")
    max_len: Lunghezza massima delle password da provare
    """
    print(f"\nAvvio attacco Brute-Force (caratteri: '{char_set}', lunghezza max: {max_len})")
    found_passwords = {}
    start_time = time.time()
    
    for user_data in hashed_users_to_attack:
        username = user_data['username']
        target_hash = user_data['hash']
        target_salt = user_data['salt']
        
        print(f"Tentativo di cracking per l'utente '{username}' (hash: {target_hash[:10]}...)")
        
        for length in range(1, max_len + 1):
            for attempt_tuple in itertools.product(char_set, repeat=length): #Esempio: Se char_set="ab" e length=3, genera aaa, aab, aba, abb, baa, ecc.
                attempt_password = "".join(attempt_tuple)
                
                if verify_password_salted(attempt_password, target_hash, target_salt):
                    print(f"    [TROVATO!] Password per '{username}': '{attempt_password}'")
                    found_passwords[username] = attempt_password
                    break # Esce dal ciclo di itertools.product
            if username in found_passwords:
                break # Esce dal ciclo delle lunghezze
        if username not in found_passwords:
            print(f"Password per '{username}' non trovata entro i parametri specificati.")
            
    end_time = time.time()
    print(f"Attacco Brute-Force completato in {end_time - start_time:.2f} secondi.")
    print("Password trovate:", found_passwords)
    return found_passwords

def run_dictionary_attack(hashed_users_to_attack, dictionary_file):
    """
    Tenta un attacco dictionary-based contro un elenco di hash di password.
    hashed_users_to_attack: Lista di {'username', 'hash', 'salt'}
    dictionary_file: Percorso al file del dizionario
    """
    print(f"\nAvvio attacco Dictionary-Based usando '{dictionary_file}'")
    found_passwords = {}
    start_time = time.time()

    # Carica le password dal dizionario
    try:
        with open(dictionary_file, "r", encoding="utf-8", errors="ignore") as f:
            dictionary_words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Errore: Il file del dizionario '{dictionary_file}' non è stato trovato.")
        return {}
    except Exception as e:
        print(f"Errore durante la lettura del dizionario: {e}")
        return {}
        
    print(f"Caricate {len(dictionary_words)} parole dal dizionario.")

    for user_data in hashed_users_to_attack:
        username = user_data['username']
        target_hash = user_data['hash']
        target_salt = user_data['salt']
        
        print(f"Tentativo di cracking per l'utente '{username}' (hash: {target_hash[:10]}...)")
        
        found = False
        for word in dictionary_words:
            # Prova la parola così com'è
            if verify_password_salted(word, target_hash, target_salt):
                print(f"[TROVATO!] Password per '{username}': '{word}'")
                found_passwords[username] = word
                found = True
                break
            
        if not found:
            print(f"Password per '{username}' non trovata nel dizionario.")
            
    end_time = time.time()
    print(f"Attacco Dictionary-Based completato in {end_time - start_time:.2f} secondi.")
    print("Password trovate:", found_passwords)
    return found_passwords

if __name__ == "__main__":
    # Esempio di utilizzo (richiede un file data/users.txt e data/dictionary.txt)
    from password_manager import create_hashed_passwords_file, load_hashed_passwords
    
    # Assicurati che i file esistano per il test
    if not os.path.exists("data"):
        os.makedirs("data")
    create_hashed_passwords_file("data/test_users_for_attacks.txt")
    with open("data/test_dictionary.txt", "w") as f:
        f.write("password\n")
        f.write("123456\n")
        f.write("qwerty\n")
        f.write("iloveunicorns\n")

    test_users = load_hashed_passwords("data/test_users_for_attacks.txt")

    if test_users:
        print("\n--- TEST BRUTE-FORCE ---")
        # Trova un utente con una password "debole" per il test rapido del brute-force
        user_to_brute_force = next((u for u in test_users if u['username'] == 'bob'), None)
        if user_to_brute_force:
            print(f"Testando brute-force su '{user_to_brute_force['username']}' (password originale 123456)")
            run_brute_force_attack([user_to_brute_force], char_set="0123456789", max_len=6)
        else:
            print("Utente 'bob' non trovato per test brute-force.")


        # Test Dictionary-Based
        print("\n--- TEST DICTIONARY-BASED ---")
        run_dictionary_attack(test_users, "data/test_dictionary.txt")
    
    # Pulizia
    os.remove("data/test_users_for_attacks.txt")
    os.remove("data/test_dictionary.txt")
    print("\nFile di test rimossi.")