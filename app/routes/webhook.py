


# @app.post("/webhook")
async def handle_webhook(payload: dict):
    # In a real scenario, you would use clerk_sdk.webhooks.verifyWebhook() here
    # to verify the payload's signature before processing.
    event_type = payload.get("type")
    if event_type == "user.created":
        user_data = payload.get("data")
        user_id = user_data.get("id")
        email = user_data.get("email_addresses")[0].get("email_address")
        print(f"New user created: ID={user_id}, Email={email}")
        return {"status": "success", "message": "User created event processed"}
    return {"status": "ignored", "message": "Event type not handled"}