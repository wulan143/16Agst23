from django.shortcuts import render, redirect, get_object_or_404
from user.models import User, Mahasiswa, MataKuliah, Lab, PC, Pengcekan, Item, Dosen
import traceback
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import IntegrityError 

@login_required(login_url=settings.LOGIN_URL)
def menu_admin(request):
    return render(request,'menu_admin.html')

@login_required(login_url=settings.LOGIN_URL)
def  kelola_lab(request):
    return render(request, 'kelola_lab.html')

@login_required(login_url=settings.LOGIN_URL)
def  kelola_laporan(request):
    return render(request, 'kelola_laporan.html')


# mahasiswa
@login_required(login_url=settings.LOGIN_URL)
def kelola_mahasiswa(request):
    mahasiswa = Mahasiswa.objects.all()

    context = {
        'mahasiswa': mahasiswa,
    }

    return render(request, 'kelola_mahasiswa.html', context)

@login_required(login_url=settings.LOGIN_URL)
def tambah_mahasiswa(request):
    if request.method == 'POST':
        nim=request.POST['nim']
        nama=request.POST['name']
        kelas=request.POST['kelas']
        semester =request.POST['semester']
        mahasiswa = Mahasiswa.objects.create(nim=nim, nama=nama, kelas=kelas, semester=semester,)
        mahasiswa.save()
        return redirect('kelola_mahasiswa')
    else:
        return render(request, 'tambah_mahasiswa.html')
    
@login_required(login_url=settings.LOGIN_URL)
def edit_mahasiswa(request, id):
    mahasiswa = Mahasiswa.objects.get(id_mahasiswa=id)
    return render(request, 'edit_mahasiswa.html', {'mahasiswa':mahasiswa})

@login_required(login_url=settings.LOGIN_URL)
def update_mahasiswa(request, id):
    mahasiswa = get_object_or_404(Mahasiswa, id_mahasiswa=id)
    if request.method=='POST':
        mahasiswa.nim=request.POST['nim']
        mahasiswa.nama=request.POST['nama']
        mahasiswa.kelas=request.POST['kelas']
        mahasiswa.semester=request.POST['semester']
        mahasiswa.save()
        return redirect('kelola_mahasiswa' )

@login_required(login_url=settings.LOGIN_URL)
def hapus_mahasiswa(request, id):
    if request.method == 'POST':
        mahasiswa = Mahasiswa.objects.get(id_mahasiswa=id)
        mahasiswa.delete()
    return redirect('kelola_mahasiswa')

# user
@login_required(login_url=settings.LOGIN_URL)
def kelola_pengguna(request):
    pengguna = User.objects.all()

    context = {
        'pengguna': pengguna,
    }

    return render(request, 'kelola_pengguna.html', context)


