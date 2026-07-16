from typing import Any

import httpx

from app.config import settings
from app.logger import logger


async def call_express_execution_sandbox(
    language: str,
    code: str,
    input_data: str = ""
) -> dict[str, Any]:
    """
    Dispatches a code execution request back to the Express backend's
    secure sandboxed workspace runner.
    """
    url = f"{settings.EXPRESS_API_URL}/execute"
    payload = {
        "language": language,
        "code": code,
        "input": input_data
    }
    
    logger.info("Dispatching execution payload to Express sandbox at %s", url)
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code != 200:
                logger.error("Express sandbox returned status code %d", response.status_code)
                return {
                    "success": False,
                    "stdout": "",
                    "stderr": f"Sandbox service returned error status: {response.status_code}",
                }
                
            data = response.json()
            return {
                "success": data.get("success", False),
                "stdout": data.get("output", ""),
                "stderr": data.get("error", "")
            }
            
    except httpx.RequestError as exc:
        logger.exception("Failed to establish connection with Express execution service")
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution sandbox communication failure: {exc!s}"
        }