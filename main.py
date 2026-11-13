import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from algorithms.sorting import quick_sort, merge_sort
from algorithms.searching import linear_search

SUBJECTS = ["Python", "DAA", "DBMS", "Java", "OS"]

class StudentResultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Analysis System")
        self.root.geometry("1120x720")
        self.root.minsize(980, 620)
        self.root.configure(bg="#f3f6fb")
        self.db = Database()
        self._style()
        self._build_ui()
        self.refresh_table()

    def _style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10),
                        background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background="#e8eef8", foreground="#24324a")
        style.map("Treeview", background=[("selected", "#dbeafe")],
                  foreground=[("selected", "#172554")])
        style.configure("TCombobox", padding=6)

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#172554", height=88)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Student Result Analysis System",
                 bg="#172554", fg="white", font=("Segoe UI", 22, "bold")).pack(
                     anchor="w", padx=24, pady=(15, 0))
        tk.Label(header, text="Manage student marks • Analyze results • Generate merit lists",
                 bg="#172554", fg="#cbd5e1", font=("Segoe UI", 10)).pack(
                     anchor="w", padx=26)

        body = tk.Frame(self.root, bg="#f3f6fb")
        body.pack(fill="both", expand=True, padx=20, pady=18)

        cards = tk.Frame(body, bg="#f3f6fb")
        cards.pack(fill="x", pady=(0, 14))
        self.total_var = tk.StringVar(value="0")
        self.avg_var = tk.StringVar(value="0.00%")
        self.topper_var = tk.StringVar(value="—")
        self._stat_card(cards, "TOTAL STUDENTS", self.total_var).pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._stat_card(cards, "CLASS AVERAGE", self.avg_var).pack(side="left", fill="x", expand=True, padx=8)
        self._stat_card(cards, "TOPPER", self.topper_var).pack(side="left", fill="x", expand=True, padx=(8, 0))

        content = tk.Frame(body, bg="#f3f6fb")
        content.pack(fill="both", expand=True)

        form = tk.Frame(content, bg="white", padx=16, pady=16,
                        highlightbackground="#dce3ee", highlightthickness=1)
        form.pack(side="left", fill="y", padx=(0, 14))
        tk.Label(form, text="Student Details", bg="white", fg="#172554",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 12))

        self.uid_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.marks_vars = [tk.StringVar() for _ in SUBJECTS]
        self._field(form, "Student UID", self.uid_var)
        self._field(form, "Student Name", self.name_var)
        for subject, var in zip(SUBJECTS, self.marks_vars):
            self._field(form, f"{subject} Marks (0–100)", var)

        btns = tk.Frame(form, bg="white")
        btns.pack(fill="x", pady=(12, 4))
        self._button(btns, "Add Student", self.add_student, "#2563eb").pack(fill="x", pady=3)
        self._button(btns, "Update Selected", self.update_student, "#0f766e").pack(fill="x", pady=3)
        self._button(btns, "Delete Selected", self.delete_student, "#dc2626").pack(fill="x", pady=3)
        self._button(btns, "Clear Form", self.clear_form, "#64748b").pack(fill="x", pady=3)

        right = tk.Frame(content, bg="#f3f6fb")
        right.pack(side="left", fill="both", expand=True)

        toolbar = tk.Frame(right, bg="white", padx=12, pady=12,
                           highlightbackground="#dce3ee", highlightthickness=1)
        toolbar.pack(fill="x", pady=(0, 12))
        tk.Label(toolbar, text="Search by UID or name", bg="white",
                 font=("Segoe UI", 9, "bold"), fg="#334155").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=22)
        search_entry.pack(side="left", padx=8)
        self._button(toolbar, "Search", self.search_student, "#2563eb").pack(side="left", padx=3)
        self._button(toolbar, "Show All", self.refresh_table, "#64748b").pack(side="left", padx=3)

        sortbar = tk.Frame(right, bg="white", padx=12, pady=10,
                           highlightbackground="#dce3ee", highlightthickness=1)
        sortbar.pack(fill="x", pady=(0, 12))
        tk.Label(sortbar, text="Sort using DAA:", bg="white",
                 font=("Segoe UI", 9, "bold"), fg="#334155").pack(side="left")
        self.sort_key = tk.StringVar(value="Percentage")
        ttk.Combobox(sortbar, textvariable=self.sort_key, state="readonly",
                     values=["Percentage", "Name", "UID"], width=13).pack(side="left", padx=8)
        self._button(sortbar, "Quick Sort", self.sort_quick, "#7c3aed").pack(side="left", padx=3)
        self._button(sortbar, "Merge Sort / Merit List", self.sort_merge, "#9333ea").pack(side="left", padx=3)

        table_frame = tk.Frame(right, bg="white", padx=10, pady=10,
                               highlightbackground="#dce3ee", highlightthickness=1)
        table_frame.pack(fill="both", expand=True)
        columns = ("uid", "name", "total", "percentage", "grade")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        headings = {"uid": "UID", "name": "Student Name", "total": "Total / 500",
                    "percentage": "Percentage", "grade": "Grade"}
        widths = {"uid": 100, "name": 190, "total": 110, "percentage": 115, "grade": 80}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")
        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        footer = tk.Frame(right, bg="#f3f6fb")
        footer.pack(fill="x", pady=(10, 0))
        self._button(footer, "Result Analysis", self.show_analysis, "#0f766e").pack(side="left")
        self._button(footer, "Reset Sorting", self.refresh_table, "#64748b").pack(side="left", padx=8)
        tk.Label(footer, text="Tip: select a row to edit or delete a student.",
                 bg="#f3f6fb", fg="#64748b", font=("Segoe UI", 9)).pack(side="right")

    def _stat_card(self, parent, title, variable):
        card = tk.Frame(parent, bg="white", padx=16, pady=12,
                        highlightbackground="#dce3ee", highlightthickness=1)
        tk.Label(card, text=title, bg="white", fg="#64748b",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(card, textvariable=variable, bg="white", fg="#172554",
                 font=("Segoe UI", 19, "bold")).pack(anchor="w", pady=(4, 0))
        return card

    def _field(self, parent, label, variable):
        tk.Label(parent, text=label, bg="white", fg="#334155",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 2))
        ttk.Entry(parent, textvariable=variable, width=27).pack(fill="x")

    def _button(self, parent, text, command, color):
        return tk.Button(parent, text=text, command=command, bg=color, fg="white",
                         activebackground=color, activeforeground="white",
                         relief="flat", cursor="hand2", padx=10, pady=7,
                         font=("Segoe UI", 9, "bold"))

    def _get_form_data(self):
        uid, name = self.uid_var.get().strip(), self.name_var.get().strip()
        if not uid or not name:
            raise ValueError("Please enter both Student UID and Student Name.")
        marks = []
        for subject, var in zip(SUBJECTS, self.marks_vars):
            raw = var.get().strip()
            try:
                mark = int(raw)
            except ValueError:
                raise ValueError(f"Enter a whole-number mark for {subject}.")
            if not 0 <= mark <= 100:
                raise ValueError(f"{subject} marks must be between 0 and 100.")
            marks.append(mark)
        total = sum(marks)
        percentage = total / len(SUBJECTS)
        grade = self._grade(percentage)
        return (uid, name, *marks, total, percentage, grade)

    @staticmethod
    def _grade(p):
        if p >= 90: return "A+"
        if p >= 80: return "A"
        if p >= 70: return "B"
        if p >= 60: return "C"
        if p >= 50: return "D"
        return "F"

    def add_student(self):
        try:
            data = self._get_form_data()
            self.db.add_student(data)
            self.clear_form()
            self.refresh_table()
            messagebox.showinfo("Success", "Student record added successfully.")
        except (ValueError, Exception) as e:
            messagebox.showerror("Unable to add student", str(e))

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select student", "Select a student record first.")
            return
        old_uid = self.tree.item(selected[0], "values")[0]
        try:
            data = self._get_form_data()
            self.db.update_student(old_uid, data)
            self.clear_form()
            self.refresh_table()
            messagebox.showinfo("Success", "Student record updated.")
        except Exception as e:
            messagebox.showerror("Unable to update student", str(e))

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select student", "Select a student record first.")
            return
        uid = self.tree.item(selected[0], "values")[0]
        if messagebox.askyesno("Confirm deletion", f"Delete student {uid}?"):
            self.db.delete_student(uid)
            self.clear_form()
            self.refresh_table()

    def clear_form(self):
        self.uid_var.set("")
        self.name_var.set("")
        for var in self.marks_vars:
            var.set("")
        self.tree.selection_remove(self.tree.selection())

    def refresh_table(self):
        self._display_records(self.db.get_all_students())

    def _display_records(self, records):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for s in records:
            self.tree.insert("", "end", values=(
                s["uid"], s["name"], s["total"], f'{s["percentage"]:.2f}%', s["grade"]))
        self._update_stats(records)

    def _update_stats(self, records):
        self.total_var.set(str(len(records)))
        self.avg_var.set(f'{sum(s["percentage"] for s in records)/len(records):.2f}%' if records else "0.00%")
        topper = max(records, key=lambda s: s["percentage"]) if records else None
        self.topper_var.set(topper["name"] if topper else "—")

    def on_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return
        uid = self.tree.item(selected[0], "values")[0]
        student = self.db.get_student(uid)
        if student:
            self.uid_var.set(student["uid"])
            self.name_var.set(student["name"])
            for var, key in zip(self.marks_vars, SUBJECTS):
                var.set(str(student[key.lower()]))

    def _sort_records(self):
        records = self.db.get_all_students()
        key = self.sort_key.get().lower()
        if key == "percentage":
            return records, lambda s: s["percentage"]
        if key == "name":
            return records, lambda s: s["name"].lower()
        return records, lambda s: s["uid"].lower()

    def sort_quick(self):
        records, key_fn = self._sort_records()
        sorted_records = quick_sort(records, key_fn)
        self._display_records(sorted_records)

    def sort_merge(self):
        records, key_fn = self._sort_records()
        sorted_records = merge_sort(records, key_fn)
        self._display_records(sorted_records)
        if records:
            messagebox.showinfo("Merit list", "Students sorted in ascending order. For a highest-marks-first merit list, choose Percentage and reverse the displayed order or use the topper analysis.")

    def search_student(self):
        query = self.search_var.get().strip().lower()
        if not query:
            messagebox.showwarning("Search", "Enter a UID or student name.")
            return
        records = self.db.get_all_students()
        found = linear_search(records, query)
        self._display_records(found)
        if not found:
            messagebox.showinfo("Search result", "No matching student found.")

    def show_analysis(self):
        records = self.db.get_all_students()
        if not records:
            messagebox.showinfo("Analysis", "Add student records to view analysis.")
            return
        avg = sum(s["percentage"] for s in records) / len(records)
        topper = max(records, key=lambda s: s["percentage"])
        passed = sum(1 for s in records if s["percentage"] >= 40)
        messagebox.showinfo(
            "Class Result Analysis",
            f"Total students: {len(records)}\n"
            f"Class average: {avg:.2f}%\n"
            f"Topper: {topper['name']} ({topper['percentage']:.2f}%)\n"
            f"Pass count (40% threshold): {passed}\n"
            f"Needs improvement: {len(records)-passed}"
        )

    def close(self):
        self.db.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentResultApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
