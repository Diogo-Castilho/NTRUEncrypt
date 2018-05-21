NTRU Cryptosystem

For running this project open a terminal on the folder that contains 
the file NTRU.py then open either python (version 2) or sage with:

python2
or
sage

Then type:
from NTRU import * 

Then you will have to inicialize a NTRU object with:

ntru = NTRU(x)

This x has to be a number between 0 and 3. It sets same parameters
like key size. (0-lower key size and 3-higher key size)

Then you will need to create your keys with:

ntru.create_keys()

You can check the values of your keys with prints. In this case 
printing ntru.h will give you your public key and ntru.f will
give you your private key


For ciphering/deciphering I have implemented two different methods.
The first method is taken from:
https://assets.securityinnovation.com/static/downloads/NTRU/resources/NTRU-PKCS-Tutorial.pdf
For using this method you need to run:

secret = ntru.simple_cipher("Very secret information", ntru.h)

The secret variable will contain a polynomial that is the string you entered ciphered.
And for deciphering you need to run:

ntru.simple_decipher(secret)

This will both print and return the deciphered secret
(If you want to assign its value to a variable)

The second method is based on the algorithm from this paper:
https://eprint.iacr.org/2015/708.pdf 
(The parameters I used were also taken from this paper)
For using this method you need to run:

secret = ntru.cipher("Even more secret info", ntru.h)

And for deciphering:

ntru.decipher(secret)

(This again will both print and return the deciphered secret)
