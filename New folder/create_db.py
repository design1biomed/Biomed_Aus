import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Ajomon@5114'
    )
    
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS bmi_aus;")
        print("Database 'bmi_aus' created successfully.")
        
    connection.commit()
    connection.close()

except Exception as e:
    print(f"Failed to create database: {e}")
