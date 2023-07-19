# Generated by Django 3.2.15 on 2022-11-10 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0009_alter_sequenceoperation_sequence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='equipmentproperty',
        ),
        migrations.AlterField(
            model_name='project',
            name='controller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admin_interface.controllermodel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='interface',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admin_interface.projectinterface'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='platform',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admin_interface.projectplatform'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='standard',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admin_interface.projectstandard'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='sysmedium',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admin_interface.systemmedium'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='systype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admin_interface.systemtypes'),
            preserve_default=False,
        ),
    ]
