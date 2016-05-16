__author__ = 'DickyIrwanto'
'''
Rumus Miller rabin
1. Random bilangan int yang akan diproses
2. Pasti kan bil tersbut > 1 dan bila 2 dan 3 otomatis prime
3. lalu cek apakah bil tersebut composit dengan rumus n-1 == 2^s.d
4. lalu kita menggunakan rumus decompose untuk mendapatkan nilai s dan d
5. lalu buatlah perulangan sejumlah akurasi yang diingin kan misalkan 100
6. lalu pilihlah nilai random dari 2-(bil-2) sebagai nilai pembahi variabel
7. lakukan modex , pada python modex dilakukan dengan pow(x,y,n) = x**y %n
8. bila modex hasilnya 1 / p-1 maka bil tersebut bukan prime
9. lalu lakukan lah perulangan sebanyak d yang didapat pada tahap 4
- kemudian lakukan kan lah modex kembali dengan cara bil_hasil modex tahap 7 ^ 2 % s
- bila hasil dari modex tersbut == p-1 maka bil tersebut bukan prime
'''
import random
import math
import copy
from itertools import combinations
'''miller rabbin'''
'''
bil merupakan variabel hasil decompose
var merupakan variabel input
exponen merupakan variabel hasil decompose
'''
def decompose (var):
    exponent = 0
    bil = var
    while bil%2 == 0:
        bil = bil/2
        exponent += 1
    return exponent,bil

def miller(poss, var, exponent, bil):
    poss = pow(poss, bil,var)

    if poss == 1 or poss == var-1:
        return False

    for _ in range(exponent):
        poss = pow(poss, 2 , var)

        if poss == var -1 :
            return False
    return True

def isPrime(var, akur=100):
    if var == 2 or var ==3:
        return True
    if var < 2:
        return False

    jumlah_coba = 0
    exponent, bil = decompose(var-1)

    for _ in range(akur):
        poss = random.randint(2,var-2)
        if miller(poss,var,exponent,bil):
            return False

    return True
'''
    Mencari nilai mod yang digunakan untuk RSA dari 2 nilai miller
'''
def encludian(a,b):
    a = abs(a)
    b = abs(b)
    if a < b:
        a,b = b,a
    while b != 0:
        a,b = b, a % b
    return a
def extendencludian(a,b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extendencludian(b % a, a)
        return g, x - (b // a) * y, y
def coPrime(val):
    for i,k in combinations(val,2):
        if encludian(i,k) != 1:
            return False
    return True
#menemukan nilai mod
def modRSA(nilai,nilai2):
    if coPrime([nilai,nilai2]):
        kombinasi = extendencludian(nilai,nilai2)
        #print kombinasi
        return kombinasi[1]%nilai2
    else:
        return 0
'''
    pengambilan nilai key
'''
def key():
    x = 2
    result = 0
    result_1 = 0
    batas_bawah = 10**100
    batas_atas = 10**101
    while x:
        dump = random.randint(batas_bawah,batas_atas)
        #print dump
        if isPrime(dump):
            if x == 2:
                #print 'masuk'
                result= dump
                x -= 1
            elif x ==1 and dump!=result:
                result_1 = dump
                x -= 1
    private = result*result_1
    publik = (result-1)*(result_1-1)
    while 1:
        e = random.randint(1,publik)
        if coPrime([e,publik]):
            break
    d=modRSA(e,publik)
    #print private
    #print e
    #print d
    return (private, e,d)
    #return(e,d)

'''
    RSA setelah mendapatkan key
'''
#convert string to list int
def stringtonum(word):
    return [ord(chars) for chars in word]

#convert list angka to string
def numtostring(num):
    return ''.join(map(chr,num))

def numtoblock(l,n=8):
    dump_list = []
    list_process = copy.copy(l)
    if len(list_process) % n !=0:
        for i in range(0,n-len(list_process)%n):
            list_process.append(random.randint(32,116))
    for i in range(0, len(list_process),n):
        block = 0
        for j in range(0,n):
            block += list_process[i+j] << (8 * (n-j-1))
        dump_list.append(block)
    return dump_list

def blocktonum(block,n=8):
    list_process = copy.copy(block)
    dump_list = []
    for x in list_process:
        inner = []
        for i in range(0,n):
            inner.append(x%256)
            x >>= 8
        inner.reverse()
        dump_list.extend(inner)
    return dump_list
'''
    encrypt dan decrypt message
'''

def encrypt(message, mod, e):
    message_list = stringtonum(message)
    #print message_list
    message_block = numtoblock(message_list)
    return [pow(block,e,mod) for block in message_block]

def decrypt(message_chipper,mod,d):
    message_chipper_block = [pow(block,d,mod) for block in message_chipper]
    message_chipper_list = blocktonum(message_chipper_block)
    return numtostring(message_chipper_list)

class RSA():
    def __init__(self):
        self.mod = 0
        self.encrypt_key = 0
        self.decrypt_key = 0
    def run(self):
        self.mod,self.encrypt_key,self.decrypt_key = key()
        #self.mod,self.encrypt_key,self.decrypt_key = key()
        return self.mod,self.encrypt_key,self.decrypt_key
    def encrypt_RSA(self,message,mod,encrypt_key):
        message = str(message)
        return encrypt(message,mod,encrypt_key)
    def decrypt_RSA(self,chipper,mod,decrypt_key):
        return decrypt(chipper,mod,decrypt_key)

if __name__ == '__main__':
    message = 12345678
    x = RSA()
    m,e,d = x.run()
    cipper = x.encrypt_RSA(message,m,e)
    plaint = x.decrypt_RSA(cipper,m,d)
    print cipper
    print plaint
