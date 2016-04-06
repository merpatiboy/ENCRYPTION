__author__ = 'dicky irwanto'

from mode_des import mode_des

if __name__ == '__main__':
    '''
        CBC
    '''
    key = "12345678"
    iv = "12345678"
    mess_panjang = "AsistenKeamananInformasiJaringan"
    mess_pendek = "Asist"
    result = mode_des().encrypt("CBC",key,iv,mess_pendek)
    result = mode_des().decrypt("CBC",key,iv,result)
    print result
    '''
        CFB
    '''
    result = mode_des().encrypt("CFB",key,iv,mess_panjang)
    result = mode_des().decrypt("CFB",key,iv,result)
    print result
    '''
        OFB
    '''
    result = mode_des().encrypt("OFB",key,iv,mess_pendek)
    result = mode_des().decrypt("OFB",key,iv,result)
    print result