@login_required(login_url=settings.LOGIN_URL)
def tambah_pengguna(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        peran =request.POST['peran']
        hashed_password = make_password(password)
        user = User(username=username, email=email, password=hashed_password, peran=peran)
        user.save()
        return redirect('kelola_pengguna')
    else:
        return render(request, 'tambah_pengguna.html')

@login_required(login_url=settings.LOGIN_URL)
def edit_pengguna(request, id):
    user = User.objects.get(id=id)
    return render(request, 'edit_pengguna.html', {'user':user})

@login_required(login_url=settings.LOGIN_URL)
def update_pengguna(request, id):
    user = get_object_or_404(User, id=id)
    if request.method=='POST':
        user.username=request.POST['username']
        user.email=request.POST['email']
        password=request.POST['password']
        hashed_password = make_password(password)
        user.password = hashed_password
        user.save()
        return redirect('kelola_pengguna' )

@login_required(login_url=settings.LOGIN_URL)
def hapus_pengguna(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        user.delete()
    return redirect('kelola_pengguna')

# lab

@login_required(login_url=settings.LOGIN_URL)
def kelola_lab(request):
    labs = Lab.objects.all()

    context = {
        'labs': labs,
    }

    return render(request, 'kelola_lab.html', context)

@login_required(login_url=settings.LOGIN_URL)
def tambah_lab(request):
    if request.method == 'POST':
        nama_lab=request.POST['nalab']
        kepala_lab=request.POST['kalab']
        jumlah_pc=request.POST['jupc']
        lab = Lab(nama_lab=nama_lab, kepala_lab=kepala_lab, jumlah_pc=jumlah_pc)
        lab.save()
        return redirect('kelola_lab')
    else:
        return render(request, 'tambah_lab.html')

@login_required(login_url=settings.LOGIN_URL)
def edit_lab(request, id_lab):
    lab = Lab.objects.get(id_lab=id_lab)
    return render(request, 'edit_lab.html', {'lab':lab})

@login_required(login_url=settings.LOGIN_URL)
def update_lab(request, id_lab):
    lab = get_object_or_404(Lab, id_lab=id_lab)
    if request.method=='POST':
        lab.nama_lab=request.POST['nalab']
        lab.kepala_lab=request.POST['kalab']
        lab.jumlah_pc=request.POST['jupc']
        lab.save()
        return redirect('kelola_lab' )

@login_required(login_url=settings.LOGIN_URL)
def hapus_lab(request, id_lab):
    if request.method == 'POST':
        lab = Lab.objects.get(id_lab=id_lab)
        lab.delete()
    return redirect('kelola_lab')

# pengecekan

@login_required(login_url=settings.LOGIN_URL)
def kelola_pengecekan(request):
    cek = Pengcekan.objects.all()
    pc = PC.objects.all()
    lab = Lab.objects.all()
    item = Item.objects.all()

    context = {
        'cek': cek,
        'pc': pc,
        'lab': lab,
        'item': item,
    }

    return render(request, 'kelola_pengecekan.html', context)

@login_required(login_url=settings.LOGIN_URL)
def hapus_pengecekan(request, id_cek):
    if request.method == 'POST':
        pengecekan = Pengcekan.objects.get(id_cek=id_cek)
        pengecekan.delete()
    return redirect('kelola_pengecekan')

@login_required(login_url=settings.LOGIN_URL)
def tambah_lab(request):
    kalab = Dosen.objects.all()
    if request.method == 'POST':
        nama_lab=request.POST['nalab']
        kepala_lab=request.POST['kalab']
        jumlah_pc=request.POST['jupc']
        lab = Lab(nama_lab=nama_lab, kepala_lab=kepala_lab, jumlah_pc=jumlah_pc)
        lab.save()
        return redirect('kelola_lab')
    else:
        return render(request, 'tambah_lab.html', {'kalab':kalab})

@login_required(login_url=settings.LOGIN_URL)
def edit_lab(request, id_lab):
    lab = Lab.objects.get(id_lab=id_lab)
    return render(request, 'edit_lab.html', {'lab':lab})

@login_required(login_url=settings.LOGIN_URL)
def update_lab(request, id_lab):
    lab = get_object_or_404(Lab, id_lab=id_lab)
    if request.method=='POST':
        lab.nama_lab=request.POST['nalab']
        lab.kepala_lab=request.POST['kalab']
        lab.jumlah_pc=request.POST['jupc']
        lab.save()
        return redirect('kelola_lab' )

@login_required(login_url=settings.LOGIN_URL)
def hapus_lab(request, id_lab):
    if request.method == 'POST':
        lab = Lab.objects.get(id_lab=id_lab)
        lab.delete()
    return redirect('kelola_lab')

# end


# matkul
@login_required(login_url=settings.LOGIN_URL)
def kelola_mata_kuliah(request):
    matkul = MataKuliah.objects.all()

    context = {
        'matkul': matkul,
    }

    return render(request, 'kelola_mata_kuliah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def tambah_mata_kuliah(request):
    if request.method == 'POST':
        kode_mk=request.POST['kodemk']
        nama_mk=request.POST['namamk']
        dosen_pengampu=request.POST['dp']
        jumlah_sks=request.POST['sks']
        matkul = MataKuliah(kode_mk=kode_mk, nama_mk=nama_mk, dosen_pengampu=dosen_pengampu, jumlah_sks=jumlah_sks)
        matkul.save()
        return redirect('kelola_mata_kuliah')
    else:
        return render(request, 'tambah_mata_kuliah.html')

@login_required(login_url=settings.LOGIN_URL)
def edit_mata_kuliah(request, id_mk):
    matkul = MataKuliah.objects.get(id_mk=id_mk)
    return render(request, 'edit_mata_kuliah.html', {'matkul':matkul})

@login_required(login_url=settings.LOGIN_URL)
def update_matkul(request, id_mk):
    matkul = get_object_or_404(MataKuliah, id_mk=id_mk)
    if request.method=='POST':
        matkul.kode_mk=request.POST['kodemk']
        matkul.nama_mk=request.POST['namamk']
        matkul.dosen_pengampu=request.POST['dp']
        matkul.jumlah_sks=request.POST['sks']
        matkul.save()
        return redirect('kelola_mata_kuliah' )

@login_required(login_url=settings.LOGIN_URL)
def hapus_mata_kuliah(request, id_mk):
    if request.method == 'POST':
        matkul = MataKuliah.objects.get(id_mk=id_mk)
        matkul.delete()
    return redirect('kelola_mata_kuliah')
# end

# pc
@login_required(login_url=settings.LOGIN_URL)
def kelola_pc(request):
    pc = PC.objects.all()
    lab = Lab.objects.all()

    context = {
        'pc': pc,
        'lab': lab,
    }

    return render(request, 'kelola_pc.html', context)

def tambah_pc(request):
    labs = Lab.objects.all()

    if request.method == 'POST':
        nama_lab=request.POST.get('nama_lab')
        nomor_pc=request.POST.get('no_pc')

        try:
            lab = Lab.objects.get(id_lab=nama_lab)

            cek = PC.objects.create(
                lab=lab,
                nomor_pc=nomor_pc
            )
            return redirect('kelola_pc')
        except Lab.DoesNotExist:
            error_message = "Lab dengan ID tersebut tidak ditemukan."
    return render(request, 'tambah_pc.html', {'labs':labs})

@login_required(login_url=settings.LOGIN_URL)
def edit_pc(request, id_pc):
    pc = PC.objects.get(id_pc=id_pc)
    return render(request, 'edit_pc.html', {'pc':pc})

@login_required(login_url=settings.LOGIN_URL)
def update_pc(request, id_pc):
    pc = get_object_or_404(PC, id_pc=id_pc)
    if request.method=='POST':
        pc.nomor_pc=request.POST['no_pc']
        pc.save()
        return redirect('kelola_pc' )

@login_required(login_url=settings.LOGIN_URL)
def hapus_pc(request, id_pc):
    if request.method == 'POST':
        pc = PC.objects.get(id_pc=id_pc)
        pc.delete()
    return redirect('kelola_pc')
#end

@login_required(login_url=settings.LOGIN_URL)
def kelola_dosen(request):
    dosen_list = Dosen.objects.all()
    context = {
        'dosen_list': dosen_list,
    }
    return render(request, 'kelola_dosen.html', context)


def tambah_dosen(request):
    if request.method == 'POST':
        nip = request.POST['nip']
        nama = request.POST['nama']
        jabatan = request.POST['jabatan']
        dosen = Dosen(nip=nip, nama=nama, jabatan=jabatan)  # Inisialisasi variabel dosen
        dosen.save()  # Simpan objek dosen ke database
        return redirect('kelola_dosen')
    else:
        return render(request, 'tambah_dosen.html')


def edit_dosen(request, dosen_id):
    dosen = Dosen.objects.get(id=dosen_id)
    if request.method == 'POST':
        dosen.nip = request.POST['nip']
        dosen.nama = request.POST['nama']
        dosen.jabatan = request.POST['jabatan']
        dosen.save()
        return redirect('kelola_dosen')
    else:
        context = {
            'dosen': dosen
        }
        return render(request, 'edit_dosen.html', context)

def hapus_dosen(request, dosen_id):
    dosen = Dosen.objects.get(id=dosen_id)
    dosen.delete()
    return redirect('kelola_dosen')
