from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('doctors', '0004_doctorprofile_certificate_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorProfileAuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_type', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('changes', models.TextField()),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.user')),
                ('doctor_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to='doctors.doctorprofile')),
            ],
        ),
    ]
