from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from typing import Annotated
from uuid import UUID, uuid4


str256 = Annotated[str, mapped_column(String(256), nullable=False)]
uuidpk = Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]
