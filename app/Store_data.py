import uuid

Data_base = []



def store_data(data):
    
    DB_block= {
    
        "id": "a1b2c3", 
        "domain": "",
        "issuer": "",
        "expires":"",
        "days_left": "",
        "last_checked": "",
        "error": False,
        "error_message": "" 
       
}
    error_flag,Cert_data=data
    print("Storing data:", data)
    print ("new id generated:", str(uuid.uuid4()))
    # Creat a new unique ID for the certificate data, including the domain name
    DB_block["id"]=str(uuid.uuid4())
    DB_block["domain"]=Cert_data["domain"]
    
    # If there was an error during the socket connection or no certificate obtained, set the error flag and message in the certificate data
    if error_flag == True:
          DB_block["error"]=True
          DB_block["error_message"]=Cert_data["error_message"]
          DB_block["last_checked"]=Cert_data["last_checked"]
          
          Data_base.append(DB_block) #save the data to the database even if there was an error, so that it can be retrieved later for debugging or analysis.
          return DB_block
    
    else:
        
        DB_block["error"]=False
        DB_block["error_message"]=""
        DB_block["issuer"]=Cert_data["issuer"]
        DB_block["expires"]=Cert_data["expires"]
        DB_block["days_left"]=Cert_data["days_left"]
        DB_block["last_checked"]=Cert_data["last_checked"]
        Data_base.append(DB_block) 
    
    return DB_block

    
    

def delet_data(item_id):
  
    for index, item in enumerate(Data_base):
        if item["id"] == item_id:
            removed = Data_base.pop(index)
            print("Deleted:", removed["domain"], flush=True)
            return removed
    return None
    
    
    
    
    
    
    
def list_data():
    
    for data in Data_base:
        print(data)
        print("________________________________________________________\n")
    
    
    print("Total number of certificates stored:", len(Data_base))
    return Data_base
      
    