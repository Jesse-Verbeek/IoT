import ldap
import sys

def login():

    #Configuration
    LDAP_SERVER = "ldap://192.168.137.100"
    username = r"BMC!\administrator"
    password = "Welkom01!"
    #------------
    l = ldap.initialize(LDAP_SERVER)
    try:
        l.simple_bind_s(username, password)
        base = "cn=users,DC=bmc,DC=lan"

        criteria = "(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))"

        result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria)
    except ldap.INVALID_CREDENTIALS:
        return False
    return result

def valid(rfid):
    results = login()
    try:
        for result in results:
            rfid.encode("utf-8")
            codeFromAd = result[1]['rfidCode']
            codeFromAd = codeFromAd[0].decode("utf-8")
            if codeFromAd == rfid:
                return True
    except:
        return False
