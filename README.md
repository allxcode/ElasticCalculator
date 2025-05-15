# Elastic Calculator — это настольное Python-приложение с интерфейсом для расчёта упругих характеристик изотропного материала по двум известным параметрам.

- Ввод двух модулей упругости и плотности
- Автоматический пересчёт:
  - **E**, **G**, **K** и т.д.
  - Скоростей звука: продольной **Cl**, **Cs**, **Cb**
- Поддержка разных единиц:
  - GPa, MPa, Pa
  - Плотность: kg/m³ или g/cm³
- Удобный графический интерфейс на `tkinter`

Работает из коробки на Python 3.6+.

Используются только стандартные библиотеки:
- `tkinter`
- `math`
- `os`
- `sys`

![image](https://github.com/user-attachments/assets/862a9b9d-733e-43b4-aa26-e52feb023a16)
Поддержка ввода 2.54 и 2,54

---

## 📦 Установка и запуск

1. Склонируй репозиторий или скачай `.py` файл:

```bash
git clone https://github.com/yourname/elastic-calculator.git
cd elastic-calculator
```

2. Соберите
```bash
pyinstaller --onefile --windowed --icon=icon_elastic.ico --add-data "icon_elastic.ico;." ElasticCalculator.py
```
