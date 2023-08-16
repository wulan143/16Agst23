from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if User.objects.filter(email=extra_fields.get('email')).exists():
        # Email sudah digunakan, tampilkan pesan error atau ambil tindakan yang sesuai
            print("Email sudah digunakan.")
            return None
        # Normalisasi username
        username = self.normalize_email(username)
        # Buat instance User baru
        user = self.model(username=username, **extra_fields)
        # Set password
        user.set_password(password)
        # Simpan user ke database
        user.save(using=self._db)
        return user
    
    def create_kalab(self, username, password=None, **extra_fields):
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.peran = 'Kepala LAB'
        user.save(using=self._db)
        return user
    
    def create_dosen(self, username, password=None, **extra_fields):
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.peran = 'Dosen'
        user.save(using=self._db)
        return user
    
    def create_mahasiswa(self, username, password=None, **extra_fields):
        username = self.normalize_email(username)
        user = self.m2odel(username=username, **extra_fields)
        user.set_password(password)
        user.peran = 'Mahasiswa'
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.peran = 'Admin'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    MAHASISWA_ROLE = 'Mahasiswa'
    KALAB_ROLE = 'Kepala LAB'
    DOSEN_ROLE = 'Dosen'
    ADMIN_ROLE = 'Admin'
    ROLE_CHOICES = [
        (MAHASISWA_ROLE, 'Mahasiswa'),
        (KALAB_ROLE, 'Kepala LAB'),
        (DOSEN_ROLE, 'Dosen'),
        (ADMIN_ROLE, 'Admin'),
    ]
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    confirm_password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    peran = models.CharField(max_length=15, choices=ROLE_CHOICES, default=MAHASISWA_ROLE)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = "pengguna"

    def is_admin(self):
        return self.role == self.ADMIN_ROLE
    
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.role == self.ADMIN_ROLE

    def has_module_perms(self, app_label):
        return self.role == self.ADMIN_ROLE
    
class Mahasiswa(models.Model):
    id_mahasiswa = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    nim = models.CharField(max_length=30)
    nama = models.CharField(max_length=30)
    kelas = models.CharField(max_length=30)
    semester = models.IntegerField()
    class Meta:
        db_table = "mahasiswa"

    def __str__(self):
        return self.nama



class Lab(models.Model):
    id_lab = models.AutoField(primary_key=True)
    nama_lab = models.CharField(max_length=100)
    kepala_lab = models.CharField(max_length=100)
    jumlah_pc = models.IntegerField()
    class Meta:
        db_table = "lab"
    def __str__(self):
        return self.nama_lab
    
class PC(models.Model):
    id_pc = models.AutoField(primary_key=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    nomor_pc = models.CharField(max_length=50)
    class Meta:
        db_table = "pc"
    def __str__(self):
        return self.nama_lab
    
class MataKuliah(models.Model):
    id_mk = models.AutoField(primary_key=True)
    kode_mk = models.CharField(max_length=10)
    nama_mk = models.CharField(max_length=100)
    dosen_pengampu = models.CharField(max_length=100)
    jumlah_sks = models.IntegerField()
    class Meta:
        db_table = "matakuliah"

    def __str__(self):
        return self.nama_mk
    
class Pengcekan(models.Model):
    id_cek = models.AutoField(primary_key=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    pc = models.ForeignKey(PC, on_delete=models.CASCADE)
    matkul = models.ForeignKey(MataKuliah, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True,default=timezone.now)
    keterangan = models.CharField(max_length=50)
    deskripsi = models.CharField(max_length=200)

    class Meta:
        db_table = "pengecekan"

    def __str__(self):
        return self.nama_lab

    def get_items(self):
        return Item.objects.filter(pengcekan=self)

class Item(models.Model):
    pengcekan = models.ForeignKey(Pengcekan, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "item"

class Dosen(models.Model):
    id_dosen = models.AutoField(primary_key=True)
    nip = models.CharField(max_length=30)
    nama = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=30)
    class Meta:
        db_table = "dosen"

    def __str__(self):
        return self.nama_dosen

