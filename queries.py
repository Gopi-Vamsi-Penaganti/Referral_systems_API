import uuid 
import mysql.connector 

def createUID():
    myuuid = uuid.uuid4()
    return str(myuuid) 

def createNewUser(data, refnum=0, balance=0):
    try:
        conn = mysql.connector.connect(host='localhost',
                            database='referralDB',
                            user='root',
                            password='vamsi123')
        cursor = conn.cursor()

        add_user = ("INSERT INTO ReferralSystem "
                "(PhoneNumber, FullName, ReferralCode, ReferredNum, ReferredContacts, Balance) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
        uuid = createUID()
        user_data = (data["phonenum"], data["name"], uuid, '0', "", '0')
        cursor.execute(add_user, user_data)
        conn.commit()

        cursor.close()
        conn.close()
        return {
            "success": True,
            "msg": f"{data['name']}, {'*'*8}{data['phonenum'][:4]} User created successfully!\n Use {uuid} to refer ur friends and family!"
        }
    except Exception as e:
        print("Error while creating new user......{str(e)}")
        return {
            "success": False, 
            "msg": f"{data['phonenum']} Error while creating new user."
        }

def get_value(value_name, value):
    query = ""
    if value_name=="ReferralCode":
        query = (f"SELECT * FROM ReferralSystem "
            "WHERE ReferralCode = %s")
    elif value_name=="PhoneNumber":
        query = (f"SELECT * FROM ReferralSystem "
            "WHERE PhoneNumber = %s")
    else: 
        return {
            "success": False,
            "msg": "Invalid Parameter"
        }
    print(query)
    
        
    try:
        conn = mysql.connector.connect(host='localhost',
                            database='referralDB',
                            user='root',
                            password='vamsi123')
        cursor = conn.cursor()
        cursor.execute(query, (value,))
        row = [r for r in cursor]
        print(row)
        cursor.close()
        conn.close()
        if len(row):
            return {
                "success": True,
                "msg": f"{value_name}....Exists",
                "row": row[0]

            }
        return {
                "success": False,
                "msg": f"{value_name} {value}.... Does Not Exists"
            }
    except Exception as e:
        print(f"Error while checking validity......{str(e)}")
        return {
            "success": False,
            "msg": str(e)
        }


def update_referer(params, phone):
    query = ("UPDATE ReferralSystem "
            "SET ReferredNum = %s, Balance = %s, ReferredContacts = %s"
            "WHERE ReferralCode = %s")
    referrednum, balance, referredcontacts, referralcode = int(params[3])+1, float(params[5]), params[4], params[2] 
    if not len(referredcontacts):
        referredcontacts = phone
    else:
        referredcontacts += f", {phone}"
    m = ""
    if referrednum == 3:
        balance += 100 
        m = f"Congratulations you have achieved your first milestone of Rs 100/- grofers cahsback\n Refer 5 more people to unlock the next milestone of Rs 500/- grofers cashback"

    elif referrednum == 8: 
        balance += 500
        m = f"Congratulations you have achieved your milestone of Rs 500/- grofers cahsback"
    else:
        if (3 - referrednum) > 0:
            m = f"Refer {(3 - referrednum)} more! for your first milestone of Rs 100/- grofers cashback"
        else:
            if (8 - referrednum) > 0:
                m = f"Refer {(8 - referrednum)} more! for your next milestone of Rs 500/- grofers cashback"

    try:
        conn = mysql.connector.connect(host='localhost',
                            database='referralDB',
                            user='root',
                            password='vamsi123')
        cursor = conn.cursor()
        cursor.execute(query, (referrednum, balance, referredcontacts, referralcode))
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "success": True, 
            "msg": f"Updated referrer  {'*'*8}{params[0][:4]}\n Available balance {balance}/-\n{m}"
        }
        
    except Exception as e:
        print(f"Error while updating referrer {params[0]}......{str(e)}")
        return {
            "success": False,
            "msg": str(e)
        }


def withdraw(value):
    query = ("DELETE FROM ReferralSystem "
            "WHERE PhoneNumber = %s")
    try:
        conn = mysql.connector.connect(host='localhost',
                            database='referralDB',
                            user='root',
                            password='vamsi123')
        cursor = conn.cursor()
        cursor.execute(query, (value,))
        conn.commit()
        cursor.close()
        conn.close()
    
        return {
            "success": True,
            "msg": f"{value} withdrawn from referral system.",

        }
    except Exception as e:
        print(f"Error while withdraw......{str(e)}")
        return {
            "success": False,
            "msg": str(e)
        }
