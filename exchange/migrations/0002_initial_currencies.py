from django.db import migrations


def crear_monedas_iniciales(apps, schema_editor):
    Moneda = apps.get_model("exchange", "Moneda")

    monedas = [
        ("Dólar estadounidense", "USD"),
        ("Euro", "EUR"),
        ("Real brasileño", "BRL"),
        ("Peso chileno", "CLP"),
    ]

    for nombre, codigo in monedas:
        Moneda.objects.get_or_create(
            codigo_iso=codigo,
            defaults={"nombre": nombre},
        )


def borrar_monedas_iniciales(apps, schema_editor):
    Moneda = apps.get_model("exchange", "Moneda")
    Moneda.objects.filter(codigo_iso__in=["USD", "EUR", "BRL", "CLP"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            crear_monedas_iniciales,
            reverse_code=borrar_monedas_iniciales,
        ),
    ]
