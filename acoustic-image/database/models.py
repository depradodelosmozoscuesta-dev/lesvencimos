"""SQLite (SQLAlchemy): diccionario de acordes base, transmisiones y capas."""
from __future__ import annotations

from sqlalchemy import JSON, Column, ForeignKey, Integer, LargeBinary, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
ALPHABET = 4096  # abecedario reducido: 4096² = 2^24 parejas = 16.777.216 estados


class BaseChord(Base):
    """Acorde base del abecedario reducido (id 0..4095 -> valor de 24 bits con 12 bits significativos)."""
    __tablename__ = "base_chords"
    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)


class Transmission(Base):
    __tablename__ = "transmissions"
    id = Column(Integer, primary_key=True)
    name = Column(String, default="")
    width, height = Column(Integer), Column(Integer)
    bursts = Column(JSON)           # lista de ráfagas (acordes de 24 bits)
    stream = Column(LargeBinary)    # flujo comprimido (para auditoría)
    layers = relationship("Layer", cascade="all, delete-orphan")


class Layer(Base):
    __tablename__ = "layers"
    id = Column(Integer, primary_key=True)
    transmission_id = Column(Integer, ForeignKey("transmissions.id"))
    idx = Column(Integer)
    rgb = Column(Integer)           # color indexado (24 bits)
    pair_a, pair_b = Column(Integer), Column(Integer)  # el color como pareja de acordes base
    pixels = Column(Integer, nullable=True)


def pair_of_color(rgb: int) -> tuple[int, int]:
    return rgb >> 12, rgb & 0xFFF


def color_of_pair(a: int, b: int) -> int:
    return (a << 12) | b


def open_db(url: str = "sqlite://", **kw):
    from sqlalchemy.pool import StaticPool
    if url == "sqlite://":
        kw.update(connect_args={"check_same_thread": False}, poolclass=StaticPool)
    engine = create_engine(url, **kw)
    Base.metadata.create_all(engine)
    s = sessionmaker(engine)
    with s.begin() as db:
        if not db.query(BaseChord).count():
            db.add_all(BaseChord(id=i, value=i << 12 | (~i & 0xFFF)) for i in range(ALPHABET))
    return s
