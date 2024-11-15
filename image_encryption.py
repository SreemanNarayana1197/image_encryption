import os
from cryptography.fernet import Fernet
from PIL import Image
import io

class ImageEncryptor:
    def __init__(self):
        # Generate a key and instantiate a Fernet cipher
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_image(self, image_path):
        """Encrypt the image at the given path."""
        try:
            with open(image_path, 'rb') as file:
                image_data = file.read()
            # Encrypt the image data
            encrypted_data = self.cipher.encrypt(image_data)
            return encrypted_data
        except Exception as e:
            print(f"Error encrypting image: {e}")
            return None

    def decrypt_image(self, encrypted_data, output_path):
        """Decrypt the encrypted data and save it as an image."""
        try:
            decrypted_data = self.cipher.decrypt(encrypted_data)
            # Save the decrypted image
            with open(output_path, 'wb') as file:
                file.write(decrypted_data)
            print(f"Image decrypted and saved as '{output_path}'")
        except Exception as e:
            print(f"Error decrypting image: {e}")

    def save_key(self, key_path):
        """Save the encryption key to a file."""
        with open(key_path, 'wb') as key_file:
            key_file.write(self.key)

    def load_key(self, key_path):
        """Load the encryption key from a file."""
        try:
            with open(key_path, 'rb') as key_file:
                self.key = key_file.read()
            self.cipher = Fernet(self.key)
        except Exception as e:
            print(f"Error loading key: {e}")

def main():
    encryptor = ImageEncryptor()

    action = input("Do you want to (e)ncrypt or (d)ecrypt an image? ").lower()
    if action == 'e':
        image_path = input("Enter the path of the image to encrypt: ")
        encrypted_data = encryptor.encrypt_image(image_path)
        
        if encrypted_data:
            with open('encrypted_image.bin', 'wb') as file:
                file.write(encrypted_data)
            encryptor.save_key('encryption_key.key')
            print("Image encrypted and saved as 'encrypted_image.bin'")
            print("Encryption key saved as 'encryption_key.key'")
        
    elif action == 'd':
        try:
            with open('encrypted_image.bin', 'rb') as file:
                encrypted_data = file.read()
            output_path = input("Enter the path to save the decrypted image: ")
            encryptor.load_key('encryption_key.key')
            encryptor.decrypt_image(encrypted_data, output_path)
        except FileNotFoundError:
            print("Error: Encrypted image file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()