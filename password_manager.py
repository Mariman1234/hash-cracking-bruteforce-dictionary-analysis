from hash_functions import hash_password_salted
import os

def create_hashed_passwords_file(filename="data/users.txt"):
    """
    Genera un set di username e password (alcune deboli, alcune forti)
    e le hasha con salt, salvandole in un file.
    Formato: username:hash:salt
    """
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    users_data = [
        ("alice", "password"),
        ("bob", "123456"),
        ("charlie", "qwerty"),
        ("diana", "MySuperSecureP@ssw0rd!2025"),
        ("eve", "iloveunicorns"),
        ("frank", "footballmania"),
        ("grace", "Pa$$w0rd"),
        ("helen", "LongAndComplexPasswordWithManyWordsAndNumbers12345")
    ]

    with open(filename, "w") as f:
        for username, password in users_data:
            hashed_pwd, salt = hash_password_salted(password)
            f.write(f"{username}:{hashed_pwd}:{salt}\n")
    print(f"Generati {len(users_data)} hash di password e salvati in {filename}")

def load_hashed_passwords(filename="data/users.txt"):
    """
    Carica gli hash delle password da un file.
    Restituisce una lista di dizionari, es: [{'username': 'alice', 'hash': '...', 'salt': '...'}]
    """
    hashed_users = []
    if not os.path.exists(filename):
        print(f"File {filename} non trovato. Genera prima gli hash.")
        return hashed_users
    
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) == 3:
                hashed_users.append({
                    'username': parts[0],
                    'hash': parts[1],
                    'salt': parts[2]
                })
            else:
                print(f"Formato riga non valido: {line.strip()}")
    return hashed_users

if __name__ == "__main__":
    # Esempio di utilizzo
    output_file = "data/test_users.txt"
    create_hashed_passwords_file(output_file)
    loaded_users = load_hashed_passwords(output_file)
    print("\nUtenti caricati:")
    for user in loaded_users:
        print(f"  Username: {user['username']}, Hash: {user['hash'][:10]}..., Salt: {user['salt'][:10]}...")
    
    # Pulizia del file di test
    os.remove(output_file)
    print(f"\nFile di test {output_file} rimosso.")