# Cremer_assignment4.py
# COSC 1352 — Assignment 4 GUI
# Name: Alexander Cremer
#

from tkinter import *
from tkinter import messagebox

# -----------------------------
# Product classes (DO NOT CHANGE)
# -----------------------------

class Product:
    def __init__(self, name, price):
        self._name = name
        self._price = float(price)
        self._category = "General"

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_category(self):
        return self._category

    def final_price(self):
        return self._price

    def __str__(self):
        return f"{self._name} ({self._category}) - ${self._price:.2f}"


class FoodProduct(Product):
    def __init__(self, name, price):
        Product.__init__(self, name, price)
        self._category = "Food"

    def final_price(self):
        return self.get_price()  # 0% tax


class BeverageProduct(Product):
    def __init__(self, name, price):
        Product.__init__(self, name, price)
        self._category = "Beverage"

    def final_price(self):
        return self.get_price() * 1.05  # 5% tax


class SnackProduct(Product):
    def __init__(self, name, price):
        Product.__init__(self, name, price)
        self._category = "Snack"

    def final_price(self):
        return self.get_price() * 1.08  # 8% tax


# -----------------------------
# Data (lists only — DO NOT CHANGE)
# -----------------------------

FOOD_NAMES = ["Bread", "Rice", "Pasta", "Apples", "Eggs"]
FOOD_PRICES = [2.00, 1.50, 1.20, 0.80, 3.00]

BEVERAGE_NAMES = ["Water", "Juice", "Soda", "Coffee", "Tea"]
BEVERAGE_PRICES = [1.00, 3.00, 2.50, 4.00, 2.00]

SNACK_NAMES = ["Chips", "Cookies", "Chocolate", "Nuts", "Popcorn"]
SNACK_PRICES = [1.50, 2.20, 1.80, 3.50, 1.25]


def money(value):
    return f"${value:.2f}"


# -----------------------------
# GUI
# -----------------------------

