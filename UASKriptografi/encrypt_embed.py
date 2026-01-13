"""
Program Enkripsi Caesar Cipher + Steganografi LSB
Kelompok 1: Caesar Cipher dengan shift 7 + Steganografi LSB
"""

from PIL import Image
import numpy as np
import os


def caesar_cipher_encrypt(plaintext, shift=7):
    encrypted = ""
    
    print("\n=== PROSES ENKRIPSI CAESAR CIPHER ===")
    print(f"Plaintext: {plaintext}")
    print(f"Shift: {shift}")
    print("\nProses per karakter:")
    
    for i, char in enumerate(plaintext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            pos = ord(char) - base
            new_pos = (pos + shift) % 26
            encrypted_char = chr(base + new_pos)
            encrypted += encrypted_char
            print(f"  {i+1}. '{char}' (pos {pos}) + {shift} = '{encrypted_char}' (pos {new_pos})")
        else:
            encrypted += char
            print(f"  {i+1}. '{char}' -> '{char}' (tidak berubah)")
    
    print(f"\nCiphertext: {encrypted}")
    return encrypted


def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    
    print("\n=== KONVERSI TEKS KE BINARY ===")
    print(f"Teks: {text}")
    print(f"Panjang: {len(text)} karakter")
    print("\nKonversi per karakter:")
    
    for i, char in enumerate(text):
        binary_char = format(ord(char), '08b')
        print(f"  {i+1}. '{char}' -> ASCII {ord(char)} -> {binary_char}")
    
    print(f"\nBinary lengkap ({len(binary)} bit):")
    print(f"{binary[:64]}..." if len(binary) > 64 else binary)
    
    return binary


def embed_lsb(image_path, message, output_path):
    print("\n=== PROSES STEGANOGRAFI LSB ===")
    
    img = Image.open(image_path)
    img_array = np.array(img)
    
    print(f"Gambar carrier: {image_path}")
    print(f"Ukuran gambar: {img_array.shape}")
    print(f"Dimensi: {img.size[0]} x {img.size[1]} pixels")
    
    binary_message = text_to_binary(message)
    message_length = len(binary_message)
    length_binary = format(message_length, '032b')
    
    print(f"\n=== HEADER INFORMASI ===")
    print(f"Panjang pesan: {message_length} bit")
    print(f"Header (32 bit): {length_binary}")
    
    full_binary = length_binary + binary_message
    print(f"Total bit yang akan di-embed: {len(full_binary)} bit")
    
    height, width, channels = img_array.shape
    max_capacity = height * width * channels
    
    print(f"\nKapasitas maksimal gambar: {max_capacity} bit")
    
    if len(full_binary) > max_capacity:
        print("ERROR: Pesan terlalu panjang untuk gambar ini!")
        return False
    
    print(f"Kapasitas tersisa: {max_capacity - len(full_binary)} bit")
    
    print("\n=== PROSES EMBEDDING ===")
    print("Memodifikasi LSB pixel...")
    
    flat_array = img_array.flatten()
    
    print("\nContoh embedding (10 bit pertama):")
    for i in range(min(10, len(full_binary))):
        original_pixel = flat_array[i]
        bit_to_embed = int(full_binary[i])
        modified_pixel = (original_pixel & 0xFE) | bit_to_embed
        print(f"  Bit {i+1}: Pixel[{i}] = {original_pixel:08b} -> {modified_pixel:08b} (embed '{bit_to_embed}')")
        flat_array[i] = modified_pixel
    
    for i in range(10, len(full_binary)):
        bit_to_embed = int(full_binary[i])
        flat_array[i] = (flat_array[i] & 0xFE) | bit_to_embed
    
    stego_array = flat_array.reshape(img_array.shape)
    stego_img = Image.fromarray(stego_array.astype('uint8'))
    stego_img.save(output_path)
    
    print(f"\n✓ Stego image berhasil disimpan: {output_path}")
    print(f"✓ Pesan berhasil di-embed dengan aman!")
    
    return True


def main():
    print("="*60)
    print("PROGRAM ENKRIPSI & EMBEDDING STEGANOGRAFI LSB")
    print("Kelompok 1: Caesar Cipher (shift 7) + LSB")
    print("="*60)
    
    print("\n--- INPUT DATA ---")
    plaintext = input("Masukkan pesan rahasia: ")
    
    if not plaintext:
        print("ERROR: Pesan tidak boleh kosong!")
        return
    
    image_path = input("Masukkan path gambar  (default: images/luffy.jpg): ")
    if not image_path:
        image_path = "images/luffy.jpg"
    
    if not os.path.exists(image_path):
        print(f"ERROR: File {image_path} tidak ditemukan!")
        return
    
    output_path = "results/stego_kelompok1.png"
    os.makedirs("results", exist_ok=True)
    
    print("\n" + "="*60)
    
    ciphertext = caesar_cipher_encrypt(plaintext, shift=7)
    
    print("\n" + "="*60)
    
    success = embed_lsb(image_path, ciphertext, output_path)
    
    if success:
        print("\n" + "="*60)
        print("✓✓✓ PROSES SELESAI ✓✓✓")
        print("="*60)
        print(f"\nRingkasan:")
        print(f"  - Plaintext: {plaintext}")
        print(f"  - Ciphertext: {ciphertext}")
        print(f"  - Gambar : {image_path}")
        print(f"  - Stego image: {output_path}")
        print(f"\nPesan Anda telah berhasil dienkripsi dan disembunyikan!")


if __name__ == "__main__":
    main()

