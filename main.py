import os
from password_manager import create_hashed_passwords_file, load_hashed_passwords
from attack_simulations import run_brute_force_attack, run_dictionary_attack

def main():
    print("--- Progetto Sicurezza dell'Informazione M: Hash e Attacchi ---")

    # --- Fase 1: Generazione Hash di Password ---
    print("\n[Fase 1] Generazione di hash di password")
    output_file_users = "data/users.txt"
    create_hashed_passwords_file(output_file_users)
    print(f"File degli hash delle password creato: {output_file_users}")

    # --- Fase 1.5 - Creazione file per John The Ripper ---
    print("\n[Fase 1.5] Creazione file di input per John the Ripper")
    input_file_jtr = "data/jtr_input.txt"
    try:
        with open(output_file_users, "r") as f_in, open(input_file_jtr, "w") as f_out:
            for line in f_in:
                parts = line.strip().split(':')
                if len(parts) == 3:
                    # Formato JTR: username:hash$salt
                    username, hash_val, salt_val = parts
                    f_out.write(f"{username}:{hash_val}${salt_val}\n")
        print(f"File per JtR creato: {input_file_jtr}")
    except Exception as e:
        print(f"Errore durante la creazione del file JtR: {e}")

    # Carica gli hash per gli attacchi successivi
    hashed_users = load_hashed_passwords(output_file_users)
    if not hashed_users:
        print("Nessun utente caricato, impossibile procedere con gli attacchi.")
        return

    # --- Fase 2: Simulazione Attacchi Brute-Force ---
    print("\n[Fase 2] Avvio della simulazione di attacco Brute-Force...")
    print("Nota: L'attacco brute-force su password lunghe può richiedere molto tempo.")
    
    response = input("Vuoi eseguire un attacco brute-force (s/n)? (Potrebbe essere lungo): ")
    if response == 's':
        run_brute_force_attack(hashed_users, char_set="123456", max_len=6) # condizioni molto limitanti pilotate per il risultato in output
        #run_brute_force_attack(hashed_users, char_set="abcdefghijklmnopqrstuvwxyz0123456789", max_len=5) --> impiega molto 872.09 secondi


    # --- Fase 3: Simulazione Attacchi Dictionary-Based ---
    print("\n[Fase 3] Avvio della simulazione di attacco Dictionary-Based...")
    dictionary_file = "data/dictionary.txt"
    if not os.path.exists(dictionary_file):
        print(f"Errore: File del dizionario non trovato in {dictionary_file}.")
    else:
        run_dictionary_attack(hashed_users, dictionary_file)

    # --- Fase 4: Preparazione per John the Ripper (Istruzioni Manuali) ---
    print("\n[Fase 4] Preparazione per John the Ripper:")
    print(f"Gli hash delle password sono stati salvati in {output_file_users}.")
    print("Puoi usare questo file come input per John the Ripper. Ad esempio:")
    print(f"   john --wordlist={dictionary_file} {output_file_users}")
    print(f"   john --incremental {output_file_users} (per attacco brute-force)")

if __name__ == "__main__":
    main()