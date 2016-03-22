
__author__ = 'DickyIrwanto'
__doc__ == 'Dicky Irwanto'
'''
    Dokumen Editor dan Dokumentasi:
    Author: Dicky Irwanto
    Date: 22 Maret 2016
    License: Free
'''

'''
    Dokumen Sumber:
    Author:   Todd Whiteman
    Date:     16th March, 2009
    Verion:   2.0.0
    License:  Public Domain - free to do as you wish
'''
import sys

#instansiasi nilai objek
class _baseDes(object):
    def __init__(self, pad=None):

        if pad:
            pad = self._guardAgainstUnicode(pad)
        self.block_size = 8
        self._padding = pad


    def getKey(self):
        """getKey() -> bytes"""
        return self.__key

    def setKey(self, key):
        """Will set the crypting key for this object."""
        key = self._guardAgainstUnicode(key)
        self.__key = key

    def _padData(self, data):
        #Tidak menggunakan Padding
        if len(data) % self.block_size == 0:
            return data
            #Otomatis padding menggunakan zero
        else:
            pad_add = len(data) % self.block_size
            #print pad_add
            for x in range(pad_add,8):
                data += chr(0)
            return data
        #data += (self.block_size - (len(data) % self.block_size)) * pad
        #print data
        return data


    def _guardAgainstUnicode(self, data):
        # Only accept byte strings or ascii unicode values, otherwise
        # there is no way to correctly decode the data into bytes.

        if isinstance(data, unicode):
            raise ValueError("Harus Byte bukan Unicode...!")
        return data

