#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class Ticket:
    id: int
    summary: str
    status: str = "open"


class DemoServiceDeskAgent:
    def __init__(self) -> None:
        self._tickets: dict[int, Ticket] = {}
        self._next_id = 1001

    def handle(self, message: str) -> str:
        text = message.strip()
        lower = text.lower()

        if not text:
            return "Please describe your issue."

        if lower.startswith("status"):
            return self._handle_status(lower)

        if any(word in lower for word in ("reset", "password", "vpn", "email")):
            return self._suggest_kb(lower)

        return self._create_ticket(text)

    def _create_ticket(self, summary: str) -> str:
        ticket = Ticket(id=self._next_id, summary=summary)
        self._tickets[ticket.id] = ticket
        self._next_id += 1
        return (
            f"Ticket #{ticket.id} created.\n"
            f"Summary: {ticket.summary}\n"
            "Priority: medium\n"
            "Status: open"
        )

    def _handle_status(self, lower_message: str) -> str:
        parts = lower_message.split()
        if len(parts) < 2 or not parts[1].isdigit():
            return "Usage: status <ticket_id>"
        ticket_id = int(parts[1])
        ticket = self._tickets.get(ticket_id)
        if ticket is None:
            return f"Ticket #{ticket_id} not found."
        return (
            f"Ticket #{ticket.id}\n"
            f"Summary: {ticket.summary}\n"
            f"Status: {ticket.status}"
        )

    def _suggest_kb(self, lower_message: str) -> str:
        if "password" in lower_message:
            return "KB-101: Password reset guide - https://example.local/kb/101"
        if "vpn" in lower_message:
            return "KB-205: VPN troubleshooting - https://example.local/kb/205"
        if "email" in lower_message:
            return "KB-310: Email sync issues - https://example.local/kb/310"
        return "KB-001: Service desk quickstart - https://example.local/kb/001"


def main() -> None:
    agent = DemoServiceDeskAgent()
    print("Demo ServiceDesk Agent")
    print("Type a problem to create a ticket, or 'status <id>' to check status.")
    print("Type 'exit' to quit.")

    while True:
        try:
            user_input = input("> ")
        except EOFError:
            break
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        print(agent.handle(user_input))


if __name__ == "__main__":
    main()
