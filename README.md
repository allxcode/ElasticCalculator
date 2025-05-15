# Elastic Calculator — это настольное Python-приложение с интерфейсом для расчёта упругих характеристик изотропного материала по двум известным параметрам.

- Ввод двух модулей упругости и плотности
- Автоматический пересчёт:
  - \( E \), \( G \), \( K \), \( \nu \), \( \lambda \), \( M \)
  - Скоростей звука: продольной \( c_l \), поперечной \( c_s \), объемной \( c_b \)
- Поддержка разных единиц:
  - GPa, MPa, Pa
  - Плотность: кг/м³ или г/см³
- Удобный графический интерфейс на `tkinter`

Работает из коробки на Python 3.6+.

Используются только стандартные библиотеки:
- `tkinter`
- `math`
- `os`
- `sys`

---

## 📦 Установка и запуск

1. Склонируй репозиторий или скачай `.py` файл:

```bash
git clone https://github.com/yourname/elastic-calculator.git
cd elastic-calculator

2. Соберите
```bash
pyinstaller --onefile --windowed --icon=icon_elastic.ico --add-data "icon_elastic.ico;." ElasticCalculator.py
