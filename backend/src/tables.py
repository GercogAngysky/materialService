from email.policy import default
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import INTEGER, VARCHAR, NUMERIC
from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine("sqlite:///:memory:", echo=False)
Base = declarative_base()
# Base.metadata.create_all(engine)     # <------ run create tables


class User(Base):
    __tablename__ = "user"

    id = Column(INTEGER, nullable=False, unique=True, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(255), nullable=False, unique=True)
    email = Column(VARCHAR(255), nullable=True, unique=True)
    role = Column(VARCHAR(127), nullable=False, unique=False)
    password_hash = Column(VARCHAR(255), nullable=False, unique=True)

    def __repr__(self):
        return "<{0.__class__.__name__}(username{0.name}, id={0.id!r})>".format(self)


class BaseModel(Base):
    __abstract__ = True

    id = Column(INTEGER, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)
    description = Column(VARCHAR(255), nullable=True)

    def __repr__(self):
        return "<{0.__class__.__name__}(name={0.name}, id={0.id!r})>".format(self)


class Brand(BaseModel):
    __tablename__ = "brand"


class Format(BaseModel):
    __tablename__ = "format"

    name = None
    description = None
    length = Column(INTEGER, nullable=False, unique=False)
    width = Column(INTEGER, nullable=False, unique=False)
    __table_args__ = (UniqueConstraint("length", "width", name="format"), )

    def __repr__(self):
        return "<{0.__class__.__name__}({0.length}mm x {0.width}mm, id={0.id!r})>".format(self)


class Plate(BaseModel):
    __tablename__ = "plate"

    name = None
    description = None
    thickness = Column(INTEGER, nullable=False, unique=False)
    density = Column(INTEGER, nullable=True, unique=False)
    typeplate_id = Column(INTEGER, ForeignKey("typeplate.id", ondelete="CASCADE"), nullable=False)
    typeplate = relationship("TypePlate", backref="plate", lazy = "subquery")

    __table_args__ = (UniqueConstraint("thickness", "typeplate_id", name="plate"), )

    def __repr__(self):
        return "<{0.__class__.__name__}({0.thickness}mm, id={0.id!r})>".format(self)


class TypePlate(BaseModel):
    __tablename__ = "typeplate"

    description = None


class Decor(BaseModel):
    __tablename__ = "decor"
    
    img = Column(VARCHAR(127), nullable = True)
    typedecor_id = Column(INTEGER, ForeignKey("typedecor.id", ondelete = "CASCADE"))
    typedecor = relationship("TypeDecor", backref = "decor", lazy = "subquery") # <------- функция sqlalchemy, не поле, во время
    # session.add и session.commit, добавит в поле <Decor>.typedecor_id внешний ключ соответсвующий <TypeDecor>.id
    # <Decor>.typedecor - будет возвращать один объект <TypeDecor>, (<TypeDecor>.name - название типа декора)


class TypeDecor(BaseModel):
    __tablename__ = "typedecor"
    # <TypeDecor>.decor - будет возвращать список из <Decor>, хотя поля decor нет в классе TypeDecor
    description = None


class Maker(BaseModel):
    __tablename__ = "maker"


class Material(BaseModel):
    __tablename__ = "material"

    name = None
    brand_id = Column(INTEGER, ForeignKey("brand.id", ondelete = "CASCADE"), nullable = True) #, onupdate="CASCADE", ondelete="SET NULL")
    format_id = Column(INTEGER, ForeignKey("format.id", ondelete = "CASCADE"), nullable = False)
    plate_id = Column(INTEGER, ForeignKey("plate.id", ondelete = "CASCADE"), nullable = False)
    decor_id = Column(INTEGER, ForeignKey("decor.id", ondelete = "CASCADE"), nullable = False)
    brand = relationship("Brand", backref = "material", lazy = "subquery", )
    format = relationship("Format", backref = "material", lazy = "subquery")
    plate = relationship("Plate", backref = "material", lazy = "subquery")
    decor = relationship("Decor", backref = "material", lazy = "subquery")
    # связь с price, для того чтобы, при удалении материала удалялась цена на материал, если только на нее больше не ссылается ни одна запись
    price = relationship("Price", back_populates = "material", cascade = "all, delete-orphan")

    __table_args__ = (UniqueConstraint("brand_id", "format_id", "plate_id", "decor_id", name = "material"), )

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Price(BaseModel):
    __tablename__ = "price"

    name = None
    description = Column(VARCHAR(127), nullable = True)
    measure = Column(VARCHAR(127), nullable = False)
    value = Column(NUMERIC(10, 2), nullable = True)
    currency = Column(VARCHAR(127), default = "₽")
    maker_id = Column(INTEGER, ForeignKey("maker.id", ondelete = "CASCADE"), nullable = True)
    material_id = Column(INTEGER, ForeignKey("material.id", ondelete = "CASCADE"))
    maker = relationship("Maker", backref = "price", lazy = "subquery")
    # связ для каскадного удаления цены, при удалении материала
    material = relationship("Material", back_populates = "price", lazy = "subquery") 
    # material = relationship("Material", backref="price", lazy = "subquery") 

    __table_args__ = (UniqueConstraint("maker_id", "material_id", name = "price"), )

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
