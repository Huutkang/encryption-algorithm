from math import e
import random
#ham tinh x^y(mod p)
def power(x, y, p) : 
    res = 1     # Initialize result
 
    # Update x if it is more
    # than or equal to p
    x = x % p
     
    if (x == 0) :
        return 0
 
    while (y > 0) :
         
        # If y is odd, multiply
        # x with result
        if ((y & 1) == 1) :
            res = (res * x) % p
 
        # y must be even now
        y = y >> 1      # y = y/2
        x = (x * x) % p
         
    return res
# TAO KHOA
print("Hay nhap mot so nguyen to p: ")
p = int(input(int()))  # (p =11 là một số nguyên tố)
print("Hay nhap mot so nguyen alpha: ")
alpha = int(input(int())) # (alpha =2 tự chọn một hệ số alpha (chưa biết điều kiển là gì)
a = random.randint(1,p-1)
print("Mot so nguyen a thỏa mãn 1<=a<=p-1 de tao khoa bi mat la: ", a)
        
#a = int(input(int()))  #( a = 3  là khóa bí mật thỏa mãn 1<= a <= p-1
private_key, public_key =((a,p), (p, alpha, power(alpha,a,p) )) #(power(alpha,a,p) là hệ số beta)
print("khoa bi mat la : ", private_key )
print("khoa cong khai la: ", public_key )


#ENCRYPTION
# chọn một số k bất kỳ thỏa mãn 1<=k<=p-1
k = random.randint(1,p-1)
#k=6
print('số k được chọn là: ', k)
# chọn plaintext m bất kỳ thỏa mãn 1<=m<=p-1
m = random.randint(1,p-1)
#m=10
print('plaintext được chọn là: ', m)
def encrypt(alpha, k, p, m):
    y1 = power(alpha,k,p)
    y2 = (m*pow(power(alpha,a,p),k))%p
    return(y1,y2)


#ciphertext 
c = encrypt(alpha, k, p, m)
print("ciphertext tìm được là: ", c)


#DECRYPTION
#d(y1,y2) = y2*(y1^-a)(modp)
# chú ý: ((y^a)^-1)modp = (y^(p-1-a))modp
y1 = power(alpha,k,p)
#print(y1)
y2 = (m*pow(power(alpha,a,p),k))%p
#print(y2)
def decrypt(y1,y2,p,a):
    x= (y2*(pow(y1,p-1-a)))%p
    return x
m1 = decrypt(y1,y2,p,a)
print("recovertext tìm được là: ", m1)