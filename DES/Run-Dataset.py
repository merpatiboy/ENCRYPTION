__author__ = 'DickyIrwanto'
'''
    Editor, Author, dan Dokumentasi:
    Author: Dicky Irwanto
    Date: 24 Maret 2016
    License: Free
'''
from DES2 import des

if __name__ == '__main__':
    '''
        Mapping Dataset:
        Baris 1: IV (64 Bit)
        Baris 2: Key (64 Bit)
        Baris 3: Pesan
    '''

    '''
        Pengambilan Data dari file
    '''
    f = open('dataset.txt',"rb")
    temp = f.readlines()
    f.close()
    dataset = []
    for data in temp:
        dataset.append(data.replace('\r\n',''))

    '''
        Proses Enkripsi dan decrypt
    '''
    mess  = []
    all_result = []
    all_result_decrypt = []
    for data in range(0,len(dataset),3):
        result = des(dataset[data+1]).encrypt(dataset[data+2])
        result_decrypt = des(dataset[data+1]).decrypt(result)
        all_result.append(result)
        all_result_decrypt.append(result_decrypt)
        mess.append(dataset[data+2])

    '''
        Proses Cetak / Print
    '''
    for data in range(0, len(all_result_decrypt)):
        print 'Pesan:',mess[data]
        print 'Encrypt:', all_result[data]
        print 'Decrypt:', all_result_decrypt[data]