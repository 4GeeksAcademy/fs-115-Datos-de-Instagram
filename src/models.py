from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from eralchemy2 import render_er

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str] = mapped_column(Text)
    profile_picture: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")
    followers: Mapped[list["Follower"]] = relationship(
        foreign_keys="[Follower.user_id]", back_populates="user"
    )
    following: Mapped[list["Follower"]] = relationship(
        foreign_keys="[Follower.follower_id]", back_populates="follower"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "bio": self.bio,
            "profile_picture": self.profile_picture,
            "created_at": self.created_at.isoformat(),
        }


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
        }


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
            "post_id": self.post_id,
        }


class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)      
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)  

    user: Mapped["User"] = relationship(foreign_keys=[user_id], back_populates="followers")
    follower: Mapped["User"] = relationship(foreign_keys=[follower_id], back_populates="following")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "follower_id": self.follower_id,
        }
    
    render_er(db.Model, "diagram.png")