'''DES'''
class des(_baseDes):

    # Permutasi dan translasi tabel DES
    #permutasi pemilihan key pc1
    __pc1 = [56, 48, 40, 32, 24, 16,  8,
          0, 57, 49, 41, 33, 25, 17,
          9,  1, 58, 50, 42, 34, 26,
         18, 10,  2, 59, 51, 43, 35,
         62, 54, 46, 38, 30, 22, 14,
          6, 61, 53, 45, 37, 29, 21,
         13,  5, 60, 52, 44, 36, 28,
         20, 12,  4, 27, 19, 11,  3
    ]

    # nilai left rotation dari pc 1
    __left_rotations = [
        1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
    ]

     #permutasi pemilihan key pc2
    __pc2 = [
        13, 16, 10, 23,  0,  4,
         2, 27, 14,  5, 20,  9,
        22, 18, 11,  3, 25,  7,
        15,  6, 26, 19, 12,  1,
        40, 51, 30, 36, 46, 54,
        29, 39, 50, 44, 32, 47,
        43, 48, 38, 55, 33, 52,
        45, 41, 49, 35, 28, 31
    ]

    # initial permutation IP
    __ip = [57, 49, 41, 33, 25, 17, 9,  1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8,  0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
    ]

    # Expand tabel dari 32 bit menjadi 48 bit
    __expansion_table = [
        31,  0,  1,  2,  3,  4,
         3,  4,  5,  6,  7,  8,
         7,  8,  9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31,  0
    ]

    #Insialisasi S_box
    __sbox = [
        # S1
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
         0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
         4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
         15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

        # S2
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
         3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
         0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
         13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

        # S3
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
         13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
         13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
         1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

        # S4
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
         13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
         10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
         3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

        # S5
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
         14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
         4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
         11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

        # S6
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
         10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
         9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
         4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

        # S7
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
         13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
         1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
         6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

        # S8
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
         1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
         7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
         2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ]


    # 32-bit permutasi fungsi P digunakan pada output dari S-boxes
    __p = [
        15, 6, 19, 20, 28, 11,
        27, 16, 0, 14, 22, 25,
        4, 17, 30, 9, 1, 7,
        23,13, 31, 26, 2, 8,
        18, 12, 29, 5, 21, 10,
        3, 24
    ]

    # final permutation IP^-1
    __fp = [
        39,  7, 47, 15, 55, 23, 63, 31,
        38,  6, 46, 14, 54, 22, 62, 30,
        37,  5, 45, 13, 53, 21, 61, 29,
        36,  4, 44, 12, 52, 20, 60, 28,
        35,  3, 43, 11, 51, 19, 59, 27,
        34,  2, 42, 10, 50, 18, 58, 26,
        33,  1, 41,  9, 49, 17, 57, 25,
        32,  0, 40,  8, 48, 16, 56, 24
    ]

    # Type dari crypting bentuk hexa
    ENCRYPT =	0x00
    DECRYPT =	0x01

    # Inisialisasi
    def __init__(self, key, pad=None):
        if len(key) != 8:
            raise ValueError("Invalid DES key size. Key must be exactly 8 bytes long.")
        _baseDes.__init__(self, pad)
        self.key_size = 8
        self.L = []
        self.R = []
        self.Kn = [ [0] * 48 ] * 16	# 16 48-bit keys (K1 - K16)
        self.final = []
        self.setKey(key)

    def setKey(self, key):
        """Set untuk crypting key yang panjang 8 byte."""
        _baseDes.setKey(self, key)
        self.__create_sub_keys()

    def __String_to_BitList(self, data):
        """Ubah dari string data menuju bits (1, 0)'s"""
        data = [ord(c) for c in data]
        l = len(data) * 8
        result = [0] * l
        pos = 0
        for ch in data:
            i = 7
            while i >= 0:
                if ch & (1 << i) != 0:
                    result[pos] = 1
                else:
                    result[pos] = 0
                pos += 1
                i -= 1
        return result

    def __BitList_to_String(self, data):
        """Ubah Bits menjadi string"""
        result = []
        pos = 0
        c = 0
        while pos < len(data):
            c += data[pos] << (7 - (pos % 8))
            if (pos % 8) == 7:
                result.append(c)
                c = 0
            pos += 1
        return ''.join([ chr(c) for c in result ])


    def __permutate(self, table, block):
        """Permutasi dan pemetaan block dengan tabel yang disediakan"""
        return list(map(lambda x: block[x], table))

    # Membuat 16 subkeys, K[1] - K[16]
    '''
    Step pembuatan key pada DES:
    1. pada awal lakukan mapping pada bit key (64 bit) menuju PC 1 hasil luaran menjadi 56 bit
    2. Lalu lakukan pemisahan 28 bit (left) dan 28 bit (right)
    3. Lakukan perulangan sebanyak 16x sejumlah subkey yang nanti digunakan
        - lakukan rotasi pada 28 bit key (right dan left) sesuai dengan __left.rotation
        - gabungkan key (left dan right) dan lakukan mapping pada pc2
        - simpan pada sebuah array K[i] - K[i+15]
    '''
    def __create_sub_keys(self):
        """Membuat 16 subkeys K[1] sampai K[16] dari key yang diberikan"""

        key = self.__permutate(des.__pc1, self.__String_to_BitList(self.getKey()))

        i = 0
        # Pembagian key menjadi left dan right sesion
        self.L = key[:28]
        """
        debug error pada left key
        print 'L',len(self.L),'\n',self.L
        debug error di key pc1 dan dibandigkan dengan bit list
        print 'key_real_key: %d\n'%len(self.__String_to_BitList(self.getKey())),self.__String_to_BitList(self.getKey())
        print 'key_after_pc1: %d\n'%len(key),key
        """

        self.R = key[28:]
        while i < 16:
            j = 0
            # Melakukan circular left shift
            while j < des.__left_rotations[i]:
                self.L.append(self.L[0])
                del self.L[0]

                self.R.append(self.R[0])
                del self.R[0]

                j += 1
            '''
            #Debug Rotasi dari Left dan Right
            print 'Total Rotasi:%d '%des.__left_rotations[i]
            print 'Hasil Right: ', self.R
            print 'Hasil Left: ', self.L
            '''
            # Membuat 1 / lebih subkey yang jumlahnya 16
            self.Kn[i] = self.__permutate(des.__pc2, self.L + self.R)
            i += 1
    '''
    Step Enkripsi:
    1. Lakukan permetaan data dengan tabel __ip
    2. Lakukan pemisahan data menjadi L dan R sebanyak 32 bit
    3. Masuk kedalam fungsi perulangan 16x
     -Lakukan pengcopyan nilai bagian Ln= Rn-1(left) dan Rn = Ln-1 + f(Rn-1,Kn) (right)
     -Karena bagian Rn masih berupa 32 bit lakukan expansi, dengan cara memetakan dengan tabel __expansion_table
     -Lakukan xor pada hasil Rn yang telah di expansion dengan Key/ K[n]
     -Bagi Rn menjadi 8 bagian , nantinya perbagian akan diproses pada s-box, lakukan perulangan sebanyak 8x
        -
     -Lakukan pemindahan nilai Rn = hasil pemetaan Bn terhadap __des.p
     -Lakukan xor Rn terhadap Ln dan disipan dalam Rn
     -Kemudian simpan nilai Rn-1 di Ln untuk digunakan kembali
    4. setelah melakukan perulangan 16x * 8x kemudian hasil akhir merupakan pemetaan tabel __fp dengan (Rk+Lk)
    '''
    # Bagian Utama enkripsi/deskripsi algorithm
    def __des_crypt(self, block, crypt_type):
        """Lakukan bit manipulasi dengan tabel IP"""
        block = self.__permutate(des.__ip, block)
        self.L = block[:32]
        self.R = block[32:]

        # Enkripsi dimulai dari Kn[1] hingga Kn[16]
        if crypt_type == des.ENCRYPT:
            iteration = 0
            iteration_adjustment = 1
        # Dekripsi dimulai Kn[16] menuju Kn[1]
        else:
            iteration = 15
            iteration_adjustment = -1

        i = 0
        while i < 16:
            # Make a copy of R[i-1], this will later become L[i]
            tempR = self.R[:]

            # Permutasi R[i - 1] untuk memulai membuat R[i]
            self.R = self.__permutate(des.__expansion_table, self.R)

            self.R = list(map(lambda x, y: x ^ y, self.R, self.Kn[iteration]))
            B = [self.R[:6], self.R[6:12], self.R[12:18], self.R[18:24], self.R[24:30], self.R[30:36], self.R[36:42], self.R[42:]]

            j = 0
            Bn = [0] * 32
            pos = 0
            while j < 8:
                # Work out the offsets
                m = (B[j][0] << 1) + B[j][5]
                n = (B[j][1] << 3) + (B[j][2] << 2) + (B[j][3] << 1) + B[j][4]

                # Menentukan nilai dari permutasi
                v = des.__sbox[j][(m << 4) + n]

                # Turn value into bits, add it to result: Bn
                Bn[pos] = (v & 8) >> 3
                Bn[pos + 1] = (v & 4) >> 2
                Bn[pos + 2] = (v & 2) >> 1
                Bn[pos + 3] = v & 1

                pos += 4
                j += 1

            # Permutasi dan combinasi dari B[1] - B[8]
            self.R = self.__permutate(des.__p, Bn)

            #XOR dengan L[1-n]
            self.R = list(map(lambda x, y: x ^ y, self.R, self.L))

            self.L = tempR

            i += 1
            iteration += iteration_adjustment

        # Final permutation of R[16]L[16]
        self.final = self.__permutate(des.__fp, self.R + self.L)
        return self.final


    # Data akan di enkrip/dekrip
    def crypt(self, data, crypt_type):

        # Error check data
        if not data:
            return ''

        # Membagi data menjadi beberapa blog
        i = 0
        dict = {}
        result = []
        while i < len(data):

            block = self.__String_to_BitList(data[i:i+8])
            processed_block = self.__des_crypt(block, crypt_type)

            result.append(self.__BitList_to_String(processed_block))
            i += 8
        return ''.join(result)


    def encrypt(self, data):
        data = self._guardAgainstUnicode(data)
        data = self._padData(data)
        return self.crypt(data, des.ENCRYPT)

    def decrypt(self, data):
        data = self._guardAgainstUnicode(data)
        data = self.crypt(data, des.DECRYPT)
        return data
