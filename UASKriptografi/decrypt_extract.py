"""
Program Dekripsi Caesar Cipher + Ekstraksi Steganografi LSB
Kelompok 1: Caesar Cipher dengan shift 7 + Steganografi LSB
"""

from PIL import Image
import numpy as np
import os


def extract_lsb(image_path):
    """
    Ekstrak pesan dari gambar stego menggunakan LSB
    """
    print("\n=== PROSES EKSTRAKSI LSB ===")
    
    
    
    img = Image.open(image_path)
    img_array = np.array(img)
    
    print(f"Gambar stego: {image_path}")
    print(f"Ukuran gambar: {img_array.shape}")
    print(f"Dimensi: {img.size[0]} x {img.size[1]} pixels")
    
    flat_array = img_array.flatten()
    
    print("\n=== MEMBACA HEADER ===")
    print("Mengekstrak 32 bit pertama untuk mendapatkan panjang pesan...")
    
    # Ekstrak 32 bit pertama untuk mendapatkan panjang pesan
    length_binary = ""
    for i in range(32):
        length_binary += str(flat_array[i] & 1)
    
    message_length = int(length_binary, 2)
    print(f"Header (32 bit): {length_binary}")
    print(f"Panjang pesan: {message_length} bit")
    
    print("\n=== EKSTRAKSI PESAN ===")
    print("Mengekstrak LSB dari pixel...")
    
    # Ekstrak pesan
    binary_message = ""
    print("\nContoh ekstraksi (10 bit pertama):")
    for i in range(32, 32 + min(10, message_length)):
        pixel_value = flat_array[i]
        bit = pixel_value & 1
        binary_message += str(bit)
        print(f"  Bit {i-31}: Pixel[{i}] = {pixel_value:08b} -> LSB = '{bit}'")
    
    # Ekstrak sisa bit
    for i in range(32 + 10, 32 + message_length):
        binary_message += str(flat_array[i] & 1)
    
    print(f"\nBinary lengkap ({len(binary_message)} bit):")
    print(f"{binary_message[:64]}..." if len(binary_message) > 64 else binary_message)
    
    print("\n=== KONVERSI BINARY KE TEKS ===")
    
    # Konversi binary ke teks
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            char = chr(int(byte, 2))
            message += char
            print(f"  Byte {i//8 + 1}: {byte} -> ASCII {int(byte, 2)} -> '{char}'")
    
    print(f"\nCiphertext hasil ekstraksi: {message}")
    return message


def caesar_cipher_decrypt(ciphertext, shift=7):
    """
    Dekripsi Caesar Cipher dengan shift 7
    """
    decrypted = ""
    
    print("\n=== PROSES DEKRIPSI CAESAR CIPHER ===")
    print(f"Ciphertext: {ciphertext}")
    print(f"Shift: {shift}")
    print("\nProses per karakter:")
    
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            pos = ord(char) - base
            new_pos = (pos - shift) % 26
            decrypted_char = chr(base + new_pos)
            decrypted += decrypted_char
            print(f"  {i+1}. '{char}' (pos {pos}) - {shift} = '{decrypted_char}' (pos {new_pos})")
        else:
            decrypted += char
            print(f"  {i+1}. '{char}' -> '{char}' (tidak berubah)")
    
    print(f"\nPlaintext: {decrypted}")
    return decrypted


def main():
    print("="*60)
    print("PROGRAM DEKRIPSI & EKSTRAKSI STEGANOGRAFI LSB")
    print("Kelompok 1: Caesar Cipher (shift 7) + LSB")
    print("="*60)
    
    print("\n--- INPUT DATA ---")
    stego_path = input("Masukkan path gambar stego (default: results/stego_kelompok1.png): ")
    
    if not stego_path:
        stego_path = "results/stego_kelompok1.png"
    
    if not os.path.exists(stego_path):
        print(f"ERROR: File {stego_path} tidak ditemukan!")
        return
    
    print("\n" + "="*60)
    
    # Ekstrak pesan dari gambar
    ciphertext = extract_lsb(stego_path)
    
    print("\n" + "="*60)
    
    # Dekripsi Caesar Cipher
    plaintext = caesar_cipher_decrypt(ciphertext, shift=7)
    
    print("\n" + "="*60)
    print("✓✓✓ PROSES SELESAI ✓✓✓")
    print("="*60)
    print(f"\nRingkasan:")
    print(f"  - Gambar stego: {stego_path}")
    print(f"  - Ciphertext: {ciphertext}")
    print(f"  - Plaintext: {plaintext}")
    print(f"\nPesan rahasia berhasil diekstraksi dan didekripsi!")
    
    # Simpan hasil ke file
    output_file = "results/decrypted_message.txt"
    os.makedirs("results", exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("HASIL DEKRIPSI\n")
        f.write("="*60 + "\n\n")
        f.write(f"Gambar stego: {stego_path}\n")
        f.write(f"Ciphertext: {ciphertext}\n")
        f.write(f"Plaintext: {plaintext}\n")
    
    print(f"\n✓ Hasil juga disimpan di: {output_file}")


if __name__ == "__main__":
    main()