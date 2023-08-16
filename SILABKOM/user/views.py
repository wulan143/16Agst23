from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout,authenticate, login as auth_login, get_user_model
from django.contrib import messages
import traceback
import json
from user.models import Mahasiswa, MataKuliah, Lab, PC, Pengcekan, Item
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import IntegrityError 
User = get_user_model()

@login_required(login_url=settings.LOGIN_URL)
def logout(request):
    auth_logout(request)
    return redirect('login')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.peran == User.ADMIN_ROLE:
                return redirect('/admin')
            elif user.peran == User.KALAB_ROLE:
                return redirect('beranda/kalab/')
            elif user.peran == User.DOSEN_ROLE:
                return redirect('beranda/dosen/')
            elif user.peran == User.MAHASISWA_ROLE:
                return redirect('beranda/mahasiswa/')
            else:
                messages.error(request, 'Anda tidak memiliki izin untuk mengakses halaman ini.')
        else:
            messages.error(request, 'Username/Password salah.')

    return render (request, 'registration/login.html')


def daftar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password1')

        # Memeriksa apakah email kosong
        if not email:
            messages.error(request, 'Email harus diisi.')
            return redirect('daftar')

        # Memeriksa apakah email sudah digunakan
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah digunakan.')
            return redirect('daftar')

        # Memeriksa apakah username sudah digunakan
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan.')
            return redirect('daftar')

        if password != confirm_password:
            messages.error(request, "Password tidak sesuai.")
            return redirect('daftar')

        hashed_password = make_password(password, confirm_password)

        user = User(username=username, email=email, password=hashed_password, peran=User.MAHASISWA_ROLE)
        try:
            user.save()
        except IntegrityError as e:
            messages.error(request, "Terjadi kesalahan saat menyimpan data pengguna.")
            traceback.print_exc()  # Cetak traceback kesalahan di konsol
            return redirect('daftar')

        # Authenticate user
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            # User authentication successful
            messages.success(request, "Akun Kamu Berhasil Dibuat, Silahkan Lakukan Pembayaran")
            return redirect('login')
        else:
            # User authentication failed
            messages.error(request, "Terjadi kesalahan saat membuat akun.")
            return redirect('daftar/')
    else:
        return render (request, 'registration/daftar.html')




# mahasiswa
@login_required(login_url=settings.LOGIN_URL)
def beranda_mahasiswa(request):
    user = request.user
    return render (request, 'beranda.html', {'user':user})


@login_required(login_url=settings.LOGIN_URL)
def home(request):
    return render (request, 'mahasiswa/home.html')

@login_required(login_url=settings.LOGIN_URL)
def pesan(request):
    return render (request, 'mahasiswa/pesan.html')
        

@login_required(login_url=settings.LOGIN_URL)
def mahasiswa(request):
    try:
        # Cek apakah pengguna saat ini sudah memiliki data mahasiswa
        mahasiswa = Mahasiswa.objects.get(user=request.user)
        button_text = "Edit"
        nim = mahasiswa.nim
        nama = mahasiswa.nama
        kelas = mahasiswa.kelas
        semester = mahasiswa.semester
    except Mahasiswa.DoesNotExist:
        mahasiswa = None
        button_text = "Submit"
        nim = ''
        nama = ''
        kelas = ''
        semester = ''

    if request.method == 'POST':
        nim = request.POST.get('nim')
        nama = request.POST.get('nama')
        kelas = request.POST.get('kelas')
        semester = request.POST.get('semester')

        if mahasiswa:
            # Update data mahasiswa yang sudah ada
            mahasiswa.nim = nim
            mahasiswa.nama = nama
            mahasiswa.kelas = kelas
            mahasiswa.semester = semester
            mahasiswa.save()
            success_message = "Data mahasiswa berhasil diperbarui."
        else:
            # Buat data mahasiswa baru
            mahasiswa = Mahasiswa.objects.create(user=request.user, nim=nim, nama=nama, kelas=kelas, semester=semester)
            success_message = "Data mahasiswa berhasil disimpan."
            button_text = "Edit"

    else:
        success_message = None

    # Refresh objek mahasiswa dari database jika ada
    if mahasiswa:
        mahasiswa.refresh_from_db()

    return render(request, 'mahasiswa/mahasiswa.html', {
        'success_message': success_message,
        'mahasiswa': mahasiswa,
        'button_text': button_text,
        'nim': nim,
        'nama': nama,
        'kelas': kelas,
        'semester': semester
    })



