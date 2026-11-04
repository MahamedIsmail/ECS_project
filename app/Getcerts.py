import socket # tcp conntion to the server.
import time 
import ssl #TLS connection to the server
Domain="dontexits" # Only host name is required for the connection, not the full URL.



def socket_connection():
    try:
        ssl_context=ssl.create_default_context() # Gets the rulebook for the TLS connection, including the CA certificates to verify the server's certificate.
        print("1. Context created. Verify mode:", ssl_context.verify_mode,
            "| Check hostname:", ssl_context.check_hostname)
        with socket.create_connection ( (Domain,443) , timeout=5) as sock: # Make a TCP connection to the server. The socket is automatically closed when the block ends.
            print("\n2. TCP connected (no encryption yet)")
            print("   My side (IP, port):    ", sock.getsockname())
            print("   Server side (IP, port):", sock.getpeername())
            with ssl_context.wrap_socket(sock, server_hostname=Domain) as tls:
                Cert=tls.getpeercert() # Get the server's certificate.
                print("\n3. TLS connected (encrypted)")
                print("certificate obtained from the server")
                #calculate the number of days left before the certificate expires
                expires_at = ssl.cert_time_to_seconds(Cert["notAfter"])
                days_left = int((expires_at - time.time()) // 86400)

    except Exception as e:
        print("Error occurred:", e)
        return {"error": str(e)}

    return {
        "domain": Domain,
        "issuer": dict(x[0] for x in Cert["issuer"]).get("organizationName"),
        "expires": Cert["notAfter"],
        "days_left": days_left,
        "years_left": round(days_left / 365, 2)
    }
