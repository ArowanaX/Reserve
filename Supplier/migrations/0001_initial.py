# Generated by Django 4.0.4 on 2022-05-10 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='res_name')),
                ('address', models.TextField(verbose_name='address')),
                ('city', models.CharField(max_length=20)),
                ('img', models.ImageField(blank=True, null=True, upload_to='supplier/')),
                ('type', models.CharField(choices=[('lux', 'lux hotel'), ('h', 'hotel'), ('gh', 'guesthouse')], max_length=10)),
                ('tag', models.CharField(blank=True, choices=[('res', 'Restaurant'), ('lux', 'lux'), ('sh', 'Sports hall')], max_length=10, null=True)),
                ('service_hours_start', models.IntegerField()),
                ('service_hours_end', models.IntegerField()),
                ('max_reserve', models.IntegerField()),
                ('detail', models.TextField(blank=True, max_length=300, null=True)),
                ('phone', models.CharField(max_length=12, unique=True, verbose_name='phone')),
                ('profile', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='residenceTOprofile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'residiance',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('describtion', models.TextField(blank=True, null=True)),
                ('att_file', models.FileField(blank=True, null=True, upload_to='supplier/ticket')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='date and time')),
                ('status', models.BooleanField(default=True)),
                ('admin', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='TickToResidence', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TickComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, help_text='کامنت خود را وارد کنید', max_length=255, null=True, verbose_name='comment')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CommentToTicket', to='Supplier.ticket', verbose_name='TickToTikComment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='CommentToUser', to=settings.AUTH_USER_MODEL, verbose_name='UserToTikComment')),
            ],
            options={
                'verbose_name': 'TikComment',
                'verbose_name_plural': 'TikComments',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('state', models.CharField(choices=[('F', 'Full'), ('E', 'Empty')], max_length=10)),
                ('faciliti', models.CharField(choices=[('lux', 'lux'), ('re', 'Refrigerator'), ('so', 'Sofa')], max_length=10)),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serviceTOroom', to='Supplier.residence')),
            ],
            options={
                'db_table': 'service',
            },
        ),
        migrations.CreateModel(
            name='RestaurantMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('describtion', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menuTOservice', to='Supplier.service')),
            ],
        ),
        migrations.CreateModel(
            name='ResidenceOutdoorAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_outdoor', models.ImageField(blank=True, null=True, upload_to='outdoor/')),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outdootTOresident', to='Supplier.residence')),
            ],
        ),
        migrations.CreateModel(
            name='ResidenceIndoorAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_indoor', models.ImageField(blank=True, null=True, upload_to='indoor/')),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indootTOresident', to='Supplier.residence')),
            ],
        ),
    ]
