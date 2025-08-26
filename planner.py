import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import os
import calendar

# ---------------------

STOREFILE = "planner.txt"
FONT_FAMILY = "Consolas" # mid font
BG_COLOR = "#1a1a1a"    # Dark background coz dark mode
FRAME_COLOR = "#2c2c2c"    # Darker frame color
BUTTON_COLOR = "#00ff00" # green
BUTTON_TEXT_COLOR = "#000000" # Black text for buttons
COMPLETED_COLOR = "#87ceeb" # Sky blue for completed tasks
DELETE_COLOR = "#ff0000" # Red for delete button
HIGHLIGHT_COLOR = "#333333" # highlight for selection
URGENT_COLOR = "#ffa500" # Orange for urgent tasks
CRITICAL_COLOR = "#ff4500" # Red-orange for critical tasks
#-------------------


# date picker popup class
class DatePopup(tk.Toplevel):
    def __init__(self, master, date_entry):
        super().__init__(master)
        self.date_entry = date_entry
        self.title("Select Due Date")
        self.grab_set()
        self.transient(master)

        style = ttk.Style()
        style.configure('TFrame', background=FRAME_COLOR)
        style.configure('TLabel', background=FRAME_COLOR, foreground=BUTTON_COLOR, font=(FONT_FAMILY, 14))
        style.configure('TButton', font=(FONT_FAMILY, 10, 'bold'), background=BUTTON_COLOR, foreground=BUTTON_TEXT_COLOR, borderwidth=0, relief='flat')
        style.map('TButton', background=[('active', '#00cc00')])

        self.cal_date = datetime.now().date()
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=10, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(main_frame, style='TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(header_frame, text="<", command=self.previous_month).pack(side=tk.LEFT)
        self.month_year_label = ttk.Label(header_frame, text=self.cal_date.strftime("%B %Y"), font=(FONT_FAMILY, 14, 'bold'), foreground=BUTTON_COLOR)
        self.month_year_label.pack(side=tk.LEFT, expand=True)
        ttk.Button(header_frame, text=">", command=self.next_month).pack(side=tk.LEFT)

        self.cal_frame = ttk.Frame(main_frame, style='TFrame')
        self.cal_frame.pack(fill=tk.BOTH, expand=True)

        self.update_calendar()
        
    def update_calendar(self):
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        self.month_year_label.config(text=self.cal_date.strftime("%B %Y"))
        
        cal = calendar.Calendar()
        
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days_of_week):
            ttk.Label(self.cal_frame, text=day, font=(FONT_FAMILY, 12, 'bold'), foreground=BUTTON_COLOR).grid(row=1, column=i, padx=5, pady=5)

        cal_days = cal.monthdatescalendar(self.cal_date.year, self.cal_date.month)
        for week_index, week in enumerate(cal_days):
            for day_index, day_obj in enumerate(week):
                if day_obj.month == self.cal_date.month:
                    btn = ttk.Button(self.cal_frame, text=str(day_obj.day), command=lambda d=day_obj: self.select_date(d))
                    btn.grid(row=week_index + 2, column=day_index, padx=5, pady=5)
                else:
                    ttk.Label(self.cal_frame, text=str(day_obj.day), foreground="#555555").grid(row=week_index + 2, column=day_index, padx=5, pady=5)
    def previous_month(self):
        self.cal_date = self.cal_date.replace(day=1) - timedelta(days=1)
        self.update_calendar()

    def next_month(self):
        if self.cal_date.month == 12:
            self.cal_date = self.cal_date.replace(year=self.cal_date.year + 1, month=1, day=1)
        else:
            self.cal_date = self.cal_date.replace(month=self.cal_date.month + 1, day=1)
        self.update_calendar()

    def select_date(self, selected_date):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, selected_date.strftime("%d-%m-%Y"))
        self.destroy()



