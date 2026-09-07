import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


def setup_database():
    conn = sqlite3.connect('foodie.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            address TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            oid INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            membership TEXT,
            items INTEGER,
            price REAL,
            distance REAL,
            food_cost REAL,
            delivery_fee REAL,
            discount REAL,
            total REAL,
            status TEXT,
            order_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(cid)
        )
    ''')
    conn.commit()
    conn.close()


def save_order_to_db(name, phone, address, membership, items, price, distance,
                     food_cost, delivery_fee, discount, total):
    conn = sqlite3.connect('foodie.db')
    cursor = conn.cursor()
    cursor.execute('SELECT cid FROM customers WHERE name = ? AND phone = ?', (name, phone))
    res = cursor.fetchone()
    if res:
        cid = res[0]
    else:
        cursor.execute(
            'INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)',
            (name, phone, address)
        )
        cid = cursor.lastrowid

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO orders (
            customer_id, membership, items, price, distance, food_cost,
            delivery_fee, discount, total, status, order_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        cid, membership, items, price, distance, food_cost,
        delivery_fee, discount, total, 'Completed', current_time
    ))
    oid = cursor.lastrowid
    conn.commit()
    conn.close()
    return oid


def get_order_history():
    conn = sqlite3.connect('foodie.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.oid, c.name, o.membership, o.items, o.total,
               o.status, o.order_date
        FROM orders o
        JOIN customers c ON o.customer_id = c.cid
        ORDER BY o.order_date DESC
    ''')
    data = cursor.fetchall()
    conn.close()
    return data


