from sql_akchemy import banco

class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True) # atributo da classe
    url = banco.Column(banco.String(80)) # atributo da classe
    hoteis = banco.relationship('HotelModel') # Demonstra que a classe siteModel tem uma relação de tabela com a classe HotelModel, contendo uma lista de objetos hoteis.

    #Construtor
    def __init__(self, url) :
        self.url = url
    
    def json(self):
        return {
            'hotel_id': self.site_id,
            'nome': self.url,
            'hoteis' : [hotel.json() for hotel in self.hoteis ]
        }

    @classmethod
    def find_site(cls, url):
        #esse cls e a abreviação da classe seria a mesma coisa de escrever SiteModel
        site = cls.query.filter_by(url=url).first() # SELECT * FROM sites WHERE url = $url
        if site:
            return site
        return None

    # salva o site no banco de dados.
    def save_site(self):
            # Adiciona o proprio objeto ao banco
            # ele identifica os argumentos e faz tudo sozinho
        banco.session.add(self)
        banco.session.commit()

    # Deleta o Site do banco de dados
    def delete_site(self):
        banco.session.delete(self)
        banco.session.commit()
