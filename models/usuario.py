from sql_akchemy import banco


class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    

    def __init__(self, login, senha) :
        self.login = login
        self.senha = senha
    
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
            #'senha': self.senha
        }

    @classmethod
    def find_user(cls, user_id):
        #esse cls e a abreviação da classe seria a mesma coisa de escrever UserModel
        user = cls.query.filter_by(user_id=user_id).first() # SELECT * FROM usuarios WHERE user_id = $user_id
        if user:
            return user
        return None

    # salva o hotel no banco de dados.
    def save_user(self):
            # Adiciona o proprio objeto ao banco
            # ele identifica os argumentos e faz tudo sozinho
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()