from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from bot.logging import (
    log_info,
    log_warning,
    log_exception,
)

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
    try:
        Base.metadata.create_all(bind=engine)
        log_info("Database tables created successfully.")
    except SQLAlchemyError as e:
        log_exception(f"Failed to create tables: {e}")
        raise


def get_db_session():
    try:
        return SessionLocal()
    except SQLAlchemyError as e:
        log_exception(f"Failed to get a new session: {e}")
        raise


def close_db_session(session) -> None:
    try:
        session.close()
        log_info("Database session closed.")
    except SQLAlchemyError as e:
        log_exception(f"Failed to close session: {e}")


def add_pending_verification(user_id: int, email: str, verification_code: str) -> None:
    session = None
    try:
        session = get_db_session()
        new_entry = PendingVerification(
            user_id=user_id, email=email, verification_code=verification_code
        )
        session.add(new_entry)
        session.commit()
        log_info(f"Pending verification added for user {user_id} with email {email}.")
    except SQLAlchemyError as e:
        log_exception(
            f"Failed to add pending verification for user {user_id} and email {email}: {e}"
        )
        if session:
            session.rollback()
    finally:
        if session:
            close_db_session(session)


def delete_pending_verification(user_id: int) -> None:
    session = None
    try:
        session = get_db_session()
        pending = (
            session.query(PendingVerification)
            .filter(PendingVerification.user_id == user_id)
            .first()
        )
        if pending:
            session.delete(pending)
            session.commit()
            log_info(f"Pending verification deleted for user {user_id}.")
        else:
            log_warning(f"No pending verification found for user {user_id}.")
    except SQLAlchemyError as e:
        log_exception(f"Failed to delete pending verification for user {user_id}: {e}")
        if session:
            session.rollback()
    finally:
        if session:
            close_db_session(session)


def is_id_verified(user_id: int) -> bool:
    session = None
    try:
        session = get_db_session()
        verified = (
            session.query(VerifiedEmail)
            .filter(VerifiedEmail.user_id == user_id)
            .first()
        )
        return verified is not None
    except SQLAlchemyError as e:
        log_exception(f"Error checking verification status for user {user_id}: {e}")
        return False
    finally:
        if session:
            close_db_session(session)


def get_email_by_id(user_id: int) -> str | None:
    session = None
    try:
        session = get_db_session()
        pending = (
            session.query(PendingVerification)
            .filter(PendingVerification.user_id == user_id)
            .first()
        )
        return str(pending.email) if pending else None
    except SQLAlchemyError as e:
        log_exception(f"Error retrieving email for user {user_id}: {e}")
        return None
    finally:
        if session:
            close_db_session(session)


def add_verified_email(user_id: int, email: str) -> None:
    session = None
    try:
        session = get_db_session()
        new_verified_entry = VerifiedEmail(user_id=user_id, email=email)
        session.add(new_verified_entry)
        session.commit()
        log_info(f"Verified email added for user {user_id} with email {email}.")
    except SQLAlchemyError as e:
        log_exception(
            f"Failed to add verified email for user {user_id} and email {email}: {e}"
        )
        if session:
            session.rollback()
    finally:
        if session:
            close_db_session(session)


def is_email_verified(email: str) -> bool:
    session = None
    try:
        session = get_db_session()
        verified = (
            session.query(VerifiedEmail).filter(VerifiedEmail.email == email).first()
        )
        return verified is not None
    except SQLAlchemyError as e:
        log_exception(f"Error checking verification status for email {email}: {e}")
        return False
    finally:
        if session:
            close_db_session(session)


def is_email_pending(email: str) -> bool:
    session = None
    try:
        session = get_db_session()
        pending = (
            session.query(PendingVerification)
            .filter(PendingVerification.email == email)
            .first()
        )
        return pending is not None
    except SQLAlchemyError as e:
        log_exception(f"Error checking pending status for email {email}: {e}")
        return False
    finally:
        if session:
            close_db_session(session)


def is_id_pending(user_id: int) -> bool:
    session = None
    try:
        session = get_db_session()
        pending = (
            session.query(PendingVerification)
            .filter(PendingVerification.user_id == user_id)
            .first()
        )
        return pending is not None
    except SQLAlchemyError as e:
        log_exception(f"Error checking pending status for user {user_id}: {e}")
        return False
    finally:
        if session:
            close_db_session(session)


def verify_code(user_id: int, verification_code: str) -> bool:
    session = None
    try:
        session = get_db_session()
        pending = (
            session.query(PendingVerification)
            .filter(
                PendingVerification.user_id == user_id,
                PendingVerification.verification_code == verification_code,
            )
            .first()
        )
        return pending is not None
    except SQLAlchemyError as e:
        log_exception(f"Error verifying code for user {user_id}: {e}")
        return False
    finally:
        if session:
            close_db_session(session)
