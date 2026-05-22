import tkinter as tk
from tkinter import messagebox, simpledialog
from models import ensure_db, add_child, list_children, add_task, list_tasks, mark_task_done, list_transactions


def run_app():
    ensure_db()

    root = tk.Tk()
    root.title('Taschengeld-Verwaltung')
    root.geometry('800x500')

    # Left: children
    left = tk.Frame(root, padx=10, pady=10)
    left.pack(side=tk.LEFT, fill=tk.Y)

    tk.Label(left, text='Kinder').pack()
    child_listbox = tk.Listbox(left, width=25)
    child_listbox.pack(fill=tk.Y, expand=True)

    def refresh_children():
        child_listbox.delete(0, tk.END)
        for c in list_children():
            child_listbox.insert(tk.END, f"{c['id']}: {c['name']} (€{c['balance']:.2f})")

    def add_child_dialog():
        name = simpledialog.askstring('Neues Kind', 'Name:')
        if not name:
            return
        age = simpledialog.askinteger('Alter', 'Alter (optional):')
        add_child(name, age)
        refresh_children()

    tk.Button(left, text='Kind hinzufügen', command=add_child_dialog).pack(fill=tk.X)

    # Right: tasks and actions
    right = tk.Frame(root, padx=10, pady=10)
    right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(right, text='Aufgaben').pack()
    task_listbox = tk.Listbox(right)
    task_listbox.pack(fill=tk.BOTH, expand=True)

    def refresh_tasks():
        task_listbox.delete(0, tk.END)
        sel = child_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        item = child_listbox.get(idx)
        child_id = int(item.split(':', 1)[0])
        for t in list_tasks(child_id):
            task_listbox.insert(tk.END, f"{t['id']}: {t['title']} — €{t['amount']:.2f} {'(erledigt)' if t['done'] else ''}")

    def add_task_dialog():
        sel = child_listbox.curselection()
        if not sel:
            messagebox.showinfo('Info', 'Bitte zuerst ein Kind auswählen')
            return
        idx = sel[0]
        item = child_listbox.get(idx)
        child_id = int(item.split(':', 1)[0])
        title = simpledialog.askstring('Aufgabe', 'Titel:')
        if not title:
            return
        desc = simpledialog.askstring('Beschreibung', 'Beschreibung (optional):')
        amount = simpledialog.askfloat('Betrag', 'Betrag in Euro:', initialvalue=0.0)
        add_task(child_id, title, desc or '', amount or 0.0)
        refresh_tasks()

    def mark_done_action():
        sel_task = task_listbox.curselection()
        if not sel_task:
            return
        t_item = task_listbox.get(sel_task[0])
        task_id = int(t_item.split(':', 1)[0])
        if messagebox.askyesno('Bestätigen', 'Als erledigt markieren und auszahlen?'):
            mark_task_done(task_id, confirmed_by_parent=True)
            refresh_tasks()
            refresh_children()

    btn_frame = tk.Frame(right)
    btn_frame.pack(fill=tk.X)
    tk.Button(btn_frame, text='Aufgabe hinzufügen', command=add_task_dialog).pack(side=tk.LEFT)
    tk.Button(btn_frame, text='Als erledigt markieren', command=mark_done_action).pack(side=tk.LEFT)

    def on_child_select(evt):
        refresh_tasks()

    child_listbox.bind('<<ListboxSelect>>', on_child_select)

    refresh_children()

    root.mainloop()
