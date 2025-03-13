from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class PendingVerification(Base):
    __tablename__ = "pending_verification"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    verification_code = Column(String, nullable=False)


class VerifiedEmail(Base):
    __tablename__ = "verified_email"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)


DB_PATH = "sqlite:///bot_database.db"
engine = create_engine(DB_PATH, echo=False, pool_size=5, max_overflow=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db_session():
    return SessionLocal()


def close_db_session(session) -> None:
    session.close()


def add_pending_verification(user_id: int, email: str, verification_code: str) -> None:
    session = get_db_session()
    new_entry = PendingVerification(
        user_id=user_id, email=email, verification_code=verification_code
    )
    session.add(new_entry)
    session.commit()
    close_db_session(session)


def delete_pending_verification(user_id: int) -> None:
    session = get_db_session()
    pending = (
        session.query(PendingVerification)
        .filter(PendingVerification.user_id == user_id)
        .first()
    )
    if pending:
        session.delete(pending)
        session.commit()
    close_db_session(session)


def is_id_verified(user_id: int) -> bool:
    session = get_db_session()

    verified = (
        session.query(VerifiedEmail).filter(VerifiedEmail.user_id == user_id).first()
    )

    session.close()

    return verified is not None


def get_email_by_id(user_id: int) -> str | None:
    session = get_db_session()
    pending = (
        session.query(PendingVerification)
        .filter(PendingVerification.user_id == user_id)
        .first()
    )
    close_db_session(session)
    return str(pending.email) if pending else None


def add_verified_email(user_id: int, email: str) -> None:
    session = get_db_session()
    new_verified_entry = VerifiedEmail(user_id=user_id, email=email)
    session.add(new_verified_entry)
    session.commit()
    close_db_session(session)


def is_email_verified(email: str) -> bool:
    session = get_db_session()
    verified = session.query(VerifiedEmail).filter(VerifiedEmail.email == email).first()
    close_db_session(session)
    return verified is not None


def is_email_pending(email: str) -> bool:
    session = get_db_session()
    pending = (
        session.query(PendingVerification)
        .filter(PendingVerification.email == email)
        .first()
    )
    close_db_session(session)
    return pending is not None


def is_id_pending(user_id: int) -> bool:
    session = get_db_session()
    pending = (
        session.query(PendingVerification)
        .filter(PendingVerification.user_id == user_id)
        .first()
    )
    close_db_session(session)
    return pending is not None


def verify_code(user_id: int, verification_code: str) -> bool:
    session = get_db_session()
    pending = (
        session.query(PendingVerification)
        .filter(
            PendingVerification.user_id == user_id,
            PendingVerification.verification_code == verification_code,
        )
        .first()
    )
    close_db_session(session)
    return pending is not None
