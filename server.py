import uvicorn
import threading
from fastmcp import FastMCP
import httpx
import os
from typing import Optional

mcp = FastMCP("Apitally Python SDK")

APIPALLY_CLIENT_ID = os.environ.get("APITALLY_CLIENT_ID", "")


@mcp.tool()
async def get_setup_guide(framework: str) -> dict:
    """
    Get setup instructions for integrating Apitally with a specific Python web framework.
    Supported frameworks: fastapi, flask, django, starlette, litestar, blacksheep
    """
    framework = framework.lower().strip()

    guides = {
        "fastapi": {
            "framework": "FastAPI",
            "install": "pip install apitally[fastapi]",
            "setup": (
                "from fastapi import FastAPI\n"
                "from apitally.fastapi import use_apitally\n\n"
                "app = FastAPI()\n\n"
                "use_apitally(\n"
                "    app,\n"
                "    client_id=\"your-client-id\",\n"
                "    env=\"dev\",\n"
                ")\n"
            ),
            "docs": "https://docs.apitally.io/frameworks/fastapi",
        },
        "flask": {
            "framework": "Flask",
            "install": "pip install apitally[flask]",
            "setup": (
                "from flask import Flask\n"
                "from apitally.flask import use_apitally\n\n"
                "app = Flask(__name__)\n\n"
                "use_apitally(\n"
                "    app,\n"
                "    client_id=\"your-client-id\",\n"
                "    env=\"dev\",\n"
                ")\n"
            ),
            "docs": "https://docs.apitally.io/frameworks/flask",
        },
        "django": {
            "framework": "Django",
            "install": "pip install apitally[django_ninja] or pip install apitally[django_rest_framework]",
            "setup": (
                "# settings.py\n"
                "MIDDLEWARE = [\n"
                "    \"apitally.django.ApitallyMiddleware\",\n"
                "    ...\n"
                "]\n\n"
                "APITALLY_MIDDLEWARE = {\n"
                "    \"client_id\": \"your-client-id\",\n"
                "    \"env\": \"dev\",\n"
                "}\n"
            ),
            "docs": "https://docs.apitally.io/frameworks/django",
        },
        "starlette": {
            "framework": "Starlette",
            "install": "pip install apitally[starlette]",
            "setup": (
                "from starlette.applications import Starlette\n"
                "from apitally.starlette import use_apitally\n\n"
                "app = Starlette()\n\n"
                "use_apitally(\n"
                "    app,\n"
                "    client_id=\"your-client-id\",\n"
                "    env=\"dev\",\n"
                ")\n"
            ),
            "docs": "https://docs.apitally.io/frameworks/starlette",
        },
        "litestar": {
            "framework": "Litestar",
            "install": "pip install apitally[litestar]",
            "setup": (
                "from litestar import Litestar\n"
                "from apitally.litestar import ApitallyPlugin\n\n"
                "app = Litestar(\n"
                "    plugins=[\n"
                "        ApitallyPlugin(\n"
                "            client_id=\"your-client-id\",\n"
                "            env=\"dev\",\n"
                "        )\n"
                "    ]\n"
                ")\n"
            ),
            "docs": "https://docs.apitally.io/frameworks/litestar",
        },
        "blacksheep": {
            "framework": "BlackSheep",
            "install": "pip install apitally[blacksheep]",
            "setup": (
                "from blacksheep import Application\n"
                "from apitally.blacksheep import use_apitally\n\n"
                "app = Application()\n\n"
                "use_apitally(\n"
                "    app,\n"
                "    client_id=\"your-client-id\",\n"
                "    env=\"dev\",\n"
                ")\n"
            ),
            "docs": "https://docs.apitally.io/frameworks/blacksheep",
        },
    }

    if framework not in guides:
        return {
            "error": f"Framework '{framework}' not recognized.",
            "supported_frameworks": list(guides.keys()),
        }

    return guides[framework]


@mcp.tool()
async def list_supported_frameworks() -> dict:
    """
    List all Python web frameworks supported by Apitally SDK.
    """
    return {
        "supported_frameworks": [
            {
                "name": "FastAPI",
                "key": "fastapi",
                "extra": "apitally[fastapi]",
                "async": True,
                "docs": "https://docs.apitally.io/frameworks/fastapi",
            },
            {
                "name": "Flask",
                "key": "flask",
                "extra": "apitally[flask]",
                "async": False,
                "docs": "https://docs.apitally.io/frameworks/flask",
            },
            {
                "name": "Django (Ninja)",
                "key": "django",
                "extra": "apitally[django_ninja]",
                "async": False,
                "docs": "https://docs.apitally.io/frameworks/django",
            },
            {
                "name": "Django (REST Framework)",
                "key": "django",
                "extra": "apitally[django_rest_framework]",
                "async": False,
                "docs": "https://docs.apitally.io/frameworks/django",
            },
            {
                "name": "Starlette",
                "key": "starlette",
                "extra": "apitally[starlette]",
                "async": True,
                "docs": "https://docs.apitally.io/frameworks/starlette",
            },
            {
                "name": "Litestar",
                "key": "litestar",
                "extra": "apitally[litestar]",
                "async": True,
                "docs": "https://docs.apitally.io/frameworks/litestar",
            },
            {
                "name": "BlackSheep",
                "key": "blacksheep",
                "extra": "apitally[blacksheep]",
                "async": True,
                "docs": "https://docs.apitally.io/frameworks/blacksheep",
            },
        ]
    }


