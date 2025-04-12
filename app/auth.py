import re



#                                             Authenticate User                                            #
############################################################################################################
def name_valid(name):
    if name.isalpha() and len(name) > 1:
        return True
    else:
        return False

def password_valid(pass1):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
	
	# compiling regex
    pat = re.compile(reg)
	
	# searching regex				
    mat = re.search(pat, pass1)
	
	# validating conditions
    if mat:
        return True
    else:
        return False

def password_check(password1, password2):
    if password1 == password2:
        return True
    else : 
        return False

def contact_valid(number):
    Pattern = re.fullmatch("[6-9][0-9]{9}",number)
    if Pattern != None:
        return True
    else:
        return False

def authentication(first_name, last_name, pass1, pass2, phone_number):
    if name_valid(first_name) == False:
        return "Invalid First Name"           
    elif name_valid(last_name) == False:
            return "Invalid Last Name"
    elif contact_valid(phone_number) == False:
            return "Invalid Phone Number"
    elif password_valid(pass1) == False:
        return "Password Should be in Proper Format. (eg. Password@1234)"
    elif password_check(pass1, pass2) == False:
        return "Password Not Matched"
    else:
        return "success"

#                                            Authenticate Input                                            #
############################################################################################################
def farmer_name_valid(full_name):
    res = full_name != '' and all(chr.isalpha() or chr.isspace() for chr in full_name)
    if res:
        return True
    else:
        return False

def ratio_valid(ratio):
    if int(ratio) >= 0 and int(ratio) <= 100:
        return True
    else:
        return False

def percentage_valid(percent):
    if float(percent) >= 0 and float(percent) <= 100:
        return True
    else:
        return False

def ph_valid(pH):
    if float(pH) >= 0 and float(pH) <= 14:
        return True
    else:
        return False

def rainfall_valid(mm):
    if float(mm) >= 0:
        return True
    else:
        return False

def input_verification(farmer_name, contact_no, n, p, k, temperature, humidity, ph, rainfall):
    if farmer_name_valid(farmer_name) == False:
        return "Invalid Farmer Name"
    elif contact_valid(contact_no) == False:
        return "Invalid Contact Number"
    elif ratio_valid(n) == False:
        return "Invalid ratio of Nitrogen content in soil"
    elif ratio_valid(p) == False:
        return "Invalid ratio of Phosphorous content in soil"
    elif ratio_valid(k) == False:
        return "Invalid ratio of Potassium content in soil"
    elif percentage_valid(temperature) == False:
        return "Invalid Temperature Value"
    elif percentage_valid(humidity) == False:
        return "Invalid Humidity Pecentage"
    elif ph_valid(ph) == False:
        return "Invalid pH Value"
    elif rainfall_valid(rainfall) == False:
        return "Invalid Rainfall (in mm)"
    else:
        return "Success"
    

def input_verification1(farmer_name, n, p, k, temperature, humidity, moisture):
    if farmer_name_valid(farmer_name) == False:
        return "Invalid Farmer Name"
    elif ratio_valid(n) == False:
        return "Invalid ratio of Nitrogen content in soil"
    elif ratio_valid(p) == False:
        return "Invalid ratio of Phosphorous content in soil"
    elif ratio_valid(k) == False:
        return "Invalid ratio of Potassium content in soil"
    elif percentage_valid(temperature) == False:
        return "Invalid Temperature Value"
    elif percentage_valid(humidity) == False:
        return "Invalid Humidity Pecentage"
    elif percentage_valid(moisture) == False:
        return "Invalid Moisture Pecentage"
    else:
        return "Success"