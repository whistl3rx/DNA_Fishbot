# Duet Night Abyss - Automatikus Halászat Bot

Ez a Python script automatikusan játsza a halászat minijátékot a **Duet Night Abyss** játékban. A bot detektálja a hal ikont és a kapszulát a képernyőn, majd automatikusan nyomja a Space gombot, amikor a hal a kapszulán belül van.

## 🎯 Funkciók

- **Automatikus hal ikon detektálás**: Több template használatával robusztus detektálás, még akkor is, ha a hal ikon elfordul
- **Kapszula pozíció követés**: Pontos kapszula detektálás
- **Intelligens Space gomb vezérlés**: Automatikusan nyomja/engedi a Space-t a hal pozíciója alapján (keyboard library használatával)
- **Debug mód**: Vizuális visszajelzés a detektált objektumokról
- **Magas FPS**: ~30 FPS vagy jobb teljesítmény
- **Biztonságos kilépés**: ESC gomb megnyomásával bármikor kiléphet

## 📦 Telepítés

1. **Függőségek telepítése**:
```bash
pip install -r requirements.txt
```

2. **Template képek előkészítése**:
   - Készítsd el a `templates/` mappát (ha még nem létezik)
   - **Hal ikon**: Mentsd el a hal sprite sheet-et `templates/fish.png` néven
     - A script automatikusan feldarabolja a 4x8-as rácsot 32 frame-re
     - Ha nincs sprite sheet, használhatsz egyedi template fájlokat is (`fish_1.png`, `fish_2.png`, stb.)
   - **Kapszula**: Mentsd el a kapszula képet `templates/capsule.png` néven

## 🖼️ Template képek készítése

### Hal ikon (`fish.png`) - Sprite Sheet (Ajánlott)
A játékfájlokból exportált hal ikon általában egy **4x8-as rács sprite sheet** (32 frame).

1. **Játékfájlokból exportálás** (lásd: `EXTRACT_FROM_GAME_FILES.md`):
   - Használd az UABE-t vagy AssetStudio-t
   - Exportáld a hal sprite sheet-et PNG formátumban
   - Mentsd el `templates/fish.png` néven

2. **A script automatikusan**:
   - Felismeri a 4x8-as rácsot
   - Feldarabolja 32 külön frame-re
   - Mind a 32 frame-et használja a template matching-hez

**Alternatíva**: Ha nincs sprite sheet, használhatsz egyedi template fájlokat:
- `fish.png` - alap template
- `fish_1.png`, `fish_2.png`, stb. - különböző szögek/frame-ek

### Kapszula (`capsule.png`)
1. **Játékfájlokból exportálás**:
   - Exportáld a kapszula képet PNG formátumban
   - Mentsd el `templates/capsule.png` néven

2. **Vagy képernyőképről**:
   - Használd az `extract_templates.py` eszközt
   - Interaktívan vágd ki a kapszulát

## ⚙️ Konfiguráció

A `main.py` fájl tetején található konfigurációs részben módosíthatod:

```python
# Képernyő régió koordinátái
SCREEN_REGION = {
    "top": 640,      # A régió felső sora
    "left": 3220,    # A régió bal oldala
    "width": 110,    # A régió szélessége
    "height": 820    # A régió magassága
}

# Template matching threshold (0.0 - 1.0)
FISH_THRESHOLD = 0.7
CAPSULE_THRESHOLD = 0.7

# FPS beállítás
TARGET_FPS = 30

# Debug mód
DEBUG_MODE = True
```

### Képernyő régió beállítása

1. Indítsd el a játékot és menj a halászat minijátékhoz
2. Használj egy képernyő koordináta eszközt (pl. Windows: Snipping Tool koordinátái)
3. Határozd meg a hal ikon és kapszula tartományát
4. Állítsd be a `SCREEN_REGION` értékeit

**Tipp**: A régió minél kisebb, annál gyorsabb a feldolgozás!

## 🚀 Használat

1. **Indítsd el a játékot** és menj a halászat minijátékhoz
2. **Futtasd a scriptet**:
```bash
python main.py
```

3. **3 másodperc van** a pozíció beállítására
4. A bot automatikusan elindul
5. **Nyomd meg az ESC gombot** a kilépéshez

## 🐛 Hibaelhárítás

### A bot nem találja a hal ikont
- Ellenőrizd, hogy a `templates/fish.png` létezik és helyes
- Csökkentsd a `FISH_THRESHOLD` értékét (pl. 0.6)
- Ellenőrizd, hogy a `SCREEN_REGION` koordinátái helyesek
- Használd a debug módot, hogy lásd, mit lát a bot

### A bot nem találja a kapszulát
- Ellenőrizd, hogy a `templates/capsule.png` létezik és helyes
- Csökkentsd a `CAPSULE_THRESHOLD` értékét
- Ellenőrizd a képernyő régió beállításait

### A bot túl lassú
- Csökkentsd a `SCREEN_REGION` méretét
- Növeld a `TARGET_FPS` értékét (de ne túl magasra, mert instabil lehet)
- Kisebb template képeket használj

### A Space gomb nem működik
- Ellenőrizd, hogy a játék ablak aktív
- Próbáld ki manuálisan, hogy a Space gomb működik-e a játékban
- Nézd meg, hogy nincs-e más program, ami blokkolja a billentyűzet bemenetet

## 📝 Megjegyzések

- A bot csak a megadott képernyő régiót figyeli
- A template matching grayscale módban működik a sebességért
- A bot automatikusan elengedi a Space gombot, ha nem talál halat vagy kapszulát
- A PyAutoGUI failsafe funkciója aktív: vigyétek az egeret a képernyő sarkába a vészhelyzeti leállításhoz

## ⚠️ Felelősség

Ez a script csak oktatási célokra készült. Használd saját felelősségre. A játék fejlesztői ellenőrizhetik az automatikus játékot, és akár bannolhatnak is.

## 📄 Licenc

Ez a projekt szabadon használható oktatási célokra.


