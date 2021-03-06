from sql_akchemy import banco

class HotelModel(banco.Model):
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True) # atributo da classe
    nome = banco.Column(banco.String(80)) # atributo da classe
    estrelas = banco.Column(banco.Float(precision=1)) # atributo da classe
    diaria = banco.Column(banco.Float(precision=2)) # atributo da classe
    cidade = banco.Column(banco.String(40)) # atributo da classe
    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.site_id')) # atributo da classe chave estrangeira da tabela siteModel
    #site = banco.relationship('SiteModel')


     #Construtor
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id) :
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id
    
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id' : self.site_id
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        #esse cls e a abreviação da classe seria a mesma coisa de escrever HotelModel
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() # SELECT * FROM hoteis WHERE hotel_id = $hotel_id
        if hotel:
            return hotel
        return None

    # salva o hotel no banco de dados.
    def save_hotel(self):
            # Adiciona o proprio objeto ao banco
            # ele identifica os argumentos e faz tudo sozinho
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
