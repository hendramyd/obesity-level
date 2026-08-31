# Mengimpor library
import pandas as pd
import streamlit as st
import pickle
import warnings
warnings.filterwarnings("ignore")

from PIL import Image

# Konfigurasi halaman
st.set_page_config(
    page_title="Obesity Level Prediction",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling profesional
st.markdown("""
    <style>
    /* Header styling */
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    
    /* Result styling dengan warna berbeda untuk setiap kategori */
    .result-card {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .result-insufficient { background-color: #d4edda; color: #155724; border-left: 5px solid #28a745; }
    .result-normal { background-color: #cfe2ff; color: #084298; border-left: 5px solid #0d6efd; }
    .result-obesity-i { background-color: #fff3cd; color: #856404; border-left: 5px solid #ffc107; }
    .result-obesity-ii { background-color: #f8d7da; color: #721c24; border-left: 5px solid #f5c6cb; }
    .result-obesity-iii { background-color: #f5c2c7; color: #842029; border-left: 5px solid #f1b0b7; }
    .result-overweight-i { background-color: #fff3cd; color: #856404; border-left: 5px solid #fd7e14; }
    .result-overweight-ii { background-color: #f8d7da; color: #721c24; border-left: 5px solid #dc3545; }
    
    /* Section styling */
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f77b4;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .divider {
        margin: 2rem 0;
        border-top: 2px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Header dengan gambar
image = Image.open(r'C:\Users\Hendra\Documents\Deployment Obesity\obesitas_level.gif')
st.image(image, use_container_width=True)

st.markdown("<div class='main-header'>⚕️ Prediksi Level Obesitas</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Aplikasi Prediksi Tingkat Obesitas Berbasis Machine Learning</div>", unsafe_allow_html=True)

# Load model
my_model = pickle.load(open('model_klasifikasi_terbaik.pkl', 'rb'))

# Pilihan mode input
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📋 Pilih Mode Input Data</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📁 Upload File CSV", "✍️ Input Manual"])

# ========== TAB 1: Upload File CSV ==========
with tab1:
    st.markdown("<div class='section-title'>Unggah File CSV Anda</div>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader('Pilih file CSV untuk prediksi', type='csv')
    
    if uploaded_file is not None:
        try:
            dataku = pd.read_csv(uploaded_file)
            
            # Menampilkan preview data
            st.success('✅ File berhasil diupload!')
            st.subheader('Preview Data:')
            st.dataframe(dataku, use_container_width=True)
            
            # Prediksi
            with st.spinner('🔄 Sedang memproses prediksi...'):
                hasil = my_model.predict(dataku)
            
            # Menampilkan hasil dengan styling
            st.subheader('📊 Hasil Prediksi:')
            
            # Mapping hasil prediksi
            obesity_labels = {
                0: ('Insufficient Weight', 'result-insufficient'),
                1: ('Normal Weight', 'result-normal'),
                2: ('Obesity Type I', 'result-obesity-i'),
                3: ('Obesity Type II', 'result-obesity-ii'),
                4: ('Obesity Type III', 'result-obesity-iii'),
                5: ('Overweight Level I', 'result-overweight-i'),
                6: ('Overweight Level II', 'result-overweight-ii')
            }
            
            # Tampilkan hasil per baris
            for i in range(len(hasil)):
                label, style_class = obesity_labels.get(hasil[i], ('Unknown', ''))
                st.markdown(f"<div class='result-card {style_class}'>Indeks {i}: {label}</div>", 
                           unsafe_allow_html=True)
            
            # Statistik hasil
            st.subheader('📈 Statistik Prediksi:')
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Prediksi", len(hasil))
            with col2:
                st.metric("Hasil Unik", len(set(hasil)))
            with col3:
                st.metric("Kategori Terbanyak", obesity_labels[max(set(hasil))][0])
                
        except Exception as e:
            st.error(f'❌ Error: Terjadi kesalahan saat membaca file. {str(e)}')
    else:
        st.info('📌 Silakan pilih file CSV dengan kolom-kolom sesuai model prediksi')

# ========== TAB 2: Input Manual ==========
with tab2:
    st.markdown("<div class='section-title'>Masukkan Data Anda Secara Manual</div>", unsafe_allow_html=True)
    
    # Baris Pertama - Informasi Dasar
    st.markdown("**📏 Informasi Dasar**")
    col1, col2, col3 = st.columns(3)
    with col1:
        Age = st.number_input('Usia (tahun)', min_value=1, max_value=120, value=21)
    with col2:
        Height = st.number_input('Tinggi Badan (meter)', min_value=0.5, max_value=3.0, value=1.62, step=0.01)
    with col3:
        Weight = st.number_input('Berat Badan (kg)', min_value=10.0, max_value=300.0, value=64.0, step=0.1)

    # Baris Kedua - Data Demografis
    st.markdown("**👤 Data Demografis**")
    col1, col2, col3 = st.columns(3)
    with col1:
        Gender = st.selectbox('Jenis Kelamin', ['Male', 'Female'])
    with col2:
        family_history_with_overweight = st.selectbox('Ada riwayat keluarga overweight?', ['no', 'yes'])
    with col3:
        FAVC = st.selectbox('Sering makan makanan berkalori tinggi?', ['no', 'yes'])

    # Baris Ketiga - Kebiasaan Makan
    st.markdown("**🍽️ Kebiasaan Makan**")
    col1, col2, col3 = st.columns(3)
    with col1:
        FCVC = st.selectbox('Frekuensi makan sayuran',
                          ['1 - Tidak pernah', '2 - Kadang-kadang', '3 - Selalu'],
                          format_func=lambda x: x.split(' - ')[1])
        FCVC = FCVC[0]  # Ambil angka pertama
    with col2:
        NCP = st.selectbox('Berapa kali makan per hari?', ['1', '2', '3', '4'])
    with col3:
        CAEC = st.selectbox('Makan makanan di antara waktu makan?',
                           ['no', 'Sometimes', 'Frequently', 'Always'],
                           format_func=lambda x: {'no': '❌ Tidak', 'Sometimes': '🔄 Kadang', 'Frequently': '⚠️ Sering', 'Always': '🔴 Selalu'}.get(x, x))

    # Baris Keempat - Gaya Hidup
    st.markdown("**🏃 Gaya Hidup**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        SMOKE = st.selectbox('Apakah Anda merokok?', ['no', 'yes'])
    with col2:
        SCC = st.selectbox('Pantau kalori harian?', ['no', 'yes'])
    with col3:
        MTRANS = st.selectbox('Transportasi utama',
                             ['Automobile', 'Motorbike', 'Bike', 'Public_Transportation', 'Walking'])
    with col4:
        CALC = st.selectbox('Frekuensi minum alkohol',
                           ['No', 'Sometimes', 'Frequently', 'Always'])

    # Baris Kelima - Air dan Aktivitas
    st.markdown("**💧 Konsumsi Air & Aktivitas Fisik**")
    col1, col2, col3 = st.columns(3)
    with col1:
        CH2O = st.selectbox('Air minum per hari (liter)', ['1', '2', '3'])
    with col2:
        FAF = st.selectbox('Frekuensi aktivitas fisik',
                          ['0 - Tidak pernah', '1 - 1-2 hari', '2 - 3-4 hari', '3 - >4 hari'],
                          format_func=lambda x: x.split(' - ')[1])
        FAF = FAF[0]  # Ambil angka pertama
    with col3:
        TUE = st.selectbox('Penggunaan perangkat teknologi',
                          ['0 - 0-2 jam', '1 - 3-5 jam', '2 - Lebih dari 5 jam'],
                          format_func=lambda x: x.split(' - ')[1])
        TUE = TUE[0]  # Ambil angka pertama    

    # Tombol Prediksi
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        predict_button = st.button('🔍 Lakukan Prediksi', use_container_width=True)
    
    if predict_button:
        # Membuat dataframe dari input
        data = {
            'Gender': Gender,
            'Age': Age,
            'Height': Height,
            'Weight': Weight,
            'family_history_with_overweight': family_history_with_overweight,
            'FAVC': FAVC,
            'FCVC': FCVC,
            'NCP': NCP,
            'CAEC': CAEC,
            'SMOKE': SMOKE,
            'CH2O': CH2O,
            'SCC': SCC,
            'FAF': FAF,
            'TUE': TUE,
            'CALC': CALC,
            'MTRANS': MTRANS,
        }
        
        df = pd.DataFrame([data.values()], columns=data.keys())
        
        # Melakukan prediksi
        with st.spinner('🔄 Sedang memproses prediksi Anda...'):
            hasil = my_model.predict(df)
        
        # Mapping hasil prediksi dengan warna dan emoji
        obesity_mapping = {
            0: {
                'label': 'Insufficient Weight',
                'emoji': '📉',
                'class': 'result-insufficient',
                'description': 'Berat badan Anda berada di bawah batas normal. Konsultasikan dengan ahli gizi untuk program penambah berat badan yang sehat.'
            },
            1: {
                'label': 'Normal Weight',
                'emoji': '✅',
                'class': 'result-normal',
                'description': 'Selamat! Berat badan Anda dalam kategori normal dan sehat. Pertahankan gaya hidup yang sehat.'
            },
            2: {
                'label': 'Obesity Type I',
                'emoji': '⚠️',
                'class': 'result-obesity-i',
                'description': 'Anda memiliki kelebihan berat badan. Tingkatkan aktivitas fisik dan ubah pola makan untuk kesehatan yang lebih baik.'
            },
            3: {
                'label': 'Obesity Type II',
                'emoji': '🔴',
                'class': 'result-obesity-ii',
                'description': 'Berat badan Anda menunjukkan tingkat obesitas yang signifikan. Segera konsultasikan dengan dokter untuk program penurunan berat badan.'
            },
            4: {
                'label': 'Obesity Type III',
                'emoji': '🛑',
                'class': 'result-obesity-iii',
                'description': 'Kondisi obesitas Anda memerlukan perhatian medis segera. Hubungi profesional kesehatan untuk mendapatkan bantuan dan program penurunan berat badan yang terstruktur.'
            },
            5: {
                'label': 'Overweight Level I',
                'emoji': '⚠️',
                'class': 'result-overweight-i',
                'description': 'Anda memiliki kelebihan berat badan. Tingkatkan aktivitas fisik dan ubah pola makan untuk hasil yang optimal.'
            },
            6: {
                'label': 'Overweight Level II',
                'emoji': '🔴',
                'class': 'result-overweight-ii',
                'description': 'Kelebihan berat badan Anda memerlukan tindakan segera. Konsultasikan dengan ahli gizi dan dokter untuk program penurunan berat badan yang efektif.'
            }
        }
        
        # Menampilkan hasil
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📋 Hasil Prediksi</div>", unsafe_allow_html=True)
        
        prediction = hasil[0]
        result_info = obesity_mapping.get(prediction, obesity_mapping[1])
        
        # Kartu hasil utama
        st.markdown(f"""
            <div class='result-card {result_info['class']}'>
                {result_info['emoji']} <br>
                <span style='font-size: 2rem; font-weight: bold;'>{result_info['label']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Deskripsi dan rekomendasi
        st.info(f"💡 {result_info['description']}")
        
        # Informasi ringkas
        st.subheader('📊 Ringkasan Data Anda:')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Usia", f"{Age} tahun")
        with col2:
            st.metric("Tinggi Badan", f"{Height:.2f} m")
        with col3:
            st.metric("Berat Badan", f"{Weight:.1f} kg")
        
        # BMI Calculation
        bmi = Weight / (Height ** 2)
        st.metric("BMI (Body Mass Index)", f"{bmi:.2f}")
        
        # Saran kesehatan
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.subheader('💪 Saran Kesehatan:')
        
        recommendations = {
            0: [
                "✓ Tingkatkan asupan kalori dengan makanan bergizi",
                "✓ Konsumsi protein yang cukup untuk membangun otot",
                "✓ Lakukan latihan kekuatan secara teratur",
                "✓ Konsultasikan dengan ahli gizi profesional"
            ],
            1: [
                "✓ Lanjutkan pola makan yang sehat dan seimbang",
                "✓ Pertahankan aktivitas fisik minimal 150 menit per minggu",
                "✓ Hindari makanan bergula dan berlemak tinggi",
                "✓ Minum air putih yang cukup setiap hari"
            ],
            2: [
                "✓ Kurangi porsi makan dan kalori harian",
                "✓ Tingkatkan aktivitas fisik menjadi 300 menit per minggu",
                "✓ Pilih makanan rendah kalori namun bergizi",
                "✓ Konsultasikan dengan dokter atau ahli gizi"
            ],
            3: [
                "✓ Segera mulai program diet yang terstruktur",
                "✓ Konsultasikan dengan dokter untuk penilaian kesehatan",
                "✓ Tingkatkan aktivitas fisik secara bertahap",
                "✓ Pertimbangkan bantuan psikologis jika diperlukan"
            ],
            4: [
                "✓ Hubungi profesional kesehatan segera",
                "✓ Ikuti program penurunan berat badan yang dipandu medis",
                "✓ Mulai perubahan gaya hidup yang signifikan",
                "✓ Pantau kesehatan secara berkala"
            ],
            5: [
                "✓ Mulai program penurunan berat badan",
                "✓ Tingkatkan aktivitas fisik secara konsisten",
                "✓ Kurangi asupan makanan berkalori tinggi",
                "✓ Dapatkan dukungan dari ahli kesehatan"
            ],
            6: [
                "✓ Ambil tindakan penurunan berat badan yang serius",
                "✓ Konsultasikan dengan dokter dan ahli gizi",
                "✓ Ikuti program latihan yang terstruktur",
                "✓ Ubah kebiasaan makan secara fundamental"
            ]
        }
        
        for rec in recommendations.get(prediction, recommendations[1]):
            st.write(rec)