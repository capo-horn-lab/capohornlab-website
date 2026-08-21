"""Poll the local API contact table and print a compact JSON list (no engine logs)."""
import asyncio
import json
import logging
import sys

import sqlalchemy
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.contact_message import ContactMessage


async def main() -> None:
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    async with AsyncSessionLocal() as db:
        rows = (
            (await db.execute(select(ContactMessage).order_by(ContactMessage.created_at.desc()).limit(8)))
            .scalars()
            .all()
        )
        print(
            json.dumps(
                [{"t": r.created_at.isoformat(), "n": r.name, "s": r.subject} for r in rows]
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
