from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
        widgets = {
            'data_validade': forms.DateInput(
                format='%d/%m/%Y',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'style': 'max-width: 300px;'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_validade'].input_formats = ['%d/%m/%Y', '%Y-%m-%d']

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        categoria = cleaned_data.get('categoria')

        # Se for uma edição, ignore o próprio objeto
        if self.instance.pk:
            existe = Produto.objects.filter(nome=nome, categoria=categoria).exclude(pk=self.instance.pk).exists()
        else:
            existe = Produto.objects.filter(nome=nome, categoria=categoria).exists()

        if existe:
            raise forms.ValidationError('Já existe um produto com esse nome e categoria.')
