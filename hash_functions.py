import hashlib
import os

def create_salt(length=16): #salt--> stringa casuale e unica da associare ad una password prima dell'hashing
    """Genera un salt crittograficamente sicuro di una data lunghezza."""
    return os.urandom(length).hex() # sorgente di casualità crittograficamente sicura del sistema operativo 

def hash_password_salted(password, salt=None):
    """
    Esegue l'hashing di una password usando SHA256 con un salt.
    Se non viene fornito un salt, ne genera uno nuovo.
    Restituisce una tupla (hash, salt).
    """
    if salt is None:
        salt = create_salt()
    
    # La password e il salt devono essere convertiti in bytes
    password_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    
    # Concateniamo password e salt prima dell'hashing
    salted_password_bytes = password_bytes + salt_bytes
    
    # Usiamo SHA256 (una funzione di hash robusta)
    hashed_password = hashlib.sha256(salted_password_bytes).hexdigest()
    
    return hashed_password, salt

def verify_password_salted(password, stored_hash, stored_salt):
    """
    Verifica se una password corrisponde a un hash memorizzato, usando il salt corretto.
    """
    hashed_input_password, _ = hash_password_salted(password, stored_salt)
    return hashed_input_password == stored_hash

# Esempio di funzione di hash molto semplificata (solo a scopo didattico, NON sicura)
def simple_xor_hash(text):
    """
    Una funzione di hash molto semplice basata su XOR per dimostrazione.
    Funzioni come questa sono facili da invertire e soggette a collisioni
    """
    hash_value = 0
    for char in text:
        hash_value ^= ord(char)
        hash_value = (hash_value * 31) & 0xFFFFFFFF  # Moltiplicazione e maschera per tenere il valore gestibile
    return hex(hash_value)

if __name__ == "__main__":
    # Esempio di utilizzo delle funzioni di hash
    pwd1 = "password123"
    pwd2 = "secure_pwd"
    
    print(f"Password da hasare: '{pwd1}'")
    h1, s1 = hash_password_salted(pwd1)
    print(f"Hash con salt: {h1}, Salt: {s1}")
    print(f"Verifica '{pwd1}': {verify_password_salted(pwd1, h1, s1)}")
    print(f"Verifica 'sbagliata': {verify_password_salted('wrong_pwd', h1, s1)}")

    print(f"\nPassword da hasare: '{pwd2}'")
    h2, s2 = hash_password_salted(pwd2)
    print(f"Hash con salt: {h2}, Salt: {s2}")

    print("\nEsempio di hash semplice (solo didattico):")
    print(f"'{pwd1}' -> {simple_xor_hash(pwd1)}")
    print(f"'hello' -> {simple_xor_hash('hello')}")
    print(f"'world' -> {simple_xor_hash('world')}")