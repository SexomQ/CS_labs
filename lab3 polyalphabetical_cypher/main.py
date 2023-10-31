def generate_key_square(key):
    # Generate a key square from the given key
    key = key.replace(" ", "").upper()
    key_square = ""
    for char in key:
        if char not in key_square:
            key_square += char
    for char in "AĂÂBCDEFGHIÎKLMNOPQRSȘTȚUVWXYZ":
        if char not in key_square:
            key_square += char

    # Print the key square
    for i in range(0, 25, 5):
        print(key_square[i:i+5])
    return key_square

def get_char_positions(key_square, char):
    # Get the row and column positions of a character in the key square
    row = key_square.index(char) // 5
    col = key_square.index(char) % 5
    return row, col

def break_double_letters(plaintext):
    # Brake doubles recursively
    changes = 0
    for i in range(0, len(plaintext), 2):
        if i != len(plaintext)-1:
            if plaintext[i] == plaintext[i+1]:
                plaintext = plaintext[:i+1] + "Y" + plaintext[i+1:]
                print("-:"+plaintext)
                changes += 1
                break
    if changes > 0:
        break_double_letters(plaintext)
    return plaintext

def prepare_plaintext(plaintext):
    plaintext = plaintext.upper().replace(" ", "").replace("J", "I")
    
    # Break double letters
    plaintext = break_double_letters(plaintext)

    # Add X if the length of the plaintext is odd
    if len(plaintext) % 2 == 1:
        plaintext += "X"

    return plaintext

def encrypt(plaintext, key):
    # Encrypt the plaintext using the Playfair cipher
    key_square = generate_key_square(key)
    ciphertext = ""
    plaintext = prepare_plaintext(plaintext)

    # Encrypt
    for i in range(0, len(plaintext), 2):
        char1 = plaintext[i]
        char2 = plaintext[i+1]
        row1, col1 = get_char_positions(key_square, char1)
        row2, col2 = get_char_positions(key_square, char2)
        if row1 == row2:
            ciphertext += key_square[row1*5+(col1+1)%5]
            ciphertext += key_square[row2*5+(col2+1)%5]
        elif col1 == col2:
            ciphertext += key_square[((row1+1)%5)*5+col1]
            ciphertext += key_square[((row2+1)%5)*5+col2]
        else:
            ciphertext += key_square[row1*5+col2]
            ciphertext += key_square[row2*5+col1]
    return ciphertext

def decrypt(ciphertext, key):
    # Decrypt the ciphertext using the Playfair cipher
    key_square = generate_key_square(key)
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        char1 = ciphertext[i]
        char2 = ciphertext[i+1]
        row1, col1 = get_char_positions(key_square, char1)
        row2, col2 = get_char_positions(key_square, char2)
        if row1 == row2:
            plaintext += key_square[row1*5+(col1-1)%5]
            plaintext += key_square[row2*5+(col2-1)%5]
        elif col1 == col2:
            plaintext += key_square[((row1-1)%5)*5+col1]
            plaintext += key_square[((row2-1)%5)*5+col2]
        else:
            plaintext += key_square[row1*5+col2]
            plaintext += key_square[row2*5+col1]
    return plaintext

def main():
    # Main function
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Your choice: ")
    # check if the key is valid    
    while True:
        key = input("Enter the key: ")
        if len(key) < 7:
            print("The key must have at least 7 characters!")
        else:
            break
    if choice == "1":
        plaintext = input("Plaintext: ")
        print("Ciphertext:", encrypt(plaintext, key))
    elif choice == "2":
        ciphertext = input("Ciphertext: ")
        print("Plaintext:", decrypt(ciphertext, key))
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()