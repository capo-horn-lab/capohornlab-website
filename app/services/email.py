"""Transactional email service with a fail-closed Resend adapter.

No API key means no delivery is attempted and callers receive False. This prevents
local development from reporting a fake successful email while keeping tests safe.
"""
from __future__ import annotations

import html
import logging
from typing import Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self) -> None:
        self.api_url = "https://api.resend.com/emails"

    @property
    def enabled(self) -> bool:
        return bool(settings.RESEND_API_KEY)

    async def _send(self, to_email: str, subject: str, content: str, reply_to: str | None = None) -> bool:
        if not self.enabled:
            logger.warning("Transactional email not configured; delivery skipped for %s", to_email)
            return False
        payload = {
            "from": f"{settings.NEWSLETTER_FROM_NAME} <{settings.NEWSLETTER_FROM_EMAIL}>",
            "to": [to_email],
            "subject": subject,
            "html": content,
        }
        if reply_to:
            payload["reply_to"] = reply_to
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}"},
                    json=payload,
                )
            response.raise_for_status()
            return bool(response.json().get("id"))
        except (httpx.HTTPError, ValueError) as exc:
            logger.error("Transactional email delivery failed: %s", type(exc).__name__)
            return False

    async def send_verification_email(self, to_email: str, to_name: Optional[str], verification_url: str) -> bool:
        name = html.escape(to_name or "there")
        url = html.escape(verification_url, quote=True)
        return await self._send(
            to_email,
            "Confirm your newsletter subscription — Capo Horn Lab",
            f"<h2>Welcome to Capo Horn Lab</h2><p>Hi {name},</p><p><a href=\"{url}\">Confirm subscription</a></p>",
        )

    async def send_unsubscribe_confirmation(self, to_email: str, to_name: Optional[str]) -> bool:
        name = html.escape(to_name or "there")
        return await self._send(
            to_email,
            "You have been unsubscribed — Capo Horn Lab",
            f"<h2>Unsubscribe confirmed</h2><p>Hi {name},</p><p>You have been unsubscribed.</p>",
        )

    async def send_campaign_email(self, to_email: str, to_name: Optional[str], subject: str, html_content: str, unsubscribe_url: str) -> bool:
        footer = f'<hr><p><a href="{html.escape(unsubscribe_url, quote=True)}">Unsubscribe</a></p>'
        return await self._send(to_email, subject, html_content + footer)

    async def send_contact_notification(self, visitor_email: str, visitor_name: str, subject: str, message: str) -> bool:
        support_email = settings.SUPPORT_EMAIL
        body = (
            f"<h2>New website contact message</h2>"
            f"<p><strong>From:</strong> {html.escape(visitor_name)} &lt;{html.escape(visitor_email)}&gt;</p>"
            f"<p><strong>Subject:</strong> {html.escape(subject)}</p>"
            f"<p>{html.escape(message).replace(chr(10), '<br>')}</p>"
        )
        return await self._send(support_email, f"[Website Contact] {subject}", body, reply_to=visitor_email)

    async def send_contact_acknowledgement(self, to_email: str, to_name: str, subject: str) -> bool:
        return await self._send(
            to_email,
            "We received your message — Capo Horn Lab",
            f"<p>Hi {html.escape(to_name)},</p><p>We received your message about <strong>{html.escape(subject)}</strong> and will reply by email.</p>",
        )

    async def send_account_verification(self, to_email: str, code: str) -> bool:
        return await self._send(
            to_email,
            "Verify your Capo Horn Lab account",
            f"<p>Your verification code is <strong>{html.escape(code)}</strong>.</p><p>This code expires in 15 minutes.</p>",
        )

    async def send_password_reset(self, to_email: str, code: str) -> bool:
        return await self._send(
            to_email,
            "Reset your Capo Horn Lab password",
            f"<p>Your password reset code is <strong>{html.escape(code)}</strong>.</p><p>This code expires in 15 minutes.</p>",
        )


email_service = EmailService()
