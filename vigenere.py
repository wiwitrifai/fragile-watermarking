def encrypt(plain, key):
	cipher = []
	for i in range(len(plain)):
		c = ord(plain[i])+ord(key[i%len(key)])
		cipher.append(chr(c%256))

	return "".join(cipher)