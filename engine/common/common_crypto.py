from Crypto.Cipher import AES
import base64
# pycryptodome
class prpcrypt():
    key = 'torrotorrotorro1'.encode('utf-8')
    iv = 'torrotorrotorro1'.encode('utf-8')
    BS = AES.block_size
    mode = AES.MODE_CBC
    @staticmethod
    def __pad(s):
        return s + (prpcrypt.BS - len(s) % prpcrypt.BS) * chr(prpcrypt.BS - len(s) % prpcrypt.BS)
        # 定义 padding 即 填充 为PKCS7

    @staticmethod
    def __unpad(s):
        return s[0:-ord(s[-1])]

    @staticmethod
    def encrypt(text):
        text = prpcrypt.__pad(text).encode('utf-8')
        cryptor = AES.new(prpcrypt.key, prpcrypt.mode, prpcrypt.iv)
        #第二个self.key 为 IV 即偏移量
        x = len(text) % 8
        if x != 0:
            text = text + '\0' * (8 - x)  # 不满16，32，64位补0
        prpcrypt.ciphertext = cryptor.encrypt(text)
        return base64.standard_b64encode(prpcrypt.ciphertext).decode("utf-8")

    @staticmethod
    def decrypt(text):
        cryptor = AES.new(prpcrypt.key, prpcrypt.mode, prpcrypt.key)
        de_text = base64.standard_b64decode(text)
        plain_text = cryptor.decrypt(de_text)
        st = str(plain_text.decode("utf-8")).rstrip('\0')
        out = prpcrypt.__unpad(st)
        return out

if __name__ == '__main__':
    # x = prpcrypt.encrypt('388||2021-09-26 12:38:36')
    z = prpcrypt.decrypt('qgrXkwN8kPjBdYCPVcbajA==')
    print(z)
    # print(x)
    # print(z, id, time)