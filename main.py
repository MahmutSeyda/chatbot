import tkinter as tk
from tkinter import messagebox

class NotYoneticisiUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Profesyonel Öğrenci Not Takip Sistemi")
        self.root.geometry("450x600")
        self.root.config(bg="#f4f6f9")
        
        self.notlar = []

        # --- BAŞLIK ---
        baslik = tk.Label(root, text="Öğrenci Not Otomasyonu", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#2c3e50")
        baslik.pack(pady=15)

        # --- NOT GİRİŞ ALANI ---
        frame_giris = tk.Frame(root, bg="#f4f6f9")
        frame_giris.pack(pady=5)

        lbl_giris = tk.Label(frame_giris, text="Not Girin (0-100):", font=("Arial", 11), bg="#f4f6f9")
        lbl_giris.pack(side=tk.LEFT, padx=5)

        self.entry_not = tk.Entry(frame_giris, font=("Arial", 12), width=10)
        self.entry_not.pack(side=tk.LEFT, padx=5)
        self.entry_not.bind("<Return>", lambda event: self.not_ekle()) # Enter tuşuna basınca ekler

        btn_ekle = tk.Button(frame_giris, text="Ekle ➕", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", command=self.not_ekle)
        btn_ekle.pack(side=tk.LEFT, padx=5)

        # --- LİSTELEME ALANI ---
        frame_liste = tk.Frame(root, bg="#f4f6f9")
        frame_liste.pack(pady=10)

        lbl_liste = tk.Label(root, text="Girilen Notlar Listesi:", font=("Arial", 11, "bold"), bg="#f4f6f9", fg="#34495e")
        lbl_liste.pack(anchor="w", padx=30)

        self.listbox_notlar = tk.Listbox(root, font=("Arial", 11), width=42, height=8)
        self.listbox_notlar.pack(pady=5)

        # --- İŞLEM BUTONLARI ---
        frame_butonlar = tk.Frame(root, bg="#f4f6f9")
        frame_butonlar.pack(pady=10)

        btn_hesapla = tk.Button(frame_butonlar, text="📊 Raporla ve Hesapla", font=("Arial", 10, "bold"), bg="#3498db", fg="white", width=18, command=self.hesapla_ve_goster)
        btn_hesapla.grid(row=0, column=0, padx=5, pady=5)

        btn_sil = tk.Button(frame_butonlar, text="🗑️ Seçileni Sil", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", width=18, command=self.not_sil)
        btn_sil.grid(row=0, column=1, padx=5, pady=5)

        # --- SONUÇ / RAPOR PANELİ ---
        self.lbl_sonuc = tk.Label(root, text="Henüz rapor oluşturulmadı.", font=("Arial", 10), bg="white", fg="#2c3e50", relief="solid", bd=1, width=50, height=8, justify=tk.LEFT)
        self.lbl_sonuc.pack(pady=10)

    def not_ekle(self):
        giris_degeri = self.entry_not.get().strip()
        try:
            not_degeri = float(giris_degeri)
            if 0 <= not_degeri <= 100:
                self.notlar.append(not_degeri)
                self.listbox_notlar.insert(tk.END, f"Not: {not_degeri}")
                self.entry_not.delete(0, tk.END)
            else:
                messagebox.showerror("Hata", "Lütfen 0 ile 100 arasında bir sayı girin!")
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz karakter! Lütfen sayı giriniz.")

    def not_sil(self):
        try:
            secili_index = self.listbox_notlar.curselection()[0]
            self.listbox_notlar.delete(secili_index)
            del self.notlar[secili_index]
            messagebox.showinfo("Bilgi", "Seçilen not silindi.")
        except IndexError:
            messagebox.showwarning("Uyarı", "Lütfen silmek için listeden bir not seçin.")

    def harf_notu_hesapla(self, ort):
        if ort >= 85: return "AA (Mükemmel)"
        elif ort >= 70: return "BA (Çok İyi)"
        elif ort >= 60: return "BB (İyi)"
        elif ort >= 50: return "CB (Geçer)"
        else: return "FF (Kaldı)"

    def hesapla_ve_goster(self):
        if not self.notlar:
            messagebox.showwarning("Uyarı", "Hesaplama yapmak için en az bir not girmelisiniz!")
            return

        toplam = sum(self.notlar)
        ort = toplam / len(self.notlar)
        en_yuksek = max(self.notlar)
        en_dusuk = min(self.notlar)
        harf = self.harf_notu_hesapla(ort)
        durum = "Tebrikler, Geçtiniz! 🎉" if ort >= 50 else "Maalesef Kaldınız. ❌"

        rapor_metni = (
            f"  Adet: {len(self.notlar)}   |   Ortalama: {ort:.2f}\n"
            f"  En Yüksek: {en_yuksek}  |   En Düşük: {en_dusuk}\n"
            f"  Harf Notu: {harf}\n"
            f"  Durum: {durum}"
        )
        self.lbl_sonuc.config(text=rapor_metni)

        # Dosyaya otomatik kaydetme
        with open("masaustu_ogrenci_raporu.txt", "w", encoding="utf-8") as f:
            f.write("--- MASAÜSTÜ NOT RAPORU ---\n")
            f.write(f"Notlar: {self.notlar}\n")
            f.write(rapor_metni)

if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = NotYoneticisiUygulamasi(pencere)
    pencere.mainloop()