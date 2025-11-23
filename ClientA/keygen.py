import paramiko

#Generates a 2048-bit RSA private key
key = paramiko.RSAKey.generate(2048)

#Saves private key to a file
private_key_path = "ClientA/private_key.pem"
key.write_private_key_file(private_key_path)

# Saves public key to a file 
public_key_path = "Alicepublickey.pem"
with open(public_key_path, "w") as f:
    f.write(f"{key.get_name()} {key.get_base64()}")