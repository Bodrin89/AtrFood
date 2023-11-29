from import_export.resources import ModelResource

from apps.individual_user.models import IndividualUserModel


class IndividualUserResource(ModelResource):

    class Meta:
        model = IndividualUserModel
        # fields = ('your_field_name', 'another_field_name', 'third_field_name')  # Перечислите нужные поля

    # # Дополнительные настройки и преобразования данных, если необходимо
    # second_phone_numberr = fields.Field(
    #     column_name='second_phone_numberr',  # Укажите старое название поля из файла
    #     attribute='second_phone_number',  # Укажите новое название поля в модели
    # )

    # Дополнительные преобразования для других полей, если нужно

    def before_import_row(self, row, **kwargs):
        """Логика перед импортом строки"""
        if row.get('second_phone_numberr'):
            row['second_phone_number'] = row.get('second_phone_numberr')
