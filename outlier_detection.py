import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor


def box_chart(dataframe,variable):
    """
    Belirtilen değişken için kutu grafiği oluşturur.

    Kutu grafiği; değişkenin dağılımını, medyanını, çeyreklerini
    ve olası aykırı değerlerini görselleştirmek amacıyla kullanılır.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Görselleştirilecek değişkeni içeren veri seti.
    variable : str
        Kutu grafiği oluşturulacak sütunun adı.

    Returns
    -------
    None
        Fonksiyon kutu grafiğini ekranda gösterir, herhangi bir değer döndürmez.

    Examples
    --------
    box_chart(df, "Age")
    """
    sns.boxplot(x=dataframe[variable])
    plt.title(f"{variable} Box Plot")
    plt.xlabel(variable)
    plt.show()


def outlier_thresholds(dataframe,variable):
    """
    Belirtilen sayısal değişken için IQR yöntemine göre
    alt ve üst aykırı değer sınırlarını hesaplar.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        İncelenecek değişkeni içeren veri seti.
    variable : str
        Aykırı değer sınırları hesaplanacak sayısal sütunun adı.

    Returns
    -------
    low_limit : float
        IQR yöntemine göre hesaplanan alt sınır.
    up_limit : float
        IQR yöntemine göre hesaplanan üst sınır.

    Examples
    --------
    low_limit, up_limit = outlier_thresholds(df, "Age")
    print(low_limit, up_limit)

    Notes
    -----
    Alt ve üst sınırlar aşağıdaki formüllerle hesaplanır:

    IQR = Q3 - Q1
    Alt sınır = Q1 - 1.5 * IQR
    Üst sınır = Q3 + 1.5 * IQR
    """
    quartile_1=dataframe[variable].quantile(0.25)
    quartile_3=dataframe[variable].quantile(0.75)
    iqr=quartile_3-quartile_1
    up_limits=quartile_3 + 1.5 * iqr
    low_limits=quartile_1 - 1.5 * iqr
    return up_limits,low_limits

def  check_outlier(dataframe,variable):
    """
    Belirtilen sayısal değişkende IQR yöntemine göre
    aykırı değer bulunup bulunmadığını kontrol eder.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        İncelenecek değişkeni içeren veri seti.
    variable : str
        Aykırı değer kontrolü yapılacak sayısal sütunun adı.

    Returns
    -------
    bool
        Değişkende en az bir aykırı değer varsa True,
        aykırı değer yoksa False döndürür.

    Examples
    --------
    check_outlier(df, "Age")
    True
    """
    up_limits,low_limits=outlier_thresholds(dataframe,variable)
    outlier_mask=((dataframe[variable]<low_limits) | (dataframe[variable]>up_limits))
    return outlier_mask.any()

    
def remove_outlier(dataframe,variable):
    """
    Belirtilen değişkendeki aykırı değerleri IQR yöntemine göre
    belirler ve veri setini aykırı değerli ve aykırı değersiz
    gözlemler olarak ikiye ayırır.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        İncelenecek değişkeni içeren veri seti.
    variable : str
        Aykırı değerleri kaldırılacak sayısal sütunun adı.

    Returns
    -------
    outlier_dataframe : pandas.DataFrame
        Alt veya üst sınırın dışında kalan aykırı gözlemler.
    without_outlier_dataframe : pandas.DataFrame
        Aykırı değer içermeyen gözlemler.

    Examples
    --------
    outliers, clean_df = remove_outlier(df, "Age")
    print(outliers.head())
    print(clean_df.head())
    """
    up_limits,low_limits=outlier_thresholds(dataframe,variable)
    outlier_mask=((dataframe[variable]<low_limits) | (dataframe[variable]>up_limits))
    outlier_dataframe=dataframe.loc[outlier_mask].copy()
    clean_dataframe=dataframe.loc[~outlier_mask].copy()
    return outlier_dataframe,clean_dataframe

def replace_thresholds(dataframe,variable):
    """
    Belirtilen değişkendeki aykırı değerleri IQR yöntemine göre
    hesaplanan alt ve üst sınırlarla değiştirir.

    Üst sınırdan büyük değerler üst sınırla, alt sınırdan küçük
    değerler ise alt sınırla değiştirilir.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Aykırı değerleri baskılanacak değişkeni içeren veri seti.
    variable : str
        Aykırı değerleri sınırlarla değiştirilecek sayısal sütunun adı.

    Returns
    -------
    pandas.DataFrame
        Aykırı değerleri alt ve üst sınırlarla değiştirilmiş veri seti.

    Examples
    --------
    df = replace_thresholds(df, "Age")
    """
    dataframe = dataframe.copy()
    up_limits,low_limits=outlier_thresholds(dataframe,variable)
    dataframe.loc[dataframe[variable]>up_limits,variable]=up_limits
    # dataframe.loc[dataframe[variable]<low_limits,variable]=low_limits
    
    return dataframe


