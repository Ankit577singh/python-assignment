import re

def meets_minimum_length(password):
    return len(password) >= 10

def meets_character_variety(password):
    uppercase_count = sum(1 for c in password if c.isupper())
    lowercase_count = sum(1 for c in password if c.islower())
    digit_count = sum(1 for c in password if c.isdigit())
    special_count = sum(1 for c in password if c in '@#$%&*!')
    return uppercase_count >= 2 and lowercase_count >= 2 and digit_count >= 2 and special_count >= 2

def meets_sequence_and_repetition_restrictions(password, username):
    if username:
        for i in range(len(username) - 2):
            if username[i:i+3] in password:
                return False
    if re.search(r'(.)\1\1', password):
        return False
    return True

def meets_historical_password_check(password, last_three_passwords):
    return password not in last_three_passwords

def validate_password(password, username, last_three_passwords):
    if not meets_minimum_length(password):
        return False, "Password must be at least 10 characters long."
    if not meets_character_variety(password):
        return False, "Password must contain at least two uppercase letters, two lowercase letters, two digits, and two special characters."
    if not meets_sequence_and_repetition_restrictions(password, username):
        return False, "Password should not contain sequences from the username or repeating characters more than three times in a row."
    if not meets_historical_password_check(password, last_three_passwords):
        return False, "Password must not be the same as the last three passwords used."
    return True, "Password is valid."

def main():
    last_three_passwords = []
    username = input("Enter your username (press enter if none): ")
    
    while True:
        password = input("Enter your new password: ")
        is_valid, message = validate_password(password, username, last_three_passwords)
        if is_valid:
            print("Password updated successfully!")
            last_three_passwords.insert(0, password)
            if len(last_three_passwords) > 3:
                last_three_passwords.pop()
            break
        else:
            print("Password not valid:", message)

if __name__ == "__main__":
    main()
