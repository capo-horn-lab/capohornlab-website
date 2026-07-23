"""App models — all SQLAlchemy models should be imported here for Alembic."""

from app.models.user import User
from app.models.login_history import LoginHistory
from app.models.strategy_request import StrategyRequest
from app.models.status_history import StatusHistory
from app.models.attachment import Attachment
from app.models.internal_note import InternalNote
from app.models.newsletter import NewsletterCampaign, NewsletterSend, NewsletterSubscriber

__all__ = [
    "User",
    "LoginHistory",
    "StrategyRequest",
    "StatusHistory",
    "Attachment",
    "InternalNote",
    "NewsletterSubscriber",
    "NewsletterCampaign",
    "NewsletterSend",
]
