import hashlib
import hmac
import time

from fastapi import Header, HTTPException, Request, status

from app.config import settings


async def verify_hmac_signature(
    request: Request,
    x_signature: str = Header(None, alias="X-Signature"),
    x_timestamp: str = Header(None, alias="X-Timestamp"),
):
    # 1. Enforce presence of required cryptographic headers
    if not x_signature or not x_timestamp:
        raise HTTPException(
            status_code=403, detail="Access denied: Missing signature attributes."
        )

    try:
        # 2. Check for Replay Attacks (Reject requests older than 30 seconds)
        request_time = int(x_timestamp) / 1000.0
        current_time = time.time()

        if abs(current_time - request_time) > 30.0:
            raise HTTPException(
                status_code=403, detail="Access denied: Request signature expired."
            )

        # Read the raw, unparsed request bytes body directly from the stream
        raw_body_bytes = await request.body()
        raw_body_str = raw_body_bytes.decode("utf-8")

        # Reconstruct the message signature footprint
        message_to_sign = (x_timestamp + raw_body_str).encode("utf-8")

        # Compute local HMAC-SHA256 signature
        computed_hash = hmac.new(
            settings.INTERNAL_SHARED_SECRET,
            message_to_sign,
            hashlib.sha256,
        ).hexdigest()

        # Execute time-constant string comparison to completely mitigate Timing Attacks
        if not hmac.compare_digest(computed_hash, x_signature):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid cryptographic hash token signature alignment.",
            )

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Malformed cryptographic verification metadata.",
        ) from err
    return True
