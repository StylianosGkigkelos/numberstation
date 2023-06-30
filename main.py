# This project simulates a number station.
# A number station requires a one time pad to encrypt a message of specific (known) characters.
# The length of that one time pad must be equal or bigger than the length of the message.
# In addition, the one time pad has to be truly randomly generated.
# Since Python functions generate random numbers using pseudo-random number generators, they weren't used.
# For true randomness the site random.org was used, which generates numbers using atmospheric noise.
# For true security, this process shouldn't use an external web application but a hardware random number generator.
# An example of such is using an RTL-SDR dongle to generate those numbers using the program rtl_entropy
# (https://pthree.org/2015/06/16/hardware-rng-through-an-rtl-sdr-dongle/)
# This module can generate the one time pad, as well as, encrypt/decrypt a message.
# It also generates the corresponding voice message using samples from https://soundbible.com/2008-0-9-Male-Vocalized.html
# The folder icon is from https://www.shareicon.net/folder-open-file-button-interface-690535
# Made by Stelios Gigelos

# Required to fetch random numbers from random.org, using http get.
import requests
# Required to manipulate .wav files.
from pydub import AudioSegment

# This cipher maps numbers into characters.
# This corresponds to a Vernam Cipher table like STASI's TAPIR
# The characters and corresponding values can be changed.
# These values were chosen because they are equal to 6 bits.
# More or less characters can be used, but they require code changes
cipher = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
    'i': 8,
    'j': 9,
    'k': 10,
    'l': 11,
    'm': 12,
    'n': 13,
    'o': 14,
    'p': 15,
    'q': 16,
    'r': 17,
    's': 18,
    't': 19,
    'u': 20,
    'v': 21,
    'w': 22,
    'x': 23,
    'y': 24,
    'z': 25,
    'A': 26,
    'B': 27,
    'C': 28,
    'D': 29,
    'E': 30,
    'F': 31,
    'G': 32,
    'H': 33,
    'I': 34,
    'J': 35,
    'K': 36,
    'L': 37,
    'M': 38,
    'N': 39,
    'O': 40,
    'P': 41,
    'Q': 42,
    'R': 43,
    'S': 44,
    'T': 45,
    'U': 46,
    'V': 47,
    'W': 48,
    'X': 49,
    'Y': 50,
    'Z': 51,
    '0': 52,
    '1': 53,
    '2': 54,
    '3': 55,
    '4': 56,
    '5': 57,
    '6': 58,
    '7': 59,
    '8': 60,
    '9': 61,
    ' ': 62,
    '.': 63
}

# This is the reversed cipher, needed for decrypting
rev_cipher = dict(map(reversed, cipher.items()))


def main():
    message = input('Enter message to encrypt\n')
    encrypt(message, 1, 'encrypted_text.txt', 'onetimepad.txt')
    print(decrypt('encrypted_text.txt', 'onetimepad.txt'))


# Takes a plaintext and encrypts it by generating a one  time pad
def encrypt(message, iterations, enc_path, otp_path, audio_path, padcode):
    # List used for storing the message in the substituted form
    temp = []
    # List used to store the one time pad
    onetimepad = []
    try:
        # match characters with numbers
        for character in message:
            temp.append(cipher[character])
    except KeyError:
        # if a character, not found in the cipher, was entered, throw exception
        print('Invalid message')
        return ''
    message_length = len(temp)
    # due to the limits imposed by random.org message is limited to 10000 characters
    if message_length > 10000:
        print('Message too long. Due to random.org only 10000 numbers can be generated at once.')
        return ''
    # The encrypted message is shown in groups of 6 digits, so padding is used
    elif message_length % 3 == 1:
        temp.append(62)
        temp.append(62)
        message_length = len(temp)
    elif message_length % 3 == 2:
        temp.append(62)
        message_length = len(temp)

    # As instructed in https://www.random.org/clients/http/
    random_parameters = {'num': message_length,
                         'min': 0,
                         'max': 63,
                         'col': 1,
                         'base': 10,
                         'format': 'plain',
                         'rnd': 'new'
                         }
    # http get
    r = requests.get('https://www.random.org/integers/', random_parameters)
    # if a response was returned
    if r.status_code == 200:
        split_response = r.text.strip('\n').split('\n')
        for i in split_response:
            onetimepad.append(int(i))
        encrypted_message = list_xor(temp, onetimepad)
        write_message_file(onetimepad, otp_path)
        write_message_file(encrypted_message, enc_path)
        create_audio(encrypted_message, audio_path, iterations, padcode)
    else:
        print('random.org could not be reached, error {}'.format(r.status_code))


