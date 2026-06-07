# Voice Assistant

A personal assistant with a primary voice interface, designed to run entirely on-premises while remaining accessible over the internet.

## Objective

Build a personal assistant whose primary interface is voice — always listening, always available, with no reliance on external cloud services for core functionality.

## Requirements

### 1. Voice Interface
The system MUST use voice as its primary interface. Text-based interfaces MAY exist as secondary or diagnostic surfaces.

### 2. Available Over the Internet
The system MUST be reachable over the public internet. Users MUST NOT be required to use a VPN or be on the local network to access it.

### 3. All Components and Data On-Premises
All components MUST run on the local machine. All data MUST be stored on the local machine. No data MUST leave the local system to third-party services.

### 4. Swappable TTS, STT, and LLM via Configuration
The TTS engine, STT engine, and LLM MUST each be independently replaceable via configuration. No code changes MUST be required to swap any of these components.

### 5. Specialized Domain Tools
The assistant MUST support calling into domain-limited tools with narrow responsibilities (e.g., calendar, home automation, search). New tools MUST be addable without modifying core assistant logic.

## Development Conventions

- Pydantic MUST be preferred over dataclasses for structured data.

## Requirements

### 6. Hands-Free Operation
The system MUST NOT require the user to press a button or interact with a UI to begin or end a conversation. Listening MUST begin on a wake word and MUST end on an end word. The screen CAN be on.