class ShopGUI:
    def __init__(self):
        
        self.window = Tk()
        self.window.title("Shopping Basket GUI")
        self.window.attributes("-fullscreen", True)

        # 0 Food, 1 Beverage, 2 Snack
        self.selected_category_index = 0
        # 0..4
        self.selected_item_index = 0

        # Basket stores Product objects (one per unit added)
        self.basket_products = []

        # ---- Layout (3 simple columns) ----
        self.frame_cat = Frame(self.window, padx=10, pady=10)
        self.frame_items = Frame(self.window, padx=10, pady=10)
        self.frame_basket = Frame(self.window, padx=10, pady=10)

        self.frame_cat.grid(row=0, column=0, sticky="n")
        self.frame_items.grid(row=0, column=1, sticky="n")
        self.frame_basket.grid(row=0, column=2, sticky="n")

        # ---- Category Listbox ----
        Label(self.frame_cat, text="Categories").pack()
        self.category_listbox = Listbox(self.frame_cat, height=3)
        self.category_listbox.pack(pady=5)
        self.category_listbox.insert(END, "Food")
        self.category_listbox.insert(END, "Beverage")
        self.category_listbox.insert(END, "Snack")
        self.category_listbox.bind("<<ListboxSelect>>", self.on_category_select)

        # ---- Items Listbox ----
        Label(self.frame_items, text="Items").pack()
        self.items_listbox = Listbox(self.frame_items, height=6, width=25)
        self.items_listbox.pack(pady=5)
        self.items_listbox.bind("<<ListboxSelect>>", self.on_item_select)

        # ---- Quantity ----
        Label(self.frame_items, text="Quantity").pack(anchor="w")
        self.qty_entry = Entry(self.frame_items, width=10)
        self.qty_entry.pack(anchor="w", pady=5)

        # ---- Buttons ----
        Button(self.frame_items, text="Add", width=12, command=self.add_to_basket).pack(anchor="w", pady=(5, 2))
        Button(self.frame_items, text="Checkout", width=12, command=self.checkout).pack(anchor="w", pady=2)

        # ---- Basket Listbox ----
        Label(self.frame_basket, text="Basket").pack()
        self.basket_listbox = Listbox(self.frame_basket, height=12, width=30)
        self.basket_listbox.pack(pady=5)

        # ---- Total Label ----
        self.total_label = Label(self.frame_basket, text="Total: $0.00")
        self.total_label.pack(pady=(5, 0))

        # Default selections
        self.category_listbox.selection_set(0)
        # TODO: load Food items into items_listbox
        self.load_items(0)
        self.items_listbox.selection_set(0)

        self.window.mainloop()

    # -----------------------------
    # TODO methods students complete
    # -----------------------------

    def on_category_select(self, event):
        """When a category is selected, update selected_category_index and reload items."""
        # TODO:
        sel = self.category_listbox.curselection()
        print(self.category_listbox.curselection())
        if sel:
            #switches sel to a certian index telling us which category we are on
           self.selected_category_index = sel[0]
           self.load_items(self.selected_category_index)
           self.items_listbox.selection_set(0)
           self.selected_item_index = 0
        pass

    def on_item_select(self, event):
        """When an item is selected, update selected_item_index."""
        # TODO:jkndklfvmlkd
        # updates item index to match the selection made
        sel = self.items_listbox.curselection()
        if sel == True:
           self.selected_item_index = sel[0]
        pass

    def load_items(self, cidx):
        """Load the 5 items for category cidx into items_listbox."""
        # TODO:
        self.items_listbox.delete(0, END) #resets everything in the item listbox 
        print("switch")

        for i in range(0,5): # sets name and prices of items to match the correct cidx
            if cidx == 0:
                self.items_listbox.insert(END, "" + str((i+1)) + ") " + FOOD_NAMES[i] + " - $" + str(format(FOOD_PRICES[i],".2f")))
            elif cidx == 1:
                self.items_listbox.insert(END, "" + str((i+1)) + ") " + BEVERAGE_NAMES[i] + " - $" + str(format(BEVERAGE_PRICES[i],".2f")))
            elif cidx == 2:
                self.items_listbox.insert(END, "" + str((i+1)) + ") " + SNACK_NAMES[i] + " - $" + str(format(SNACK_PRICES[i],".2f")))

            pass
        pass

    def get_quantity(self):
        """Return quantity as int, or None if invalid (<=0)."""
        # TODO:
        qty = int(self.qty_entry.get()) #check to see if the ammount of the product is valid
        if qty <= 0 or str(qty) == None:
            messagebox.showinfo("error", "Please enter a valid integer")

        else:
            print(qty)
            return qty
        # else: return qty
        return None

    def create_product(self, cidx, iidx):
        """Create and return the correct Product object based on category and item index."""
        # TODO:

        if cidx == 0: #uses product functions to get the name and price of items
            name = FOOD_NAMES[cidx]
            price = FOOD_PRICES[iidx]
            return FoodProduct(name, price)
        elif cidx == 1:
            name = BEVERAGE_NAMES[cidx]
            price = BEVERAGE_PRICES[iidx]
            return BeverageProduct(name, price)
        elif cidx == 2:
            name = SNACK_NAMES[cidx]
            price = SNACK_PRICES[iidx]
            return SnackProduct(name, price)

        return NONE

    def compute_total(self):
        total = 0.0
        """Sum final_price() for all Product objects in basket_products."""
        # TODO: loop over self.basket_products and sum p.final_price()

        #calculates the total price based on the basket products list
        for p in self.basket_products:
            total += p.final_price()

        return total

    def update_total_label(self):
        """Update the total label with two decimals."""
        # TODO:
        #updates the "total" label
        total = self.compute_total()
        self.total_label.config(text=f"Total: ${total:.2f}")
        pass

    def add_to_basket(self):
        """Add selected item quantity times and update basket display + total."""
        # TODO:
        # 1) qty = self.get_quantity(); if None return
        qty = self.get_quantity()
        if qty == None:
            return
        # 2) cidx/iidx from saved selection
        cidx = self.selected_category_index
        iidx = self.selected_item_index
        # 3) p = self.create_product(cidx, iidx)
        p = self.create_product(cidx, iidx)
        # 4) append p (or a new one) qty times into self.basket_products
        for i in range(qty):
            self.basket_products.append(self.create_product(cidx, iidx))
        # 5) add ONE line to basket_listbox: "<name> (<category>) x<qty>"
        name = p.get_name()
        category = p.get_category()
        self.basket_listbox.insert(END, f"{name} ({category}) x{qty}")
        # 6) clear qty_entry and call update_total_label()
        self.qty_entry.delete(0, END)
        self.update_total_label()
        pass

    def checkout(self):
        """Show receipt in a messagebox."""
        # TODO:
        # If basket is empty:
        if len(self.basket_products) == 0:
            messagebox.showinfo("Receipt", "Basket is empty\n\nTotal: $0.00")
            return


        receipt = "---RECEIPT---\n" #formats adn sets up the receipt 
        for i in range(self.basket_listbox.size()):
            receipt += self.basket_listbox.get(i) + "\n"

        receipt += f"Total: {money(self.compute_total())}"

        messagebox.showinfo("Receipt", receipt)
        pass

ShopGUI()
