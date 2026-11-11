from django.db import migrations


def link_pdfs(apps, schema_editor):
    Accreditation = apps.get_model('main', 'Accreditation')
    mapping = {
        'FDA': 'accreditations/certificates/fda.pdf',
        'EU organic': 'accreditations/certificates/eu_organic.pdf',
        'FSSAI': 'accreditations/certificates/fssai.pdf',
        'FSSC 22000': 'accreditations/certificates/fssc_22000.pdf',
        'GMP': 'accreditations/certificates/gmp.pdf',
        'India halal': 'accreditations/certificates/india_halal.pdf',
        'India Organic': 'accreditations/certificates/india_organic.pdf',
        'ISO 9001 2015': 'accreditations/certificates/iso_9001_2015.pdf',
        'ISO 9001': 'accreditations/certificates/iso_9001.pdf',
        'KLBD': 'accreditations/certificates/klbd.pdf',
        'Kosher': 'accreditations/certificates/kosher.pdf',
        'SGS GMP': 'accreditations/certificates/sgs_gmp.pdf',
        'spice board': 'accreditations/certificates/spice_board.pdf',
        'USDA organic': 'accreditations/certificates/usda_organic.pdf',
    }
    for name, path in mapping.items():
        Accreditation.objects.filter(name__iexact=name).update(certificate_file=path)


def reverse_link_pdfs(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_accreditation_category_and_more'),
    ]

    operations = [
        migrations.RunPython(link_pdfs, reverse_link_pdfs),
    ]
