import pandas as pd

# 1. تحميل الداتا
# تأكد من المسار حسب اللي كتبته في الـ README
try:
    df = pd.read_csv("D:\مشاريع تحليل البيانات\pandas\Nasa\NASA-Exoplanet-Habitability\data~", comment='#')
except FileNotFoundError:
    print("❌ Error: clean_data.csv not found in data/ folder.")
    exit()

# 2. الفلتر الذهبي (Rocky + Habitable Zone)
# أضفنا فلتر الحرارة (pl_eqt) عشان نطابق الـ README
condition = (
    (df['pl_rade'] <= 2.0) &               # Filter I: Rocky
    (df['pl_eqt'] >= 273) & (df['pl_eqt'] <= 373) &  # Filter II: Thermal
    (df['pl_insol'] >= 0.5) & (df['pl_insol'] <= 1.5) # Filter III: Flux
)

final_candidates = df[condition].copy()

# 3. عرض النتائج النهائية بشكل منظم
print("\n" + "="*50)
print("🚀 NASA EXOPLANET HABITABILITY - FINAL RESULTS")
print("="*50)
print(f"Total Records Scanned: {len(df)}")
print(f"Candidates Isolated:   {len(final_candidates)}")
print("-" * 50)

if not final_candidates.empty:
    # عرض الأعمدة الأساسية فقط للوضوح
    cols = ['pl_name', 'hostname', 'st_spectype', 'pl_orbper', 'sy_dist']
    print(final_candidates[cols].sort_values('sy_dist'))
else:
    print("No candidates matched all criteria.")