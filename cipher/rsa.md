
RSA总结
=======


RSA加密和解密
=============

  * 加密

		RSAEP ((n, e), m)

		Input:
		(n, e)   RSA public key
		m        message representative, an integer between 0 and n - 1

		Output:
		c        ciphertext representative, an integer between 0 and n - 1

		Error: "message representative out of range"

		Assumption: RSA public key (n, e) is valid

		Steps:

		If the message representative m is not between 0 and n - 1, output
			"message representative out of range" and stop.

		Let c = m^e mod n.

		Output c.


  * 解密

		RSADP (K, c)

		Input:
		K        RSA private key, where K has one of the following forms:
			- a pair (n, d)
            - a quintuple (p, q, dP, dQ, qInv) and a possibly empty
              sequence of triplets (r_i, d_i, t_i), i = 3, ..., u
		c        ciphertext representative, an integer between 0 and n - 1

		Output:
		m        message representative, an integer between 0 and n - 1

		Error: "ciphertext representative out of range"

		Assumption: RSA private key K is valid

		Steps:

		If the ciphertext representative c is not between 0 and n - 1,
		output "ciphertext representative out of range" and stop.

		The message representative m is computed as follows.

		a. If the first form (n, d) of K is used, let m = c^d mod n.

		b. If the second form (p, q, dP, dQ, qInv) and (r_i, d_i, t_i)
			of K is used, proceed as follows:

         i.    Let m_1 = c^dP mod p and m_2 = c^dQ mod q.

         ii.   If u > 2, let m_i = c^(d_i) mod r_i, i = 3, ..., u.

         iii.  Let h = (m_1 - m_2) * qInv mod p.

         iv.   Let m = m_2 + q * h.

         v.    If u > 2, let R = r_1 and for i = 3 to u do

                  1. Let R = R * r_(i-1).

                  2. Let h = (m_i - m) * t_i mod r_i.

                  3. Let m = m + R * h.

		Output m.


签名和验签
==========


  * 签名

		RSASP1 (K, m)

		Input:
		K        RSA private key, where K has one of the following forms:
            - a pair (n, d)
            - a quintuple (p, q, dP, dQ, qInv) and a (possibly empty)
              sequence of triplets (r_i, d_i, t_i), i = 3, ..., u
		m        message representative, an integer between 0 and n - 1

		Output:
		s        signature representative, an integer between 0 and n - 1

		Error: "message representative out of range"

		Assumption: RSA private key K is valid

		Steps:

		If the message representative m is not between 0 and n - 1,
		output "message representative out of range" and stop.

		The signature representative s is computed as follows.

		 a. If the first form (n, d) of K is used, let s = m^d mod n.

         b. If the second form (p, q, dP, dQ, qInv) and (r_i, d_i, t_i)
         of K is used, proceed as follows:

         i.    Let s_1 = m^dP mod p and s_2 = m^dQ mod q.

         ii.   If u > 2, let s_i = m^(d_i) mod r_i, i = 3, ..., u.

         iii.  Let h = (s_1 - s_2) * qInv mod p.

         iv.   Let s = s_2 + q * h.

         v.    If u > 2, let R = r_1 and for i = 3 to u do

                  1. Let R = R * r_(i-1).

		Output s.


  * 验签

		RSAVP1 ((n, e), s)

		Input:
		(n, e)   RSA public key
		s        signature representative, an integer between 0 and n - 1

		Output:
		m        message representative, an integer between 0 and n - 1

		Error: "signature representative out of range"

		Assumption: RSA public key (n, e) is valid

		Steps:

		If the signature representative s is not between 0 and n - 1,
		output "signature representative out of range" and stop.

		Let m = s^e mod n.

		Output m.


RSA-PKCS1-v1_5
=================

  * 加密

		RSAES-PKCS1-V1_5-ENCRYPT ((n, e), M)

		Input:
		(n, e)   recipient's RSA public key (k denotes the length in octets
            of the modulus n)
		M        message to be encrypted, an octet string of length mLen,
            where mLen <= k - 11

		Output:
		C        ciphertext, an octet string of length k

		Error: "message too long"

		Steps:

		Length checking: If mLen > k - 11, output "message too long" and
		stop.

		EME-PKCS1-v1_5 encoding:

		  a. Generate an octet string PS of length k - mLen - 3 consisting
		  of pseudo-randomly generated nonzero octets.  The length of PS
		  will be at least eight octets.

		  b. Concatenate PS, the message M, and other padding to form an
		  encoded message EM of length k octets as

            EM = 0x00 || 0x02 || PS || 0x00 || M.

		RSA encryption:

		  a. Convert the encoded message EM to an integer message
		  representative m (see Section 4.2):

            m = OS2IP (EM).

		  b. Apply the RSAEP encryption primitive (Section 5.1.1) to the RSA
		  public key (n, e) and the message representative m to produce
		  an integer ciphertext representative c:

            c = RSAEP ((n, e), m).

		  c. Convert the ciphertext representative c to a ciphertext C of
			  length k octets (see Section 4.1):

               C = I2OSP (c, k).

		Output the ciphertext C.


  * 解密

		RSAES-PKCS1-V1_5-DECRYPT (K, C)

		Input:
		K        recipient's RSA private key
		C        ciphertext to be decrypted, an octet string of length k,
			where k is the length in octets of the RSA modulus n

		Output:
		M        message, an octet string of length at most k - 11

		Error: "decryption error"

		Steps:

		Length checking: If the length of the ciphertext C is not k octets
		(or if k < 11), output "decryption error" and stop.

		RSA decryption:

		  a. Convert the ciphertext C to an integer ciphertext
			  representative c (see Section 4.2):

            c = OS2IP (C).

		  b. Apply the RSADP decryption primitive (Section 5.1.2) to the RSA
		  private key (n, d) and the ciphertext representative c to
		  produce an integer message representative m:

            m = RSADP ((n, d), c).

		  If RSADP outputs "ciphertext representative out of range"
		  (meaning that c >= n), output "decryption error" and stop.

		  Convert the message representative m to an encoded message EM
		  of length k octets (see Section 4.1):

            EM = I2OSP (m, k).

		EME-PKCS1-v1_5 decoding: Separate the encoded message EM into an
		octet string PS consisting of nonzero octets and a message M as

		EM = 0x00 || 0x02 || PS || 0x00 || M.

		If the first octet of EM does not have hexadecimal value 0x00, if
		the second octet of EM does not have hexadecimal value 0x02, if
		there is no octet with hexadecimal value 0x00 to separate PS from
		M, or if the length of PS is less than 8 octets, output
		"decryption error" and stop.  (See the note below.)

		Output M.


引用
====

* <http://www.cs.cornell.edu/courses/cs5430/2015sp/notes/rsa_sign_vs_dec.php>

* [rfc3447](https://www.ietf.org/rfc/rfc3447.txt)
