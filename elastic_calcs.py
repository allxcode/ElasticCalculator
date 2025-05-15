
import tkinter as tk
from tkinter import ttk, messagebox
import math

def calculate_all(known):
    E, G, K, ν, λ, M = None, None, None, None, None, None

    if "E" in known and "G" in known:
        E = known["E"]
        G = known["G"]
        ν = E / (2 * G) - 1
        K = E / (3 * (1 - 2 * ν))
    elif "E" in known and "ν" in known:
        E = known["E"]
        ν = known["ν"]
        G = E / (2 * (1 + ν))
        K = E / (3 * (1 - 2 * ν))
    elif "K" in known and "G" in known:
        K = known["K"]
        G = known["G"]
        E = 9 * K * G / (3 * K + G)
        ν = E / (2 * G) - 1
    elif "K" in known and "ν" in known:
        K = known["K"]
        ν = known["ν"]
        E = 3 * K * (1 - 2 * ν)
        G = E / (2 * (1 + ν))

    if E is None or G is None or K is None or ν is None:
        raise ValueError("Не удалось вычислить все параметры. Проверьте введённые значения.")

    λ = K - 2 * G / 3
    M = λ + 2 * G

    return {
        "E": E,
        "G": G,
        "K": K,
        "ν": ν,
        "λ": λ,
        "M": M
    }

def compute_properties():
    try:
        rho = float(entry_rho.get())
        val1 = float(entry_val1.get())
        val2 = float(entry_val2.get())
        key1 = combo_val1.get()
        key2 = combo_val2.get()

        if key1 == key2:
            raise ValueError("Выберите два разных упругих модуля.")

        known = {key1: val1, key2: val2}
        results = calculate_all(known)

        G = results["G"]
        K = results["K"]
        M = results["M"]

        cl = math.sqrt(M / rho)
        cs = math.sqrt(G / rho)
        cb = math.sqrt(K / rho)

        output = ""
        for key, val in results.items():
            output += f"{key} = {val:.3e}\n"
        output += f"\nСкорости звука:\n"
        output += f"Продольная c_l = {cl:.2f} м/с\n"
        output += f"Поперечная c_s = {cs:.2f} м/с\n"
        output += f"Объёмная c_b = {cb:.2f} м/с\n"

        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, output)

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

root = tk.Tk()
root.title("Упругие свойства материала")

tk.Label(root, text="Плотность (ρ), кг/м³:").grid(row=0, column=0)
entry_rho = tk.Entry(root)
entry_rho.grid(row=0, column=1)

options = ["E", "G", "K", "ν"]

tk.Label(root, text="1-й модуль:").grid(row=1, column=0)
combo_val1 = ttk.Combobox(root, values=options)
combo_val1.grid(row=1, column=1)
entry_val1 = tk.Entry(root)
entry_val1.grid(row=1, column=2)

tk.Label(root, text="2-й модуль:").grid(row=2, column=0)
combo_val2 = ttk.Combobox(root, values=options)
combo_val2.grid(row=2, column=1)
entry_val2 = tk.Entry(root)
entry_val2.grid(row=2, column=2)

btn = tk.Button(root, text="Рассчитать", command=compute_properties)
btn.grid(row=3, column=0, columnspan=3)

text_output = tk.Text(root, height=15, width=60)
text_output.grid(row=4, column=0, columnspan=3)

root.mainloop()