@mcp.tool()
async def get_features_overview() -> dict:
    """
    Get an overview of Apitally's key features and capabilities.
    """
    return {
        "product": "Apitally",
        "tagline": "API monitoring & analytics made simple",
        "description": "Metrics, logs, traces, and alerts for your APIs — with just a few lines of code.",
        "features": [
            {
                "name": "API Analytics",
                "description": "Track traffic, error and performance metrics for your API, each endpoint and individual API consumers.",
            },
            {
                "name": "Request Logs",
                "description": "Drill down from insights to individual API requests. View correlated application logs and traces.",
            },
            {
                "name": "Error Tracking",
                "description": "Understand which validation rules cause client errors. Capture error details and stack traces for 500 responses. Links to Sentry issues.",
            },
            {
                "name": "API Monitoring & Alerts",
                "description": "Get notified immediately with custom alerts, synthetic uptime checks and heartbeat monitoring. Supports email, Slack, and Microsoft Teams.",
            },
        ],
        "links": {
            "website": "https://apitally.io",
            "documentation": "https://docs.apitally.io",
            "github": "https://github.com/apitally/apitally-py",
            "pypi": "https://pypi.org/project/apitally/",
        },
    }


@mcp.tool()
async def get_consumer_tracking_guide(framework: str) -> dict:
    """
    Get guidance on how to identify and track API consumers using Apitally for a given framework.
    Supported frameworks: fastapi, flask, django, starlette, litestar, blacksheep
    """
    framework = framework.lower().strip()

    consumer_examples = {
        "fastapi": {
            "framework": "FastAPI",
            "description": "Use the consumer_callback parameter to identify consumers by returning a string or ApitallyConsumer object.",
            "example": (
                "from fastapi import FastAPI, Request\n"
                "from apitally.fastapi import use_apitally, ApitallyConsumer\n\n"
                "app = FastAPI()\n\n"
                "def identify_consumer(request: Request):\n"
                "    # Return a string identifier or an ApitallyConsumer object\n"
                "    if hasattr(request.state, 'user'):\n"
                "        return ApitallyConsumer(\n"
                "            identifier=str(request.state.user.id),\n"
                "            name=request.state.user.username,\n"
                "        )\n"
                "    return None\n\n"
                "use_apitally(\n"
                "    app,\n"
                "    client_id=\"your-client-id\",\n"
                "    env=\"dev\",\n"
                "    consumer_callback=identify_consumer,\n"
                ")\n"
            ),
            "docs": "https://docs.apitally.io/frameworks/fastapi#identify-consumers",
        },
        "flask": {
            "framework": "Flask",
            "description": "Use the consumer_callback parameter to identify consumers.",
            "example": (
                "from flask import Flask, request\n"
                "from apitally.flask import use_apitally, ApitallyConsumer\n\n"
                "app = Flask(__name__)\n\n"
                "def identify_consumer():\n"
                "    # Access flask.request in the callback\n"
                "    api_key = request.headers.get('X-API-Key')\n"
                "    if api_key:\n"
                "        return api_key\n"
                "    return None\n\n"
                "use_apitally(\n"
                "    app,\n"
                "    client_id=\"your-client-id\",\n"
                "    env=\"dev\",\n"
                "    consumer_callback=identify_consumer,\n"
                ")\n"
            ),
            "docs": "https://docs.apitally.io/frameworks/flask#identify-consumers",
        },
        "default": {
            "description": "Use the consumer_callback parameter in use_apitally() to return a string or ApitallyConsumer object.",
            "ApitallyConsumer_fields": {
                "identifier": "Required. A unique string to identify the consumer.",
                "name": "Optional. A human-readable name for the consumer.",
                "group": "Optional. A group name to categorize consumers.",
            },
            "docs": "https://docs.apitally.io/concepts/consumers",
        },
    }

    if framework in consumer_examples:
        return consumer_examples[framework]
    else:
        result = consumer_examples["default"].copy()
        result["note"] = f"Framework '{framework}' not specifically documented here. Check docs.apitally.io for details."
        return result


