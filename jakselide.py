import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from compiler import compile_source, run_compiled_code

def run_code():
    source = editor.get("1.0", tk.END)
    try:
        python_code = compile_source(source)
        output = run_compiled_code(python_code)
    except Exception as e:
        output = f"Compile Error:\n{e}"

    console.delete("1.0", tk.END)
    console.insert(tk.END, output)

# --- UI ---
root = tk.Tk()
root.title("Jaksel Mini IDE")

editor = ScrolledText(root, height=15, font=("Consolas", 11))
editor.pack(fill=tk.BOTH, expand=True)

run_btn = tk.Button(root, text="▶ Run Jaksel", command=run_code)
run_btn.pack()

console = ScrolledText(root, height=10, bg="black", fg="lime", font=("Consolas", 11))
console.pack(fill=tk.BOTH, expand=True)

# Sample code
editor.insert(tk.END, """\
imo fib(n):
    yap n
END

yap fib(3)

""")

root.mainloop()
