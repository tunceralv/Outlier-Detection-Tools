# Outlier-Detection-Tools
Bu proje, veri analizi ve makine öğrenmesi çalışmalarında aykırı değer tespiti ve aykırı değer işlemlerini daha kolay ve tekrar kullanılabilir hale getirmek amacıyla geliştirilmiş bir Python modülüdür.

Modül sayesinde farklı projelerde aynı kodları tekrar tekrar yazmak yerine, gerekli fonksiyonlar import edilerek doğrudan kullanılabilir.

Özellikler

Bu modül aşağıdaki işlemleri gerçekleştirmek için kullanılabilir:

Sayısal değişkenler için boxplot oluşturma
IQR yöntemine göre alt ve üst aykırı değer sınırlarını hesaplama
Bir değişkende aykırı değer olup olmadığını kontrol etme
Aykırı gözlemleri ve aykırı olmayan gözlemleri ayırma
Aykırı değerleri alt ve üst sınırlar ile baskılama
Veri setindeki kategorik ve sayısal değişkenleri otomatik olarak belirleme
Kullanılan Teknolojiler
Python
Pandas
Seaborn
Matplotlib
Kullanım

Modülü projenize import ederek fonksiyonları kullanabilirsiniz.

from outlier_tools import (
    box_chart,
    outlier_thresholds,
    check_outlier,
    remove_outlier,
    replace_thresholds,
    grab_col_names
)
Boxplot Oluşturma
box_chart(df, "Age")
Aykırı Değer Sınırlarını Hesaplama
low_limit, up_limit = outlier_thresholds(df, "Age")

print(low_limit)
print(up_limit)
Aykırı Değer Kontrolü
check_outlier(df, "Age")

Fonksiyon, değişkende en az bir aykırı değer bulunuyorsa True, bulunmuyorsa False döndürür.

Aykırı Değerleri Ayırma
outliers, clean_df = remove_outlier(df, "Age")

Bu işlem sonucunda:

outliers: Aykırı gözlemleri içerir.
clean_df: Aykırı değer içermeyen gözlemleri içerir.
Aykırı Değerleri Baskılama
df = replace_thresholds(df, "Age")

Üst sınırdan büyük değerler üst sınır, alt sınırdan küçük değerler ise alt sınır ile değiştirilir.

Kullanılan Yöntem

Aykırı değer sınırlarının belirlenmesinde IQR (Interquartile Range) yöntemi kullanılmaktadır.

IQR = Q3 - Q1

Alt Sınır = Q1 - 1.5 × IQR

Üst Sınır = Q3 + 1.5 × IQR

Bu sınırların dışında kalan gözlemler potansiyel aykırı değer olarak değerlendirilir.

Projenin Amacı

Bu projenin temel amacı, veri ön işleme süreçlerinde sık kullanılan aykırı değer analizlerini modüler bir yapı altında toplamak ve farklı veri bilimi projelerinde tekrar kullanılabilir hale getirmektir.

Proje aynı zamanda Python'da fonksiyon geliştirme, modüler programlama ve yeniden kullanılabilir kod yazma konularında pratik yapmak amacıyla geliştirilmiştir.
