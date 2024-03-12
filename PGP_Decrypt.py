import os
import gnupg

# Variables
passphrase = "[REDACTED]"
gpg_exe_file_path = r"C:\Program Files (x86)\GnuPG\bin\gpg.exe"

# Define directories
directories = [
    "AIR", "BROLV", "CRW", "FTL", "LBP", "MDL", "MKT", "OLV", "SMS", "YYCBREW"
]

print("Decryption under way...")

# Initialize the gnupg.GPG object
gpg = gnupg.GPG(gpgbinary=gpg_exe_file_path)

def decrypt_directory(encrypted_dir, decrypted_dir):
    for file in os.listdir(encrypted_dir):
        if file.endswith(".pgp"):  # Only process PGP encrypted files
            file_path = os.path.join(encrypted_dir, file)
            decrypted_data = gpg.decrypt_file(file_path, passphrase=passphrase)

            # Remove existing decrypted file with the same name
            decrypted_file_path = os.path.join(decrypted_dir, os.path.splitext(file)[0])
            if os.path.exists(decrypted_file_path):
                try:
                    os.remove(decrypted_file_path)
                    print(f"Removed existing decrypted file: {decrypted_file_path}")
                except PermissionError:
                    print(f"ATTEMPT TO DELETE EXISTING DECRYPTED FILE FAILED.\nCould not remove {decrypted_file_path}.\nIt may be in use.")
                    continue

            # Remove the PGP encrypted file
            try:
                os.remove(file_path)
                print(f"Removed PGP encrypted file: {file_path}")
            except PermissionError:
                print(f"ATTEMPT TO DELETE PGP ENCRYPTED FILE FAILED.\nCould not remove {file_path}.\nIt may be in use.")
                continue

            # Write the newly decrypted data to the file
            with open(decrypted_file_path, 'wb') as df:
                df.write(decrypted_data.data)

            if decrypted_data.ok:
                print(f"Decryption in {decrypted_dir} successful.")
            else:
                print("Decryption failed.")
                print(decrypted_data.stderr)

# Iterate over directories
for directory in directories:
    encrypted_dir = rf"\\bbcfilesrv\C$\Users\ceridian\Documents\{directory}"
    decrypted_dir = rf"\\bbcfilesrv\C$\Users\ceridian\Documents\{directory}"
    
    print(f"\nDecryption in directory {directory} complete.")
    decrypt_directory(encrypted_dir, decrypted_dir)

print("\nEnd of decryption process.")
