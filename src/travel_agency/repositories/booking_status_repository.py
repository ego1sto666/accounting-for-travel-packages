"""Работа с таблицей BookingStatus (справочник статусов брони)."""

from database.database import get_connection
from models.booking_status import BookingStatus


def _map(row) -> BookingStatus:
    return BookingStatus(*row)


def get_all() -> list[BookingStatus]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT statusID, name FROM BookingStatus ORDER BY statusID")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_id(status_id: int) -> BookingStatus | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT statusID, name FROM BookingStatus WHERE statusID = ?",
        (status_id,),
    )
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None
