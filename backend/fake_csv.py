import csv
import random
from faker import Faker

# Initialize Faker to generate random data
fake = Faker('zh_CN')  # 'zh_CN' generates data in Chinese for more realistic fields

# Specify the number of rows to generate
num_rows = 1000

# Define the file name for the CSV output
output_file = 'xiaomi_com.csv'

# Generate data and write to CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write header
    writer.writerow(["id", "账户名", "密码", "email", "ip地址", "号码", "身份证号", "年龄", "月份", "年份", "姓氏"])
    
    for i in range(1, num_rows + 1):
        # Generate fake data for each field
        account_id = str(i)
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        ip_address = fake.ipv4()
        phone_number = fake.phone_number()
        id_number = fake.ssn()
        age = random.randint(18, 60)
        month = random.randint(1, 12)
        year = random.randint(1970, 2005)
        surname = fake.last_name()
        
        # Write row to CSV
        writer.writerow([account_id, username, password, email, ip_address, phone_number, id_number, age, month, year, surname])

print(f"Generated {num_rows} rows of sample data and saved to {output_file}.")
