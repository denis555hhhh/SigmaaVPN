import glob, os

folder = r"C:\Users\Gnida222\Desktop\Сайт впн"
for path in glob.glob(os.path.join(folder, "*.html")):
    if "privacy.html" in path:
        continue
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace('<a href="#">Политика конфиденциальности</a>', '<a href="privacy.html">Политика конфиденциальности</a>')
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Updated:", os.path.basename(path))
print("Done")