@mcp.tool()
async def get_request_logging_config_options() -> dict:
    """
    Get available configuration options for Apitally request logging (RequestLoggingConfig).
    """
    return {
        "class": "RequestLoggingConfig",
        "import": "from apitally.<framework> import RequestLoggingConfig",
        "description": "Configure what gets captured in request logs.",
        "options": [
            {
                "name": "enabled",
                "type": "bool",
                "default": True,
                "description": "Enable or disable request logging.",
            },
            {
                "name": "log_query_params",
                "type": "bool",
                "default": True,
                "description": "Include query parameters in logs.",
            },
            {
                "name": "log_request_headers",
                "type": "bool",
                "default": False,
                "description": "Include request headers in logs.",
            },
            {
                "name": "log_request_body",
                "type": "bool",
                "default": False,
                "description": "Include request body in logs.",
            },
            {
                "name": "log_response_headers",
                "type": "bool",
                "default": False,
                "description": "Include response headers in logs.",
            },
            {
                "name": "log_response_body",
                "type": "bool",
                "default": False,
                "description": "Include response body in logs.",
            },
            {
                "name": "mask_query_params",
                "type": "list[str] | pattern",
                "default": None,
                "description": "Query parameter names to mask in logs.",
            },
            {
                "name": "mask_request_headers",
                "type": "list[str] | pattern",
                "default": None,
                "description": "Request header names to mask in logs.",
            },
            {
                "name": "mask_response_headers",
                "type": "list[str] | pattern",
                "default": None,
                "description": "Response header names to mask in logs.",
            },
        ],
        "example": (
            "from apitally.fastapi import use_apitally, RequestLoggingConfig\n\n"
            "use_apitally(\n"
            "    app,\n"
            "    client_id=\"your-client-id\",\n"
            "    env=\"dev\",\n"
            "    log_query_params=True,\n"
            "    log_request_body=True,\n"
            "    log_response_body=True,\n"
            ")\n"
        ),
        "docs": "https://docs.apitally.io/request-logging",
    }


@mcp.tool()
async def get_installation_instructions(framework: str, include_extras: Optional[str] = None) -> dict:
    """
    Get pip installation instructions for Apitally with the specified framework.
    framework: one of fastapi, flask, django_ninja, django_rest_framework, starlette, litestar, blacksheep
    include_extras: optional comma-separated list of additional extras
    """
    valid_extras = [
        "fastapi",
        "flask",
        "django_ninja",
        "django_rest_framework",
        "starlette",
        "litestar",
        "blacksheep",
    ]

    framework = framework.lower().strip()
    if framework not in valid_extras:
        return {
            "error": f"Framework '{framework}' not recognized.",
            "valid_options": valid_extras,
        }

    extras = [framework]
    if include_extras:
        for extra in include_extras.split(","):
            extra = extra.strip()
            if extra and extra in valid_extras and extra not in extras:
                extras.append(extra)

    extras_str = ",".join(extras)
    pip_command = f"pip install apitally[{extras_str}]"

    python_version_note = "Requires Python >=3.9,<4.0"

    return {
        "framework": framework,
        "pip_command": pip_command,
        "python_version_requirement": python_version_note,
        "pypi_url": "https://pypi.org/project/apitally/",
        "all_available_extras": valid_extras,
        "note": "After installation, call use_apitally() in your app setup with your client_id.",
    }


@mcp.tool()
async def validate_client_id(client_id: str) -> dict:
    """
    Validate the format of an Apitally client ID (UUID format).
    """
    import re

    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE,
    )

    is_valid = bool(uuid_pattern.match(client_id.strip()))

    result = {
        "client_id": client_id,
        "valid_format": is_valid,
    }

    if not is_valid:
        result["message"] = "Client ID should be a UUID in format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        result["where_to_find"] = "You can find your client ID in the Apitally dashboard at https://app.apitally.io"
    else:
        result["message"] = "Client ID format is valid."

    return result




_SERVER_SLUG = "apitally-apitally-py"

def _track(tool_name: str, ua: str = ""):
    try:
        import urllib.request, json as _json
        data = _json.dumps({"slug": _SERVER_SLUG, "event": "tool_call", "tool": tool_name, "user_agent": ua}).encode()
        req = urllib.request.Request("https://www.volspan.dev/api/analytics/event", data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=1)
    except Exception:
        pass

async def health(request):
    return JSONResponse({"status": "ok", "server": mcp.name})

async def tools(request):
    registered = await mcp.list_tools()
    tool_list = [{"name": t.name, "description": t.description or ""} for t in registered]
    return JSONResponse({"tools": tool_list, "count": len(tool_list)})

mcp_app = mcp.http_app(transport="streamable-http", stateless_http=True)

class _FixAcceptHeader:
    """Ensure Accept header includes both types FastMCP requires."""
    def __init__(self, app):
        self.app = app
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            accept = headers.get(b"accept", b"").decode()
            if "text/event-stream" not in accept:
                new_headers = [(k, v) for k, v in scope["headers"] if k != b"accept"]
                new_headers.append((b"accept", b"application/json, text/event-stream"))
                scope = dict(scope, headers=new_headers)
        await self.app(scope, receive, send)

app = _FixAcceptHeader(Starlette(
    routes=[
        Route("/health", health),
        Route("/tools", tools),
        Mount("/", mcp_app),
    ],
    lifespan=mcp_app.lifespan,
))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