@login_required(login_url=settings.LOGIN_URL)
def pengecekan(request):
    error_message = ""
    success_message = ""
    labs = Lab.objects.all()
    pcs = PC.objects.all()
    matkuls = MataKuliah.objects.all()

    if request.method == 'POST':
        nama_mk = request.POST.get('nama_mk')
        nama_lab = request.POST.get('nama_lab')
        nomor_pc = request.POST.get('no_pc')
        keterangan = request.POST.get('keterangan')
        deskripsi = request.POST.get('deskripsi')
        items = request.POST.getlist('items')

        try:
            matkul = MataKuliah.objects.get(id_mk=nama_mk)
            lab = Lab.objects.get(id_lab=nama_lab)
            pc = PC.objects.get(id_pc=nomor_pc)

            cek = Pengcekan.objects.create(
                lab=lab,
                pc=pc,
                matkul=matkul,
                keterangan=keterangan,
                deskripsi=deskripsi
            )

            for item in items:
                Item.objects.create(name=item, pengcekan=cek)

            success_message = "Data pengcekan berhasil disimpan."
            return redirect('pesan')

        except Lab.DoesNotExist:
            error_message = "Lab dengan ID tersebut tidak ditemukan."
        except PC.DoesNotExist:
            error_message = "PC dengan ID tersebut tidak ditemukan."
        except MataKuliah.DoesNotExist:
            error_message = "Nama mata kuliah tidak ditemukan."

    items = [
        {"id": "Keyboard", "name": "Keyboard"},
        {"id": "Mouse", "name": "Mouse"},
        {"id": "CPU", "name": "CPU"},
        {"id": "Monitor", "name": "Monitor"}
    ]
    
    context = {
        'labs': labs,
        'pcs': pcs,
        'matkuls': matkuls,
        'error_message': error_message,
        'success_message': success_message,
        'items': items
    }

    return render(request, 'mahasiswa/cekform.html', context)


# mahasiswa

# dosen
@login_required(login_url=settings.LOGIN_URL)
def beranda_dosen(request):
    return render (request, 'dosen/berandadosen.html')

def lihatpengecekan(request):
    cek = Pengcekan.objects.all()
    pc = PC.objects.all()
    nama = Mahasiswa.objects.all()
    lab = Lab.objects.all()
    item = Item.objects.all()

    context = {
        'cek': cek,
        'pc': pc,
        'lab': lab,
        'item': item,
    }
    return render (request, 'dosen/lihatpengecekan.html', context)
# dosen

# kalab
@login_required(login_url=settings.LOGIN_URL)
def beranda_kalab(request):
    
    return render (request, 'kalab/berandakalab.html')

# kalab

def cek_form(request):
    if request.method == 'POST':
        form = AbsensiForm(request.POST)
        if form.is_valid():
            nama = form.cleaned_data['nama']
            tanggal = form.cleaned_data['tanggal']
            
            # Lakukan logika untuk memproses dan mencatat absensi
            # Misalnya, menyimpan data ke database, file, atau sistem lainnya

            # Contoh sederhana mencetak data absensi
            absensi = f"Nama: {nama}\nTanggal: {tanggal}\n"
            
            # Menyimpan data absensi ke file
            with open('absensi.txt', 'a') as file:
                file.write(absensi)

            return render(request, 'absensi/success.html')
    else:
        form = AbsensiForm()
    
    return render(request, 'absensi/cek_form.html', {'form': form})


# def absensi_view(request):
#     # Lakukan logika pemrosesan absensi di sini
#     # Misalnya, menyimpan data absensi ke database atau melakukan operasi lainnya

#     return render(request, 'absensi.html')
