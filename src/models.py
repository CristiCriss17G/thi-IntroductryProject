from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.dialects import postgresql

from .database import Base


class Answer(Base):
    __tablename__ = "answers"
    id: int = Column(Integer, primary_key=True, index=True)
    answer: str = Column(String, index=True)
    tags: List[str] = Column(postgresql.ARRAY(String(100)), index=True)
    already_trained: bool = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Answer(id={self.id}, answer={self.answer}, tags={self.tags}, already_trained={self.already_trained})>"


class Settings(Base):
    __tablename__ = "settings"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), index=True, nullable=False, unique=True)
    value: str = Column(String(100), index=True, nullable=False)

    def __repr__(self):
        return f"<Settings(id={self.id}, name={self.name}, value={self.value})>"


class ChatTag(Base):
    __tablename__ = "tag"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), index=True, nullable=True, unique=True)

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"


class ChatStatement(Base):
    __tablename__ = "statement"
    id: int = Column(Integer, primary_key=True, index=True)
    text: str = Column(String(), nullable=True)
    search_text: str = Column(String(), nullable=False)
    conversation: str = Column(String(50), nullable=False)
    created_at: str = Column(postgresql.TIMESTAMP(timezone=True), nullable=True)
    in_response_to: str = Column(String(500), nullable=True)
    search_in_response_to: str = Column(String(500), nullable=False)
    persona: str = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Statement(id={self.id}, text={self.text}, search_text={self.search_text}, conversation={self.conversation}, created_at={self.created_at}, in_response_to={self.in_response_to}, search_in_response_to={self.search_in_response_to}, persona={self.persona})>"


chat_tag_association = Table(
    "tag_association",
    Base.metadata,
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
    Column("statement_id", ForeignKey("statement.id"), primary_key=True),
)


# association_table = Table(
#     "user_avatar_association",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id"), primary_key=True),
#     Column("avatar_id", ForeignKey("avatars.id"), primary_key=True),
# )


# class User(Base):
#     __tablename__ = "users"
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String(50), index=True)
#     email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
#     avatars: Mapped[List["Avatar"]] = relationship(
#         secondary=association_table, back_populates="users"
#     )

#     def __repr__(self):
#         return f"<User(id={self.id}, name={self.name}, email={self.email})>"


# class Avatar(Base):
#     __tablename__ = "avatars"
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     users: Mapped[List["User"]] = relationship(
#         secondary=association_table, back_populates="avatars"
#     )
#     gender: Mapped[str] = mapped_column(String(10), index=True)
#     measurement: Mapped[JSONB] = mapped_column(JSONB, nullable=False)

#     def __repr__(self):
#         return f"<Avatar(id={self.id}, user={self.users.__repr__}, gender={self.gender}), measurement={self.measurement}>"
