__author__ = 'DickyIrwanto'

'''
    Dokumen Editor, Author, dan Dokumentasi:
    Author: Dicky Irwanto
    Date: 22 Maret 2016
    License: Free
'''

from DES import des

if __name__ == '__main__':
    '''
        Definisi Pesan dan Kunci harus 64 bit / 8 character
    '''
    key = '12345678'
    mess = '87654321'
    x = des(key).encrypt(mess)
    print x

    y = des(key).decrypt(x)
    print y
