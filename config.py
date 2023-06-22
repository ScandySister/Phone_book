host = '127.0.0.1'
user = 'root'
port = 3306
password = 'password'
db_name = 'phone_book'

'''
CREATE TABLE contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    image BLOB
);

CREATE TABLE phone_number (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contact_id INT NOT NULL,
    number INT(10) UNSIGNED NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES contact(id)
);
'''
