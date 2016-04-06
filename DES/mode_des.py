__author__ = 'dicky irwanto'

from DES2 import des

class mode_des():
    def __init__(self):
        self.key = None
        self.iv = None
        self.mess = None
        self.type = None
        self.mess_chipper = None

    def padding(self):
        for x in xrange(0,8-(len(self.mess)%8)):
            self.mess += '~'

    def xor(self,data, data1):
        dummy = []
        for num in range(0, 64):
            if (data[num] == data1[num]):
                dummy.append(0)
            else:
                dummy.append(1)
        return dummy

    def __BitList_to_String(self, data):
        """Turn the list of bits -> data, into a string"""
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

    def __String_to_BitList(self,data):
        l = len(data) * 8
        result = [0] * l
        pos = 0
        for ch in data:
            i = 7
            ch = ord(ch)
            while i >= 0:
                if ch & (1 << i) != 0:
                    result[pos] = 1
                else:
                    result[pos] = 0
                pos += 1
                i -= 1
        return result

    def encrypt(self,type,key,iv,mess):
        self.mess = mess
        self.type = type
        self.key = key
        self.iv = iv
        if len(self.mess) % 8 != 0:
            self.padding()

        if type == "CBC":
            mess_arr = []
            result_arr = []
            for x in xrange (0,len(self.mess)/8):
                mess_arr.append(self.mess[x*8:(x+1)*8])
            temp_iv = self.__String_to_BitList(self.iv)
            for x in mess_arr:
                temp_mess = self.__String_to_BitList(x)
                temp_result_xor = self.xor(temp_mess,temp_iv)
                result = des(self.key).encrypt(self.__BitList_to_String(temp_result_xor))
                result_arr.append(result)
                temp_iv = self.__String_to_BitList(result)
            return ''.join(result_arr)

        elif type == "CFB":
            mess_arr = []
            result_arr = []
            for x in xrange (0,len(self.mess)/8):
                mess_arr.append(self.mess[x*8:(x+1)*8])
            data = self.iv
            for x in mess_arr:
                result = des(self.key).encrypt(data)
                result = self.xor(self.__String_to_BitList(x),self.__String_to_BitList(result))
                result = self.__BitList_to_String(result)
                result_arr.append(result)
                data = result
            return ''.join(result_arr)

        elif type == "OFB":
            mess_arr = []
            result_arr = []
            for x in xrange (0,len(self.mess)/8):
                mess_arr.append(self.mess[x*8:(x+1)*8])
            data = self.iv
            for x in mess_arr:
                result_des = des(self.key).encrypt(data)
                result = self.xor(self.__String_to_BitList(x),self.__String_to_BitList(result_des))
                result = self.__BitList_to_String(result)
                result_arr.append(result)
                data = result_des
            return ''.join(result_arr)


    def decrypt(self,type,key,iv,mess_chipper):
        self.type = type
        self.key = key
        self.iv = iv
        self.mess_chipper = str(mess_chipper)
        if type == "CBC":
            mess_chipper_arr = []
            result_arr = []
            for x in xrange(0, len(self.mess_chipper)/8):
                mess_chipper_arr.append(self.mess_chipper[x*8:(x+1)*8])
            temp_iv = self.__String_to_BitList(self.iv)
            for x in mess_chipper_arr:
                result_des = des(self.key).decrypt(x)
                result_des = self.__String_to_BitList(result_des)
                result = self.xor(temp_iv,result_des)
                result_arr.append(self.__BitList_to_String(result))
                temp_iv = self.__String_to_BitList(x)
            result = ''.join(result_arr)
            result = result.replace('~','')
            return result

        elif type == "CFB":
            mess_chipper_arr = []
            result_arr = []
            for x in xrange(0, len(self.mess_chipper)/8):
                mess_chipper_arr.append(self.mess_chipper[x*8:(x+1)*8])
            data = self.iv
            for x in mess_chipper_arr:
                result_des = des(self.key).encrypt(data)
                result = self.xor(self.__String_to_BitList(x),self.__String_to_BitList(result_des))
                result = self.__BitList_to_String(result)
                data = x
                result_arr.append(result)
            result = ''.join(result_arr)
            result = result.replace('~','')
            return result

        elif type == "OFB":
            mess_chipper_arr = []
            result_arr = []
            for x in xrange(0, len(self.mess_chipper)/8):
                mess_chipper_arr.append(self.mess_chipper[x*8:(x+1)*8])
            data = self.iv
            for x in mess_chipper_arr:
                result_des = des(self.key).encrypt(data)
                result = self.xor(self.__String_to_BitList(x),self.__String_to_BitList(result_des))
                result = self.__BitList_to_String(result)
                data = result_des
                result_arr.append(result)
            result = ''.join(result_arr)
            result = result.replace('~','')
            return result




