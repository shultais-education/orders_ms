from sqlmodel import SQLModel, Field
import sqlalchemy as sa


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: int | None = Field(default=None, primary_key=True)
    house_id: int = Field(sa_column=sa.Column(sa.Integer, nullable=False, index=True))

    user_name: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    user_phone: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    user_email: str = Field(sa_column=sa.Column(sa.String, nullable=False, index=True))