class FoodieApp:
    def __init__(self, root):
        self.root = root
        self.root.title('FoodieExpress - Order System')
        self.root.geometry('950x720')
        self.root.configure(bg='#F5F0E8')
        setup_database()
        self.create_widgets()

    def create_widgets(self):
        header = tk.Frame(self.root, bg='#E8DEC9', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text='🍔 FoodieExpress', font=('Segoe UI', 24, 'bold'),
                 fg='#4A3728', bg='#E8DEC9').pack(pady=5)
        tk.Label(header, text='Order Management System', font=('Segoe UI', 11),
                 fg='#6B5240', bg='#E8DEC9').pack()

        split_frame = tk.Frame(self.root, bg='#F5F0E8', padx=20, pady=15)
        split_frame.pack(fill='both', expand=True)

        left_frame = tk.Frame(split_frame, bg='#FAF5ED', padx=15, pady=10,
                              relief='solid', borderwidth=1)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        tk.Label(left_frame, text='👤 Customer Details',
                 font=('Segoe UI', 12, 'bold'), bg='#FAF5ED', fg='#4A3728').grid(
                     row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))
        for row, label in [(1, 'Full Name:'), (2, 'Phone:'), (3, 'Address:')]:
            tk.Label(left_frame, text=label, bg='#FAF5ED', fg='#4A3728',
                     font=('Segoe UI', 10)).grid(row=row, column=0, sticky='e', pady=5)

        self.ent_name = tk.Entry(left_frame, width=28, font=('Segoe UI', 10))
        self.ent_name.grid(row=1, column=1, pady=5)
        self.ent_phone = tk.Entry(left_frame, width=28, font=('Segoe UI', 10))
        self.ent_phone.grid(row=2, column=1, pady=5)
        self.ent_addr = tk.Entry(left_frame, width=28, font=('Segoe UI', 10))
        self.ent_addr.grid(row=3, column=1, pady=5)

        tk.Label(left_frame, text='Membership:', bg='#FAF5ED', fg='#4A3728',
                 font=('Segoe UI', 10)).grid(row=4, column=0, sticky='e', pady=5)
        self.combo_mem = ttk.Combobox(
            left_frame, values=['Regular', 'Premium', 'VIP'],
            state='readonly', width=26
        )
        self.combo_mem.set('Regular')
        self.combo_mem.grid(row=4, column=1, pady=5)

        tk.Label(left_frame, text='📦 Order Details', font=('Segoe UI', 12, 'bold'),
                 bg='#FAF5ED', fg='#4A3728').grid(
                     row=5, column=0, columnspan=2, sticky='w', pady=(15, 10))

        tk.Label(left_frame, text='Select Food:', bg='#FAF5ED', fg='#4A3728',
                 font=('Segoe UI', 10)).grid(row=6, column=0, sticky='e', pady=5)
        self.combo_food = ttk.Combobox(
            left_frame,
            values=['Burger - Rs. 450', 'Pizza - Rs. 800', 'Pasta - Rs. 600',
                    'Salad - Rs. 350', 'Sandwich - Rs. 400'],
            state='readonly', width=26
        )
        self.combo_food.set('Burger - Rs. 450')
        self.combo_food.grid(row=6, column=1, pady=5)

        for row, label in [(7, 'Quantity:'), (8, 'Price (Rs.):'), (9, 'Distance (km):')]:
            tk.Label(left_frame, text=label, bg='#FAF5ED', fg='#4A3728',
                     font=('Segoe UI', 10)).grid(row=row, column=0, sticky='e', pady=5)

        self.ent_items = tk.Entry(left_frame, width=28, font=('Segoe UI', 10))
        self.ent_items.grid(row=7, column=1, pady=5)
        self.ent_price = tk.Entry(left_frame, width=28, font=('Segoe UI', 10))
        self.ent_price.grid(row=8, column=1, pady=5)
        self.ent_dist = tk.Entry(left_frame, width=28, font=('Segoe UI', 10))
        self.ent_dist.grid(row=9, column=1, pady=5)

        info_frame = tk.Frame(left_frame, bg='#FAF5ED', pady=10)
        info_frame.grid(row=10, column=0, columnspan=2)
        tk.Label(info_frame, text='Delivery Rate:', bg='#FAF5ED', fg='#4A3728',
                 font=('Segoe UI', 9)).pack(side='left', padx=(0, 5))
        tk.Label(info_frame, text='Rs. 50/km', bg='#FAF5ED', fg='#5A4A3A',
                 font=('Segoe UI', 9, 'bold')).pack(side='left', padx=(0, 15))
        tk.Label(info_frame, text='Free Delivery:', bg='#FAF5ED', fg='#4A3728',
                 font=('Segoe UI', 9)).pack(side='left', padx=(0, 5))
        tk.Label(info_frame, text='Orders > Rs. 5,000', bg='#FAF5ED', fg='#5A4A3A',
                 font=('Segoe UI', 9, 'bold')).pack(side='left')

        btn_frame = tk.Frame(left_frame, bg='#FAF5ED', pady=10)
        btn_frame.grid(row=11, column=0, columnspan=2, pady=(10, 0))
        buttons = [
            ('🧮 Calculate Bill', self.calculate_bill, 0, 0),
            ('💾 Save Order', self.save_order, 0, 1),
            ('📋 View Orders', self.view_history, 0, 2),
            ('🗑️ Clear', self.clear_fields, 1, 0),
            ('🚪 Logout', self.logout, 1, 1),
            ('❌ Exit', self.root.quit, 1, 2),
        ]
        for text, command, row, col in buttons:
            tk.Button(btn_frame, text=text, bg='#D8C5A0', fg='#000000',
                      font=('Segoe UI', 10, 'bold'), width=14, relief='raised',
                      borderwidth=2, command=command).grid(row=row, column=col,
                                                           padx=4, pady=4)

        right_frame = tk.Frame(split_frame, bg='#FAF5ED', padx=15, pady=10,
                               relief='solid', borderwidth=1)
        right_frame.pack(side='right', fill='both', expand=True)
        tk.Label(right_frame, text='📊 Order Summary', font=('Segoe UI', 14, 'bold'),
                 bg='#FAF5ED', fg='#4A3728').pack(anchor='w', pady=(0, 15))
        summary_grid = tk.Frame(right_frame, bg='#FAF5ED')
        summary_grid.pack(fill='both', expand=True, padx=10, pady=5)

        self.lbl_food = self._summary_label(summary_grid, 'Food Cost:', 0, 12)
        self.lbl_del = self._summary_label(summary_grid, 'Delivery Fee:', 1, 12)
        self.lbl_disc = self._summary_label(summary_grid, 'Discount:', 2, 12)
        tk.Frame(summary_grid, height=2, bg='#D8C5A0').grid(
            row=3, column=0, columnspan=2, pady=10, sticky='ew')
        self.lbl_total = self._summary_label(summary_grid, 'TOTAL PAYABLE:', 4, 16, True)
        self.lbl_status = self._summary_label(summary_grid, 'Status:', 5, 11)

    def _summary_label(self, parent, title, row, size, bold=False):
        font = ('Segoe UI', size, 'bold') if bold else ('Segoe UI', size)
        tk.Label(parent, text=title, bg='#FAF5ED', fg='#4A3728', font=font).grid(
            row=row, column=0, sticky='w', pady=8)
        default = 'Rs. 0.00' if title != 'Status:' else 'Pending'
        label = tk.Label(parent, text=default, bg='#FAF5ED', fg='#C0392B' if bold else '#4A3728', font=font)
        label.grid(row=row, column=1, sticky='e', pady=8)
        return label

    def calculate_bill(self):
        try:
            items = int(self.ent_items.get())
            price = float(self.ent_price.get())
            dist = float(self.ent_dist.get())
        except ValueError:
            messagebox.showerror('Error', 'Please enter valid numbers for Quantity, Price, and Distance.')
            return
        food_cost = items * price
        delivery_fee = 0 if food_cost > 5000 else dist * 50
        mem = self.combo_mem.get()
        discount = food_cost * (0.10 if mem == 'Premium' else 0.20 if mem == 'VIP' else 0)
        total = food_cost + delivery_fee - discount
        self.lbl_food.config(text=f'Rs. {food_cost:.2f}')
        self.lbl_del.config(text=f'Rs. {delivery_fee:.2f}')
        self.lbl_disc.config(text=f'Rs. {discount:.2f}')
        self.lbl_total.config(text=f'Rs. {total:.2f}')
        self.lbl_status.config(text='Calculated')

    def save_order(self):
        name, phone, addr = self.ent_name.get(), self.ent_phone.get(), self.ent_addr.get()
        if not name:
            messagebox.showerror('Error', 'Customer Name is required.')
            return
        try:
            items = int(self.ent_items.get())
            price = float(self.ent_price.get())
            dist = float(self.ent_dist.get())
        except ValueError:
            messagebox.showerror('Error', 'Invalid numbers in Order Details.')
            return
        food_cost = items * price
        delivery_fee = 0 if food_cost > 5000 else dist * 50
        mem = self.combo_mem.get()
        discount = food_cost * (0.10 if mem == 'Premium' else 0.20 if mem == 'VIP' else 0)
        total = food_cost + delivery_fee - discount
        oid = save_order_to_db(name, phone, addr, mem, items, price, dist,
                               food_cost, delivery_fee, discount, total)
        self.lbl_food.config(text=f'Rs. {food_cost:.2f}')
        self.lbl_del.config(text=f'Rs. {delivery_fee:.2f}')
        self.lbl_disc.config(text=f'Rs. {discount:.2f}')
        self.lbl_total.config(text=f'Rs. {total:.2f}')
        self.lbl_status.config(text=f'Saved (Order #{oid})')
        messagebox.showinfo('Success', f'Order #{oid} saved successfully!')

    def view_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title('Order History & Logs')
        history_window.geometry('850x450')
        history_window.configure(bg='#F5F0E8')
        cols = ('Order ID', 'Customer', 'Membership', 'Items', 'Total', 'Status', 'Date')
        tree = ttk.Treeview(history_window, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        scrollbar = ttk.Scrollbar(history_window, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True, padx=15, pady=15)
        scrollbar.pack(side='right', fill='y', pady=15)
        for row in get_order_history():
            tree.insert('', 'end', values=row)
        tk.Button(history_window, text='Close History', bg='#D8C5A0',
                  font=('Segoe UI', 10, 'bold'), width=15,
                  command=history_window.destroy).pack(pady=10)

    def clear_fields(self):
        for entry in (self.ent_name, self.ent_phone, self.ent_addr,
                      self.ent_items, self.ent_price, self.ent_dist):
            entry.delete(0, tk.END)
        self.combo_mem.set('Regular')
        self.combo_food.set('Burger - Rs. 450')
        self.lbl_food.config(text='Rs. 0.00')
        self.lbl_del.config(text='Rs. 0.00')
        self.lbl_disc.config(text='Rs. 0.00')
        self.lbl_total.config(text='Rs. 0.00')
        self.lbl_status.config(text='Pending')

    def logout(self):
        self.clear_fields()
        messagebox.showinfo('Logout', 'You have been logged out successfully.\nThe system is ready for the next staff member.')


if __name__ == '__main__':
    root = tk.Tk()
    app = FoodieApp(root)
    root.mainloop()
