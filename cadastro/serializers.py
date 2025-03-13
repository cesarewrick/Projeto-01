from rest_framework import serializers
from cadastro.models import Estudante, Curso, Matricula

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ['id', 'nome', 'email', 'cpf', 'data_nascimento', 'celular']
        
        def validate_cpf(self,cpf):
            if len(cpf) != 11:
                raise serializers.ValidationError('O CPF deve ter 11 dígitos.')
            
            if not cpf.isdigit():
                raise serializers.ValidationError('O CPF deve conter apenas números.')
            
            return cpf
        
        def validate_nome(self, nome):
            if not re.match(r'^[A-Za-zÀ-ú\s]+$', nome):
                raise serializers.ValidationError("O nome deve conter apenas letras e espaços.")
            
            if len(nome.strip()) < 3:
                raise serializers.ValidationError('O nome deve ter pelo menis 3 caracteres.')
            
            return nome
        
        def validate_email(self, email):
             if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                 raise serializers.ValidationError('O e-mail informado não é valido.')
             
             return email
        def validate_data_nascimento(self, data_nascimento):
            if data_nascimento > date.today():
                raise serializers.ValidatonError('A data de nascimeento não pode ser no futuro.')
            
            idade = (date.today() - data_nascimento).days // 365
            if idade < 18:
                raise serializers.ValidationError('0 estudante deve ter pelo menis 18 anos')
            
            return data_nascimento
        
        def validate_celular(self, celular):
            if len(celular) != 11:
                raise serializers.ValidationErros('O celular deve ter 11 digitos.')
            
            if not celular.isdigit():
                raise serializers.ValidationError('O celular deve conter apenas números.')
            
            return celular

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = "__all__"  # Corrigido para "__all__"

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        exclude = []  # Ou use fields = "__all__"

class ListaMatriculasEstudanteSerializer(serializers.ModelSerializer):
    curso = serializers.ReadOnlyField(source='curso.descricao')
    periodo = serializers.SerializerMethodField()

    class Meta:
        model = Matricula
        fields = ['curso', 'periodo']

    def get_periodo(self, obj):
        return obj.get_periodo_display()

class ListaMatriculasCursoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.ReadOnlyField(source='estudante.nome')

    class Meta:
        fields = ['estudante_nome']
        model = Matricula