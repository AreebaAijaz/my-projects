import time
import json
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
try:
    import winsound
except ImportError:
    winsound = None

# Initialize Rich console
console = Console()

class OutOfStockError(Exception):
    def __str__(self):
        return "[red]Error: This item is out of stock.[/red]"
    
class InsufficientFundsError(Exception):
    def __str__(self):
        return "[red]Error: Your balance is insufficient. Please insert a coin.[/red]"

class InvalidProductId(Exception):
    def __str__(self):
        return "[red]Error: Invalid product selection.[/red]"

class Product:
    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

    def reduce_stock(self):
        if self.stock <= 0:
            raise OutOfStockError()
        self.stock -= 1

class VendingMachine:
    def __init__(self):
        self.data_file = "vending_data.json"
        if os.path.exists(self.data_file):
            self.load_data()
        else:
            self.products = [
                Product("Snacks", 1.50, 10),
                Product("Juice", 3.00, 10),
                Product("Water", 1.00, 10),
                Product("Biscuit", 1.25, 10)

            ]
            self.balance = 0.00
            self.save_data()

    def save_data(self):
        data = {
            "products": [
                {"name": p.name, "price": p.price, "stock": p.stock}
                for p in self.products
            ],
            "balance": self.balance
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        with open(self.data_file) as f:
            data = json.load(f)
            self.products = [
                Product(item["name"], item["price"], item["stock"])
                for item in data["products"]
            ]
            self.balance = data["balance"]        

    def play_sound(self, sound_type):
        if winsound:
            try:
                if sound_type == "coin":
                    winsound.Beep(800, 200)  # High pitch short beep
                    winsound.Beep(600, 200)  # Lower pitch short beep
                elif sound_type == "dispense":
                    winsound.Beep(500, 300)  # Mid pitch longer beep
                elif sound_type == "change":
                    for _ in range(3):
                        winsound.Beep(300, 100)  # Coin dropping sound
                        time.sleep(0.05)
                elif sound_type == "error":
                    winsound.Beep(200, 500)  # Low pitch error sound
            except:
                pass

    def insert_coin(self, amount):
        self.balance += amount
        self.save_data()
        self.play_sound("coin")

    def select_product(self, product_id):
        if product_id < 0 or product_id >= len(self.products):
            raise InvalidProductId()
    
        product = self.products[product_id]
        if product.stock <= 0:
            self.play_sound("error")
            raise OutOfStockError()
        if self.balance < product.price:
            self.play_sound("error")
            raise InsufficientFundsError()
    
        product.reduce_stock()
        self.balance -= product.price
        self.save_data()
        self.play_sound("dispense")
        return product

    def return_change(self):
        change = self.balance
        self.balance = 0.00
        self.save_data()
        if change > 0:
            self.play_sound("change")
        return change
    
    def show_products(self):
        console.print("\n[bold cyan]Available Products:[/bold cyan]")
        for i, product in enumerate(self.products):
            stock_color = "red" if product.stock <= 0 else "green"
            console.print(
                f"[yellow]{i+1}.[/yellow] [magenta]{product.name}[/magenta] - "
                f"[green]${product.price:.2f}[/green]  "
                f"[{stock_color}]({product.stock} left)[/{stock_color}]"
            )

def clear_screen():
    console.print("\n" * 5)

def main():
    machine = VendingMachine()

    while True:
        clear_screen()

        # Display UI - Keeping your ASCII art
        console.print("[bright_blue]╔══════════════════════════════╗[/bright_blue]")  
        console.print("[bright_blue]║[/bright_blue]       [bold]VENDING MACHINE[/bold]        [bright_blue]║[/bright_blue]")  
        console.print("[bright_blue]╠══════════════════════════════╣[/bright_blue]")  
        machine.show_products()  
        console.print(f"[bright_blue]║[/bright_blue] [cyan]Balance:[/cyan] [green]${machine.balance:.2f}[/green]               [bright_blue]║[/bright_blue]")  
        console.print("[bright_blue]╠══════════════════════════════╣[/bright_blue]")  
        console.print("[bright_blue]║[/bright_blue] [yellow][1-3][/yellow] Select Product         [bright_blue]║[/bright_blue]")  
        console.print("[bright_blue]║[/bright_blue] [yellow][C][/yellow] Insert Coin              [bright_blue]║[/bright_blue]")  
        console.print("[bright_blue]║[/bright_blue] [yellow][R][/yellow] Refund Money             [bright_blue]║[/bright_blue]")  
        console.print("[bright_blue]║[/bright_blue] [yellow][Q][/yellow] Quit                     [bright_blue]║[/bright_blue]")  
        console.print("[bright_blue]╚══════════════════════════════╝[/bright_blue]")  

        choice = input("\n>> ").upper()

        if choice == "Q":
            console.print("[bold yellow]Goodbye![/bold yellow]")
            break

        elif choice == "C":
            while True:
                console.print("\n[bold]Choose a coin:[/bold]")
                console.print("[cyan]1.[/cyan] $1.00    [cyan]2.[/cyan] $1.25    [cyan]3.[/cyan] $1.50")
                console.print("[cyan]4.[/cyan] $2.00    [cyan]5.[/cyan] $3.00    [cyan]6.[/cyan] $5.00")
                console.print("\n[yellow][M][/yellow] --> Back to the Menu")
                coin_choice = input("Select coin [1-6] or press M: ").upper()
        
                if coin_choice == "M":
                    break
                elif coin_choice in ["1", "2", "3", "4", "5", "6"]:
                    coins = [1.00, 1.25, 1.50, 2.00, 3.00, 5.00]
                    inserted_coin = coins[int(coin_choice) - 1]
                    machine.insert_coin(inserted_coin)
                    console.print(f"\n[green]✅ Successfully added ${inserted_coin:.2f} to your balance![/green]")
                    console.print("[cyan]You can shop now.[/cyan]")
                    time.sleep(2)
                    break
                else:
                    console.print("[red]❌ Invalid choice![/red]")
                    time.sleep(1)

        elif choice == "R":
            change = machine.return_change()
            console.print(f"[green]Returned ${change:.2f} change.[/green]")
            time.sleep(1)

        elif choice.isdigit():
            try:
                product = machine.select_product(int(choice) - 1)
                console.print(f"[green]Dispensing {product.name}... 🚀[/green]")
                time.sleep(1)
                change = machine.return_change()
                if change > 0:
                    console.print(f"\n[yellow]Returning ${change:.2f} change.[/yellow]")
                console.print("[bold green]THANK YOU FOR SHOPPING![/bold green]")
                user_input = input("\nPress Enter to Continue...  OR press 'q' to quit: ").lower()
                if user_input == "q":
                    break
            except InvalidProductId as e:
                console.print(str(e))
                time.sleep(1)
            except OutOfStockError as e:
                console.print(str(e))
                time.sleep(2)
            except InsufficientFundsError as e:
                console.print(str(e))
                time.sleep(2)
        else:
            console.print("[red]❌ Please enter a valid product number (1-3)![/red]")
            time.sleep(1)

if __name__ == "__main__":
    main()