import socket # tcp conntion to the server.
import time 
import ssl #TLS connection to the server
 # Only host name is required for the connection, not the full URL.

Cert_data= {
    
         
        "domain": "",
        "issuer": "",
        "expires":"",
        "days_left": "",
        "last_checked": "",
        "error_message": ""
       
}


def socket_connection(Domain):
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
                
                last_checked = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                expires=Cert["notAfter"]   
                issuer=dict(x[0] for x in Cert["issuer"]).get("organizationName")  
                days_left=days_left 
                Cert_data["domain"]=Domain
                Cert_data["issuer"]=issuer
                Cert_data["expires"]=expires
                Cert_data["days_left"]=days_left
                Cert_data["last_checked"]=last_checked
                error_flag = False          

    except Exception as e:
        print("Error occurred:", e)
        
        error_flag = True
        error_message = str(e)
        Cert_data["domain"]= Domain
        Cert_data["error_message"] = error_message
        return error_flag,Cert_data
     
    

    return error_flag,Cert_data