# Awareness WhatsApp Bot

A Flask webhook that returns short awareness FAQ answers over WhatsApp. It
validates Twilio's request signature and labels every reply as awareness-only,
not medical advice.

## Run locally

1. Copy `.env.example` to `.env` and set `TWILIO_AUTH_TOKEN` to your Twilio
   account Auth Token. Keep `.env` private; it is excluded by `.gitignore`.
2. Start the server:

   ```powershell
   .\venv\Scripts\python.exe app.py
   ```

3. In another terminal, expose port 5000:

   ```powershell
   ngrok http 5000
   ```

4. In the Twilio WhatsApp Sandbox settings, set **When a message comes in** to
   your ngrok HTTPS URL followed by `/whatsapp`, and select **HTTP POST**.
5. Each tester must join your Sandbox by sending its displayed `join <code>` to
   the Sandbox number.

The webhook recognizes messages containing `dengue` or `hygiene`. Other
messages receive a safe fallback directing the user to a doctor or 104.

## Awareness broadcasts

The current app handles inbound FAQ messages; it does not send scheduled or
group broadcasts. Before adding an outbound sender, account for WhatsApp's
messaging rules:

- A user-initiated message opens a 24-hour customer-service window, measured
  from the most recent user message. Free-form replies are allowed during that
  window. Outside it, business-initiated messages require a pre-approved
  template.
- In the Twilio Sandbox, only users who joined that specific Sandbox can
  receive messages. The Sandbox supports only its pre-approved templates for
  business-initiated messages and does not support custom templates. Joining
  starts a customer-service window, so a free-form test message can be sent
  during that window.
- The Sandbox is for testing, not production. Production use requires
  registering a WhatsApp sender with Twilio. Requirements for business
  verification depend on the account and onboarding path; do not assume that
  every production setup has the same verification prerequisite.
- Send alerts only to people who have agreed to receive them. A scheduled or
  button-triggered sender must handle expired windows with an approved
  template and surface Twilio delivery errors.

## Demo tips

- Test on venue Wi-Fi and keep a phone hotspot available. A free ngrok URL
  changes after restart, so update the Sandbox webhook URL each time.
- Keep a screen recording as a backup.
- Demonstrate a known FAQ, an unknown question and its fallback, and an
  outbreak-alert flow only when the recipient's messaging window or an
  approved template permits it.

## Twilio references

- [WhatsApp API: notifications and the 24-hour customer-service window](https://www.twilio.com/docs/whatsapp/api)
- [WhatsApp Sandbox: joining, limits, and templates](https://www.twilio.com/docs/whatsapp/sandbox)
- [Sending WhatsApp notifications with templates](https://www.twilio.com/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates)
