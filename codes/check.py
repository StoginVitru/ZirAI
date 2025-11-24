import os
from PIL import Image

base_path = "code/dataset"
broken_files = []
deleted_files = []
checked_files = []

banned_keywords = ["pngtree", "depositphotos", "stock", "watermark"]

for root, dirs, files in os.walk(base_path):
    for file in files:
        file_path = os.path.join(root, file)
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            checked_files.append(file_path)
            try:
                with Image.open(file_path) as img:
                    if img.mode in ("RGBA", "LA"):
                        deleted_files.append((file_path, "Прозорий фон"))
                        os.remove(file_path)
                        continue

                    if any(keyword in file.lower() for keyword in banned_keywords):
                        deleted_files.append((file_path, "Підозра на водяний знак"))
                        os.remove(file_path)
                        continue

                    img.verify()
            except Exception as e:
                broken_files.append((file_path, str(e)))
                try:
                    os.remove(file_path)
                except:
                    pass

report_path = "broken_images_report.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("📋 Перевірені файли:\n")
    for path in checked_files:
        f.write(f"  ✔️ {path}\n")

    f.write("\n")
    
    if deleted_files:
        f.write("🗑️ Видалені підозрілі файли:\n\n")
        for path, reason in deleted_files:
            f.write(f"{path}\n  → {reason}\n\n")
    else:
        f.write("✅ Підозрілих файлів не знайдено.\n\n")

    if broken_files:
        f.write("❌ Пошкоджені або некоректні файли зображень:\n\n")
        for path, error in broken_files:
            f.write(f"{path}\n  → {error}\n\n")
    else:
        f.write("✅ Усі зображення відкриваються коректно.\n")

print(f"✔️ Перевірку завершено. Звіт збережено у: {report_path}")