def create_audio(encrypted_array, audio_path, block_repetitions=1, padcode=None):
    numbers = [AudioSegment.from_wav('numbers\\0.wav'),
               AudioSegment.from_wav('numbers\\1.wav'),
               AudioSegment.from_wav('numbers\\2.wav'),
               AudioSegment.from_wav('numbers\\3.wav'),
               AudioSegment.from_wav('numbers\\4.wav'),
               AudioSegment.from_wav('numbers\\5.wav'),
               AudioSegment.from_wav('numbers\\6.wav'),
               AudioSegment.from_wav('numbers\\7.wav'),
               AudioSegment.from_wav('numbers\\8.wav'),
               AudioSegment.from_wav('numbers\\9.wav'),
               AudioSegment.from_wav('numbers\\silence.wav'),
               AudioSegment.from_wav('numbers\\intro.wav'),
               AudioSegment.from_wav('numbers\\break.wav')
               ]
    soundfile = numbers[11] + numbers[10] + numbers[11] + numbers[10]
    if isinstance(padcode, list):
        for j in range(block_repetitions):
            for k in range(3):
                soundfile += numbers[int(padcode[k][0])] + numbers[int(padcode[k][1])]
            soundfile += numbers[12]

    for i in range(0, len(encrypted_array), 3):
        temp = [format(encrypted_array[i], 'd').zfill(2),
                format(encrypted_array[i+1], 'd').zfill(2),
                format(encrypted_array[i+2], 'd').zfill(2)]
        for j in range(block_repetitions):
            for k in range(3):
                soundfile += numbers[int(temp[k][0])] + numbers[int(temp[k][1])]

            soundfile += numbers[10] + numbers[10]
    soundfile += numbers[11] + numbers[10] + numbers[11] + numbers[10]
    soundfile.export(audio_path, format='wav')


# XORs two integer lists of the same length
def list_xor(list1, list2):
    if len(list1) != len(list2):
        raise ValueError('Arguments of different sizes')
    xored = []
    for i in range(len(list1)):
        xored.append(list1[i] ^ list2[i])
    return xored


def write_message_file(message_array, filename):
    with open(filename, "w") as f:
        f.write(format(message_array[0], 'd').zfill(2))
        for i in range(1, len(message_array)):
            if i % 3 != 0:
                f.write(format(message_array[i], 'd').zfill(2))
            else:
                f.write(' {}'.format(format(message_array[i], 'd').zfill(2)))


def read_message_file(filename):
    message = []
    with open(filename, 'r') as f:
        text = f.readline()
        a = text.split()
        for i in a:
            message.append(int(i[0:2]))
            message.append(int(i[2:4]))
            message.append(int(i[4:6]))
    return message


def decrypt(encrypted_file, onetimepad_file):
    temp = []
    encrypted = read_message_file(encrypted_file)
    onetimepad = read_message_file(onetimepad_file)
    decrypted = list_xor(encrypted, onetimepad)
    try:
        for number in decrypted:
            temp.append(rev_cipher[number])
        return ''.join(temp)
    except KeyError:
        print('Invalid text')
        return ''


if __name__ == '__main__':
    main()