def grab_col_names(dataframe, cat_th=10, car_th=20):
    """
    Veri setindeki kategorik, sayısal ve kategorik fakat
    kardinal değişkenlerin isimlerini döndürür.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Değişken türleri incelenecek veri seti.
    cat_th : int, default=10
        Sayısal fakat kategorik değişkenler için eşik değer.
    car_th : int, default=20
        Kategorik fakat kardinal değişkenler için eşik değer.

    Returns
    -------
    cat_cols : list
        Kategorik değişkenler.
    num_cols : list
        Sayısal değişkenler.
    cat_but_car : list
        Kategorik görünümlü kardinal değişkenler.
    """

    # Kategorik sütunlar
    cat_cols = [
        col for col in dataframe.columns
        if dataframe[col].dtype == "O"
    ]

    # Sayısal görünümlü kategorik sütunlar
    num_but_cat = [
        col for col in dataframe.columns
        if dataframe[col].nunique() < cat_th
        and dataframe[col].dtype != "O"
    ]

    # Kategorik görünümlü kardinal sütunlar
    cat_but_car = [
        col for col in dataframe.columns
        if dataframe[col].nunique() > car_th
        and dataframe[col].dtype == "O"
    ]

    cat_cols = cat_cols + num_but_cat

    cat_cols = [
        col for col in cat_cols
        if col not in cat_but_car
    ]

    # Sayısal sütunlar
    num_cols = [
        col for col in dataframe.columns
        if dataframe[col].dtype != "O"
    ]

    num_cols = [
        col for col in num_cols
        if col not in num_but_cat
    ]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f"cat_cols: {len(cat_cols)}")
    print(f"num_cols: {len(num_cols)}")
    print(f"cat_but_car: {len(cat_but_car)}")
    print(f"num_but_cat: {len(num_but_cat)}")

    return cat_cols, num_cols, cat_but_car


def grab_outliers(dataframe, variable, index=False, head=10):
    """
    Belirtilen sütundaki aykırı gözlemleri getirir.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        İncelenecek veri seti.
    variable : str
        Aykırı değerleri incelenecek sütun adı.
    index : bool, default=False
        True olduğunda aykırı gözlemlerin indekslerini döndürür.
    head : int, default=10
        Aykırı gözlem sayısı fazla olduğunda gösterilecek satır sayısı.

    Returns
    -------
    pandas.DataFrame veya pandas.Index
        index=False ise aykırı gözlemleri,
        index=True ise aykırı gözlemlerin indekslerini döndürür.
    """

    up_limits, low_limits = outlier_thresholds(dataframe,variable)

    outlier_mask = (
        (dataframe[variable] <  low_limits)
        | (dataframe[variable] > up_limits)
    )

    outliers = dataframe.loc[outlier_mask]

    if index:
        return outliers.index

    return outliers

def lof_analysis(dataframe, n_neighbors=20, plot_limit=50, show_plot=True):
    """
    Local Outlier Factor yöntemiyle aykırı gözlemleri analiz eder.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Yalnızca sayısal ve eksik değer içermeyen veri seti.
    n_neighbors : int, default=20
        LOF hesaplamasında kullanılacak komşu sayısı.
    plot_limit : int, default=50
        Grafikte gösterilecek sıralanmış skor sayısı.
    show_plot : bool, default=True
        LOF skor grafiğinin gösterilip gösterilmeyeceği.

    Returns
    -------
    results : pandas.DataFrame
        Her gözlem için LOF skoru ve tahmin sonucu.
    model : LocalOutlierFactor
        Eğitilmiş LOF modeli.
    """

    if n_neighbors >= len(dataframe):
        raise ValueError(
            "n_neighbors, gözlem sayısından küçük olmalıdır."
        )

    model = LocalOutlierFactor(n_neighbors=n_neighbors)
    predictions = model.fit_predict(dataframe)
    lof_scores = model.negative_outlier_factor_

    results = pd.DataFrame(
        {
            "lof_score": lof_scores,
            "prediction": predictions,
            "is_outlier": predictions == -1
        },
        index=dataframe.index
    )

    if show_plot:
        sorted_scores = np.sort(lof_scores)

        pd.Series(sorted_scores).plot(
            style=".-",
            xlim=(0, min(plot_limit, len(sorted_scores))),
            title="Sıralanmış LOF Skorları"
        )

        plt.xlabel("Sıralanmış gözlem")
        plt.ylabel("Negatif LOF skoru")
        plt.show()

    return results, model



