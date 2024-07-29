from DB_connection import connect_to_db, close_connection
from mysql.connector import Error

cart = []

class Functions:
    def __init__(self, connection):
        self.connection = connection

    def show_products(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            print("Products:")
            print("====================")
            for row in rows:
                print(f"id: {row[0]}")
                print(f"name: {row[1]}")
                print(f"price: {row[2]}$")
                print(f"description: {row[3]}")
                print("====================")
        except Error as e:
            print(f"Error: {e}")

    def order_products(self, id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM products WHERE id = {id}")
            rows = cursor.fetchall()
            if rows:
                print("\nProduct detail:")
                print("\n====================")
                for row in rows:
                    print(f"id: {row[0]}")
                    print(f"name: {row[1]}")
                    print(f"price: {row[2]}$")
                    print(f"description: {row[3]}")
                    print("====================\n")
                    cart.append(id)
                    print("* product added to cart *")
            else:
                print("product was not found..")
                return

        except Error as e:
            print(f"Error: {e}")

    def add_product(self, name, price, description):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO products (name, price, description) VALUES ('{name}', {price}, '{description}')")
            rows = cursor.fetchall()
            print(f"\nProduct Added! = {rows}")
        except Error as e:
            print(f"Error: {e}") 
 
    def show_cart(self, cart):
        try:
            print("\nProducts in Cart:")
            print("\n====================")
            for id in cart:
                cursor = self.connection.cursor()
                cursor.execute(f"SELECT * FROM products WHERE id = {id}")
                rows = cursor.fetchall()
                for row in rows:
                    print(f"id: {row[0]}")
                    print(f"name: {row[1]}")
                    print(f"price: {row[2]}$")
                    print(f"description: {row[3]}")
                    print("====================\n")

        except Error as e:
            print(f"Error: {e}")

    def delete_product(self, id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM products WHERE id = {id}")
            rows = cursor.fetchall()
            print(f"\nProduct Deleted! = {rows}")
        except Error as e:
            print(f"Error: {e}")

    def remove_product_from_cart(self, id):
        try:
            for item in cart:
                if int(item[0]) == id:
                    cart.remove(item)
                print(f"\nProduct Removed From Cart!")
        except Error as e:
            print(f"Error: {e}")

def main():
    connection = connect_to_db()
    if not connection:
        return
    
    func = Functions(connection)
    
    while True:
        print("\n1) Show products")
        print("2) Order a product")
        print("3) Add a product")
        print("4) Show Cart")
        print("5) Delete a product")
        print("6) Remove Product From Cart")
        print("7) Exit")
        user_input = int(input("Please Choose: "))
        match user_input:
            case 1:
                func.show_products()
            case 2:
                id = input("Please Enter product id: ")
                func.order_products(id)
            case 3:
                name = input("Please Enter product name: ")
                price = int(input("Please Enter product price: "))
                description = input("Please Enter product description: ")
                func.add_product(name, price, description)
            case 4:
                if not cart:
                    print("cart is empty.")
                    continue
                
                func.show_cart(cart)
            case 5:
                id = input("Enter the products id: ")
                print(f"are you sure you wanna delete product with id = {id}??")
                confirm = input("Are you sure you wanna delete? (y/n)")
                if confirm:
                    func.delete_product(id)
                else:
                    continue
            case 6:
                id = int(input("What product You wanna remove from your cart?: "))
                func.remove_product_from_cart(id)


            case 7:
                confirm = input("Are you sure you wanna quit? (y/n)")
                if confirm:
                    break
                else:
                    continue
            case _:
                print("Invalid option, please try again.")
    
    close_connection(connection)
    exit()

if __name__ == "__main__":
    main()
