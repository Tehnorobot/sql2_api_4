from werkzeug.security import generate_password_hash, check_password_hash
password = generate_password_hash('1')
print(password)
print(check_password_hash(password, '1'))