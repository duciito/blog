from django.db.models.fields.files import FieldFile


def file_cleanup(sender, instance, *args, **kwargs):
    """Delete model files. Intended for use with pre-delete signals on models."""

    for field_name in instance.__dict__:
        field = getattr(instance, field_name)
        if issubclass(field.__class__, FieldFile) and field.name:
            field.delete(save=False)
