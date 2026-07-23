"""Email service — stub for Resend API integration.

In production, replace stub implementations with actual Resend API calls.
See: https://resend.com/docs/api-reference/introduction

Env vars needed in production:
- RESEND_API_KEY: str
- NEWSLETTER_FROM_EMAIL: str = "newsletter@capohornlab.com"
- NEWSLETTER_FROM_NAME: str = "Capo Horn Lab"
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class EmailService:
    """Email sending service with Resend stub.

    Currently logs emails to the console. Replace `_send_via_resend`
    with actual Resend API calls when the API key is configured.
    """

    def __init__(self) -> None:
        self._enabled = False  # Toggle to True when RESEND_API_KEY is set

    async def send_verification_email(
        self,
        to_email: str,
        to_name: Optional[str],
        verification_url: str,
    ) -> bool:
        """Send a double opt-in verification email."""
        subject = "Confirm your newsletter subscription — Capo Horn Lab"
        html = f"""
        <h2>Welcome to Capo Horn Lab</h2>
        <p>Hi {to_name or 'there'},</p>
        <p>Please confirm your email address to subscribe to our newsletter.</p>
        <p><a href="{verification_url}" style="display:inline-block;padding:12px 24px;background:#1a3a5c;color:#fff;text-decoration:none;border-radius:6px;">
            Confirm Subscription
        </a></p>
        <p>If you did not sign up for this newsletter, you can ignore this email.</p>
        <p>— Capo Horn Lab<br><em>Beyond the Market Edge</em></p>
        """
        return await self._send(to_email, subject, html)

    async def send_unsubscribe_confirmation(
        self,
        to_email: str,
        to_name: Optional[str],
    ) -> bool:
        """Send a confirmation that the user has been unsubscribed."""
        subject = "You have been unsubscribed — Capo Horn Lab"
        html = f"""
        <h2>Unsubscribe Confirmed</h2>
        <p>Hi {to_name or 'there'},</p>
        <p>You have been successfully unsubscribed from the Capo Horn Lab newsletter.</p>
        <p>If this was a mistake, you can <a href="#">subscribe again</a> at any time.</p>
        <p>— Capo Horn Lab</p>
        """
        return await self._send(to_email, subject, html)

    async def send_campaign_email(
        self,
        to_email: str,
        to_name: Optional[str],
        subject: str,
        html_content: str,
        unsubscribe_url: str,
    ) -> bool:
        """Send a campaign email to a single subscriber."""
        # Append unsubscribe footer
        full_html = f"""
        {html_content}
        <hr style="margin-top:30px;">
        <p style="font-size:12px;color:#666;">
            <a href="{unsubscribe_url}">Unsubscribe</a> from these emails.
        </p>
        """
        return await self._send(to_email, subject, full_html)

    async def _send(
        self,
        to_email: str,
        subject: str,
        html: str,
    ) -> bool:
        """Internal send method. Stub: logs email instead of sending."""
        logger.info(
            "[EMAIL STUB] To: %s | Subject: %s\n%s",
            to_email,
            subject,
            html[:500],
        )
        if self._enabled:
            return await self._send_via_resend(to_email, subject, html)
        return True  # Stub always succeeds

    async def _send_via_resend(
        self,
        to_email: str,
        subject: str,
        html: str,
    ) -> bool:
        """Actual Resend API call. TODO: implement when API key is available."""
        # from resend import Emails
        # params = {
        #     "from": f"{settings.NEWSLETTER_FROM_NAME} <{settings.NEWSLETTER_FROM_EMAIL}>",
        #     "to": [to_email],
        #     "subject": subject,
        #     "html": html,
        # }
        # response = Emails.send(params)
        # return response["id"] is not None
        raise NotImplementedError("Resend API not yet configured")


# Singleton
email_service = EmailService()