# Planner App Class
class PlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Planner App")
        self.root.geometry("800x900")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        # centered window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.homeworks = []
        self.load_homeworks()
        self.create_widgets()
        self.populate_listbox()
    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR, foreground=BUTTON_COLOR, font=(FONT_FAMILY, 14))
        style.configure('TButton', font=(FONT_FAMILY, 12, 'bold'), background=BUTTON_COLOR, foreground=BUTTON_TEXT_COLOR, borderwidth=0, relief='flat')
        style.map('TButton', background=[('active', '#00cc00')])
        
        style.configure('Delete.TButton', background=DELETE_COLOR)
        style.map('Delete.TButton', background=[('active', '#cc0000')])

        style.configure('TEntry', fieldbackground=FRAME_COLOR, foreground=BUTTON_COLOR, insertbackground=BUTTON_COLOR)
        
        main_frame = ttk.Frame(self.root, padding="30", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title_label = ttk.Label(main_frame, text="My Planner", font=(FONT_FAMILY, 28, 'bold'), background=BG_COLOR, foreground=BUTTON_COLOR)
        title_label.pack(pady=(0, 30))

        input_frame = ttk.Frame(main_frame, style='TFrame')
        input_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(input_frame, text="Task/Event Title:", foreground=BUTTON_COLOR).pack(anchor='w', pady=(0, 5))
        self.title_entry = ttk.Entry(input_frame, font=(FONT_FAMILY, 16), style='TEntry')
        self.title_entry.pack(fill=tk.X, ipady=5)

        date_frame = ttk.Frame(input_frame, style='TFrame')
        date_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Label(date_frame, text="Due Date (DD-MM-YYYY):", foreground=BUTTON_COLOR).pack(side=tk.LEFT, anchor='w', padx=(0, 10))
        self.date_entry = ttk.Entry(date_frame, font=(FONT_FAMILY, 16), style='TEntry')
        self.date_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        date_button = ttk.Button(date_frame, text="📅", command=lambda: DatePopup(self.root, self.date_entry))
        date_button.pack(side=tk.LEFT, padx=(10, 0), ipadx=10, ipady=5)

        add_button = ttk.Button(main_frame, text="Add to Planner", command=self.add_homework)
        add_button.pack(pady=(20, 0), ipadx=10, ipady=5)
        
        list_frame = ttk.Frame(main_frame, style='TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        self.homework_treeview = ttk.Treeview(
            list_frame,
            columns=("Due Date", "Task/Event"),
            show="headings",
            selectmode="browse"
        )
        self.homework_treeview.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.homework_treeview.yview)
        self.homework_treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.homework_treeview.heading("Due Date", text="Due Date")
        self.homework_treeview.heading("Task/Event", text="Task/Event")
        self.homework_treeview.column("Due Date", width=120, stretch=False)
        self.homework_treeview.column("Task/Event", stretch=True)

        self.homework_treeview.tag_configure("completed", foreground=COMPLETED_COLOR, font=(FONT_FAMILY, 14, 'overstrike'))
        self.homework_treeview.tag_configure("incomplete", foreground=BUTTON_COLOR, font=(FONT_FAMILY, 14))
        self.homework_treeview.tag_configure("urgent", foreground=URGENT_COLOR, font=(FONT_FAMILY, 14, 'bold'))
        self.homework_treeview.tag_configure("critical", foreground=CRITICAL_COLOR, font=(FONT_FAMILY, 14, 'bold'))

        style.configure("Treeview", background=FRAME_COLOR, fieldbackground=FRAME_COLOR, foreground=BUTTON_COLOR, font=(FONT_FAMILY, 14), borderwidth=0)
        style.configure("Treeview.Heading", background=FRAME_COLOR, foreground=BUTTON_COLOR, font=(FONT_FAMILY, 14, 'bold'))
        style.map("Treeview", background=[('selected', HIGHLIGHT_COLOR)], foreground=[('selected', BUTTON_COLOR)])

        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.pack(fill=tk.X, pady=(15, 0))

        delete_button = ttk.Button(button_frame, text="Delete", command=self.remove_homework, style='Delete.TButton')
        delete_button.pack(side=tk.LEFT, padx=(0, 5), ipadx=10, ipady=5)
        
        done_button = ttk.Button(button_frame, text="Mark as Done / Restore", command=self.toggle_completed)
        done_button.pack(side=tk.RIGHT, padx=(5, 0), ipadx=10, ipady=5)
        
        
    def add_homework(self):
        title = self.title_entry.get().strip()
        date_str = self.date_entry.get().strip()

        if not title or not date_str:
            messagebox.showerror("Error", "Please enter both a task/event title and a due date.")
            return
        try:
            due_date = datetime.strptime(date_str, "%d-%m-%Y").date()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid date in DD-MM-YYYY format.")
            return

        homework_item = {"title": title, "due_date": due_date, "completed": False}
        self.homeworks.append(homework_item)
        self.homeworks.sort(key=lambda x: (x['completed'], x['due_date']))
        self.save_homeworks()
        self.populate_listbox()

        self.title_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

    def remove_homework(self):
        try:
            selected_item = self.homework_treeview.selection()[0]
            index = self.homework_treeview.index(selected_item)
            item_text = self.homework_treeview.item(selected_item, "values")
            
            if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this item?\n\n{item_text[1]}"):
                del self.homeworks[index]
                self.save_homeworks()
                self.populate_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select an item to delete.")

    def toggle_completed(self):
        try:
            selected_item = self.homework_treeview.selection()[0]
            index = self.homework_treeview.index(selected_item)
            self.homeworks[index]["completed"] = not self.homeworks[index]["completed"]
            self.homeworks.sort(key=lambda x: (x['completed'], x['due_date']))
            self.save_homeworks()
            self.populate_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select an item to mark as done/restore.")

    def load_homeworks(self):
        if os.path.exists(STOREFILE):
            with open(STOREFILE, "r") as f:
                for line in f:
                    try:
                        title, date_str, completed_str = line.strip().split("|", 2)
                        due_date = datetime.strptime(date_str, "%d-%m-%Y").date()
                        completed = completed_str.lower() == 'true'
                        self.homeworks.append({"title": title, "due_date": due_date, "completed": completed})
                    except (ValueError, IndexError):
                        continue
            self.homeworks.sort(key=lambda x: (x['completed'], x['due_date']))

    def save_homeworks(self):
        with open(STOREFILE, "w") as f:
            for item in self.homeworks:
                f.write(f"{item['title']}|{item['due_date'].strftime('%d-%m-%Y')}|{item['completed']}\n")

    def populate_listbox(self):
        self.homework_treeview.delete(*self.homework_treeview.get_children())
        today = date.today()
        for item in self.homeworks:
            if item['completed']:
                tags = ("completed",)
            else:
                days_until_due = (item['due_date'] - today).days
                if days_until_due <= 0:
                    tags = ("critical",)
                elif days_until_due <= 7:
                    tags = ("urgent",)
                else:
                    tags = ("incomplete",)
            self.homework_treeview.insert(
                "",
                "end",
                values=(item['due_date'].strftime('%d-%m-%Y'), item['title']),
                tags=tags
            )
            
                
# --- Main execution block ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PlannerApp(root)
    root.mainloop()
