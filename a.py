import os
import sys
import json
import subprocess
import time


#PASSING USER'S DESIRED DOMAIN NAME TO CREATE "DNS A-RECORD"

realm_name = sys.argv[1]
r = realm_name
realm_name = '"'+realm_name+'"'
pre = "admin"
domain = pre + ".harshit3030.xyz"
#print(domain+" added into PYTHON script successfully...\n")
fileread = open("sample.json", 'r')
json_object = json.load(fileread)
fileread.close()
json_object["Changes"][0]["ResourceRecordSet"]["Name"] = domain
#curl --request POST --header "Content-Type: application/json" "http://openam.harshit3030.xyz:8080/openam/json/authenticate"
#CREATING REALM
print("Authenticating...\n")
api_string = "curl --request POST --header "+"\"Content-Type: application/json\"" + \
    " \"https://"+pre+".harshit3030.xyz:8443/ctrl/json/authenticate\""
result = subprocess.run(api_string, shell=True, capture_output=True)
json_string = result.stdout
json_object = json.loads(json_string)
json_formatted_string = json.dumps(json_object, indent=2)
json_object["callbacks"][0]["input"][0]["value"] = "amadmin"
json_object["callbacks"][1]["input"][0]["value"] = "harshit123"
json_object_final = json.dumps(json_object, indent=2)
api_string2 = "curl --request POST --header "+"\"Content-Type: application/json\"" + " --data '" + \
    json_object_final+"' "+" \"https://"+pre + \
    ".harshit3030.xyz:8443/ctrl/json/authenticate\""
result2 = subprocess.run(api_string2, shell=True, capture_output=True)
json_string2 = result2.stdout
json_object2 = json.loads(json_string2)
json_formatted_string2 = json.dumps(json_object2["tokenId"], indent=2)
print(json_formatted_string2)
print("\n\n")
token = json_formatted_string2
token = token.lstrip('\"')
token = token.rstrip('\"')
print("Token is " + token)
print("\n\n")


#Adding aliases
#realm_name = '"testapi"'
alias = "\""+realm_name.strip('"') + ".harshit3030.xyz"+"\""
s = '{"name":' + realm_name + \
    ', "active":true, "parentPath":"/","aliases":['+alias+']}'

api_string3 = "curl --request POST --header "+"\"iPlanetDirectoryPro: "+token + "\"" + " --header " + "\"Content-Type: application/json\"" + \
    " --data " + "\'" + s + "\'" + " \"https://"+pre + \
    ".harshit3030.xyz:8443/ctrl/json/global-config/realms?_action=create\""

print(api_string3)
result3 = subprocess.run(api_string3, shell=True, capture_output=True)
print(result3)
print("\n\n")
j3 = result3.stdout
jobj3 = json.loads(j3)
j3string = json.dumps(jobj3, indent=2)
print(j3string)
print("\n\n")


# Create a LDIF file in the location "cd /usr/ssosec/config/opends/bin"
realm_name = realm_name.strip('"')
file_name = realm_name + ".ldif"
name = os.path.join('/usr/ssosec/config/opends/bin', file_name)
ldif_file = open(name, "w")
ldif_file.write("dn: ou="+realm_name+",dc=openam,dc=openidentityplatform,dc=org\nchangetype: add\nou: " +
                realm_name+"\nobjectClass: organizationalUnit")
ldif_file.close()

ldap_command = "./ldapmodify --hostname localhost --port 50389 --bindDN " + \
    '"cn=Directory Manager"' + " --bindPassword harshit123 --filename " + file_name

result4 = subprocess.run(ldap_command, shell=True,
                         capture_output=True, cwd="/usr/ssosec/config/opends/bin")
print(result4)
print("\n\nAdding user to realm\n")


#ADDING user to newly created realm
#curl --request POST --header "iPlanetDirectoryPro: AQIC5wM2LY4SfczIpGCSYjzLfP7xLgfFDZrj3OlO7xWKh6k.*AAJTSQACMDEAAlNLABQtNDUxNTg4MDkwOTY4MjA2MDc5MQACUzEAAA..*" --header "Content-Type: application/json" --data '{"realm":"test","username": "user","userpassword": "user12345","mail": "user@ssosec.com"}' "https://admin.harshit3030.xyz:8443/ctrl/json/realms/test/users/?_action=create"
#r = realm_name
realm_name = '"' + realm_name + '"'

#user creds starts here
user_name = "user1"
user_name = '"' + user_name + '"'
user_password = "password123"
user_password = '"' + user_password + '"'
user_mail = "user@ssosec.com"
user_mail = '"' + user_mail + '"'
#user creds ends here


x = '{"realm":'+'"' + r+'"' + ',"username":' + user_name + \
    ',"userpassword":' + user_password + ',"mail":' + user_mail + '}'
user_api = "curl --request POST --header "+"\"iPlanetDirectoryPro: "+token + "\"" + " --header " + "\"Content-Type: application/json\"" + \
    " --data " + "'" + x + "'" + " \"https://"+pre + \
    ".harshit3030.xyz:8443/ctrl/json/realms/" + r + "/users/?_action=create\""
result_user = subprocess.run(user_api, shell=True, capture_output=True)
print(result_user)
#json/realms/test/users/?_action=create


# Adding FQDN mappings in https://admin.harshit3030.xyz:8443/ctrl/json/global-config/servers/01/properties/advanced
# GET Advanced default values
get_adv = "curl --request GET --header "+"\"iPlanetDirectoryPro: "+token + "\"" + " --header " + "\"Content-Type: application/json\"" + \
    " --header 'Accept-API-Version: resource=1.0,protocol=1.0'" + " \"https://"+pre + \
    ".harshit3030.xyz:8443/ctrl/json/global-config/servers/01/properties/advanced\""

result5 = subprocess.run(get_adv, shell=True, capture_output=True)
json_string = result5.stdout
json_object = json.loads(json_string)
# add fqdn to dictionary
#property_name = "com.sun.identity.server.fqdnMap["+alias+"]"
#property_name = property_name.strip('"')
#property_value = realm_name.strip('"') + ".harshit3030.xyz"

alias = realm_name.strip('"') + ".harshit3030.xyz"
property_name = "com.sun.identity.server.fqdnMap["+alias+"]"
property_name = property_name.strip('"')
property_value = realm_name.strip('"') + ".harshit3030.xyz"
d = {property_name: property_value}
json_object.update(d)
#print(property_name)
#print(property_value)

#json_object.update(property_name = property_value)

json_object_final = json.dumps(json_object, indent=2)
#print(json_object_final)
put_adv = "curl --request PUT --header "+"\"iPlanetDirectoryPro: "+token + "\"" + " --header " + "\"Content-Type: application/json\"" + \
    " --header 'Accept-API-Version: resource=1.0,protocol=1.0'" + " --data " + "\'" + json_object_final + "\'" + " \"https://"+pre + \
    ".harshit3030.xyz:8443/ctrl/json/global-config/servers/01/properties/advanced\""

result6 = subprocess.run(put_adv, shell=True, capture_output=True)
print(result6)

print(property_value)
