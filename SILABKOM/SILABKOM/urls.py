from django.contrib import admin
from django.urls import path
from app_silabkom.views import *
from user.views import *
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', menu_admin, name='menu_admin'),
    path('',login, name='login'),
    path('login/',login, name='login'),
    path('daftar/',daftar, name='daftar'),
    path('logout/',logout,name='logout'),

    # mahasiswa
    path('login/beranda/mahasiswa/',beranda_mahasiswa, name='beranda_mahasiswa'),
    path('pengecekan/',pengecekan, name='pengecekan'),
    path('home/',home, name='home'),
    path('pesan/',pesan, name='pesan'),
    path('mahasiswa/',mahasiswa, name='mahasiswa'),

    # dosen
    path('login/beranda/dosen/',beranda_dosen, name='beranda_dosen'),
    path('lihat_pengecekan/',lihatpengecekan, name='lihat_pengecekan'),

    # kalab
    path('login/beranda/kalab/',beranda_kalab, name='beranda_kalab'),
    path('lihat_pengecekan/',lihatpengecekan, name='lihat_pengecekan'),

    path('tambah_pengguna/kelola_pengguna/', kelola_pengguna, name='kelola_pengguna'),
    path('tambah_pengguna/', tambah_pengguna, name='tambah_pengguna'),
    path('edit/user/<int:id>/', edit_pengguna, name='edit_pengguna'),
    path('edit/user/<int:id>/update/', update_pengguna, name='update_pengguna'),
    path('hapus/user/<int:id>/', hapus_pengguna, name='hapus_pengguna'),


    path('kelola_mahasiswa/', kelola_mahasiswa, name='kelola_mahasiswa'),
    path('tambah_mahasiswa/', tambah_mahasiswa, name='tambah_mahasiswa'),
    path('edit/mahasiswa/<int:id>/', edit_mahasiswa, name='edit_mahasiswa'),
    path('edit/mahasiswa/<int:id>/update/', update_mahasiswa, name='update_mahasiswa'),
    path('hapus/mahasiswa/<int:id>/', hapus_mahasiswa, name='hapus_mahasiswa'),


    path('kelola_laporan/', kelola_laporan, name='kelola_laporan'),

    path('kelola_pengecekan/', kelola_pengecekan, name='kelola_pengecekan'),
    path('hapus/cek/<int:id_cek>/', hapus_pengecekan, name='hapus_pengecekan'),

    path('manajemen_lab/', kelola_lab, name='kelola_lab'),
    path('tambah_lab/', tambah_lab, name='tambah_lab'),
    path('edit/lab/<int:id_lab>/', edit_lab, name='edit_lab'),
    path('edit/lab/<int:id_lab>/update/', update_lab, name='update_lab'),
    path('hapus/lab/<int:id_lab>/', hapus_lab, name='hapus_lab'),



    path('kelola_pc/', kelola_pc, name='kelola_pc'),
    path('tambah_pc/', tambah_pc, name='tambah_pc'),
    path('edit/pc/<int:id_pc>/', edit_pc, name='edit_pc'),
    path('edit/pc/<int:id_pc>/update/', update_pc, name='update_pc'),
    path('hapus/pc/<int:id_pc>/', hapus_pc, name='hapus_pc'),

    path('kelola_mata_kuliah/', kelola_mata_kuliah, name='kelola_mata_kuliah'),
    path('tambah_matkul/', tambah_mata_kuliah, name='tambah_matkul'),
    path('edit/matkul/<int:id_mk>/', edit_mata_kuliah, name='edit_mata_kuliah'),
    path('edit/matkul/<int:id_mk>/update/', update_matkul, name='update_matkul'),
    path('hapus/matkul/<int:id_mk>/', hapus_mata_kuliah, name='hapus_mata_kuliah'),

    path('kelola_dosen/',kelola_dosen, name='kelola_dosen'),
    path('tambah_dosen/',tambah_dosen, name='tambah_dosen'),
    path('edit_dosen/<int:dosen_id>/',edit_dosen, name='edit_dosen'),
    path('hapus_dosen/<int:dosen_id>/',hapus_dosen, name='hapus_dosen'),
    # path('absensi/', absensi_view, name='absensi'),
]