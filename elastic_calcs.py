
import tkinter as tk
from tkinter import ttk, messagebox
import math
import os
import sys

modules = ["K", "E", "G", "ν", "λ", "M", "ρ", "c_l", "c_s", "c_b"]
dimensioned = {"K", "E", "G", "λ", "M"}
velocity = {"c_l", "c_s", "c_b"}

unit_options = {
    "GPa": 1e9,
    "MPa": 1e6,
    "Pa": 1,
}

def normalize_number(value):
    return float(value.replace(",", "."))

def calculate_all(known):
    E = G = K = ν = λ = M = None
    if "E" in known and "G" in known:
        E, G = known["E"], known["G"]
        ν = E / (2 * G) - 1
        K = E / (3 * (1 - 2 * ν))
    elif "E" in known and "ν" in known:
        E, ν = known["E"], known["ν"]
        G = E / (2 * (1 + ν))
        K = E / (3 * (1 - 2 * ν))
    elif "K" in known and "G" in known:
        K, G = known["K"], known["G"]
        E = 9 * K * G / (3 * K + G)
        ν = E / (2 * G) - 1
    elif "K" in known and "ν" in known:
        K, ν = known["K"], known["ν"]
        E = 3 * K * (1 - 2 * ν)
        G = E / (2 * (1 + ν))
    elif "λ" in known and "G" in known:
        λ, G = known["λ"], known["G"]
        K = λ + 2 * G / 3
        E = G * (3 * λ + 2 * G) / (λ + G)
        ν = λ / (2 * (λ + G))
    elif "λ" in known and "ν" in known:
        λ, ν = known["λ"], known["ν"]
        G = λ * (1 - 2 * ν) / (2 * ν)
        K = λ * (1 + ν) / (3 * ν)
        E = G * 2 * (1 + ν)
    elif "G" in known and "ν" in known:
        G, ν = known["G"], known["ν"]
        E = 2 * G * (1 + ν)
        K = 2 * G * (1 + ν) / (3 * (1 - 2 * ν))
    elif "K" in known and "λ" in known:
        K, λ = known["K"], known["λ"]
        G = 1.5 * (K - λ)
        E = 9 * K * G / (3 * K + G)
        ν = E / (2 * G) - 1
    elif "K" in known and "E" in known:
        K, E = known["K"], known["E"]
        ν = (3 * K - E) / (6 * K)
        G = E / (2 * (1 + ν))
    else:
        raise ValueError("Не удалось вычислить параметры из выбранной пары.")

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

def update_table():
    try:
        p1, p2 = combo1.get(), combo2.get()
        u1, u2 = combo1_unit.get(), combo2_unit.get()

        if p1 == p2:
            raise ValueError("Выберите два разных параметра.")

        if p1 in dimensioned and p2 in dimensioned and u1 != u2:
            raise ValueError("Размерности параметров должны совпадать.")

        val1 = normalize_number(entry1.get())
        val2 = normalize_number(entry2.get())

        val1 *= unit_options.get(u1, 1) if p1 in dimensioned else 1
        val2 *= unit_options.get(u2, 1) if p2 in dimensioned else 1

        rho = normalize_number(entry_rho.get())
        if unit_rho.get() == "g/cm³":
            rho *= 1000  # г/см³ -> кг/м³

        known = {p1: val1, p2: val2}
        result = calculate_all(known)

        # Расчет скоростей
        G, K, M = result["G"], result["K"], result["M"]
        cl = (M / rho) ** 0.5
        cs = (G / rho) ** 0.5
        cb = (K / rho) ** 0.5

        result.update({
            "ρ": rho / 1000,  # для вывода
            "c_l": cl / 1000,
            "c_s": cs / 1000,
            "c_b": cb / 1000
        })

        output_unit = u1 if p1 in dimensioned else u2 if p2 in dimensioned else "GPa"
        output_div = unit_options.get(output_unit, 1)

        for i, key in enumerate(modules):
            val = result.get(key)
            if val is None:
                table_labels[i]["text"] = f"{key} = —"
            elif key in velocity:
                table_labels[i]["text"] = f"{key} = {val:.3f} kg/m³"
            elif key == "ρ":
                table_labels[i]["text"] = f"{key} = {val:.3f} g/cm³"
            elif key in dimensioned:
                table_labels[i]["text"] = f"{key} = {val / output_div:.3f} {output_unit}"
            else:
                table_labels[i]["text"] = f"{key} = {val:.5f}"

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

root = tk.Tk()
root.title("Elastic Calculator")

# Установка кастомной иконки
icon_path = os.path.join(os.path.dirname(sys.argv[0]), "icon_elastic.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

tk.Label(root, text="Плотность ρ:").grid(row=0, column=0, sticky="e")
entry_rho = tk.Entry(root)
entry_rho.grid(row=0, column=1)
unit_rho = ttk.Combobox(root, values=["kg/m³", "g/cm³"], width=6)
unit_rho.set("g/cm³")
unit_rho.grid(row=0, column=2)

tk.Label(root, text="1-й параметр:").grid(row=1, column=0, sticky="e")
combo1 = ttk.Combobox(root, values=modules[:-4])
combo1.grid(row=1, column=1)
entry1 = tk.Entry(root)
entry1.grid(row=1, column=2)
combo1_unit = ttk.Combobox(root, values=["GPa", "MPa", "Pa"], width=6)
combo1_unit.grid(row=1, column=3)

tk.Label(root, text="2-й параметр:").grid(row=2, column=0, sticky="e")
combo2 = ttk.Combobox(root, values=modules[:-4])
combo2.grid(row=2, column=1)
entry2 = tk.Entry(root)
entry2.grid(row=2, column=2)
combo2_unit = ttk.Combobox(root, values=["GPa", "MPa", "Pa"], width=6)
combo2_unit.grid(row=2, column=3)

def update_units(event=None):
    for combo, unit in [(combo1, combo1_unit), (combo2, combo2_unit)]:
        param = combo.get()
        if param in dimensioned:
            unit["state"] = "readonly"
            if not unit.get():
                unit.set("GPa")
        else:
            unit.set("")
            unit["state"] = "disabled"

combo1.bind("<<ComboboxSelected>>", update_units)
combo2.bind("<<ComboboxSelected>>", update_units)

btn_calc = tk.Button(root, text="Рассчитать", command=update_table)
btn_calc.grid(row=3, column=0, columnspan=4, pady=5)

table_labels = []
for i, mod in enumerate(modules):
    label = tk.Label(root, text=f"{mod} = —", anchor="w", width=40)
    label.grid(row=4+i, column=0, columnspan=4, sticky="w")
    table_labels.append(label)

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # для .exe
else:
    base_path = os.path.abspath(".")

icon_path = os.path.join(base_path, "icon_elastic.ico")
root.iconbitmap(icon_path)

root.mainloop()
