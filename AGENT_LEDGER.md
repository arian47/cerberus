# Autonomous Agent Project Ledger

**Purpose:** This file acts as the continuous memory and changelog for the AI agent. It tracks architectural decisions, modifications, and project evolution. 
**Agent Instruction:** You MUST prepend your newest entry directly below this header block. Strictly adhere to the format of the example entry.

---

## [2026-02-22 22:55] - Fix MiniMax API Key Loading Issue
**Task ID / PR Reference:** N/A

### 1. Core Changes
* **Modified:** `.env` - Removed quotes around MINIMAX_API_KEY value causing 401 authentication errors.
* **Modified:** `cerberus.py` - Added `load_env()` function to properly load environment variables from .env file at startup.

### 2. Rationale & Architecture
* **Why:** The MiniMax API was returning 401 errors because the API key in .env had surrounding quotes, and the main cerberus.py wasn't loading the .env file properly.
* **Architecture Alignment:** Added environment variable loading at script initialization to ensure all API keys are available before use.

### 3. Recommendations & Next Steps
* **Technical Debt:** Consider moving all environment loading to a centralized config module.
* **Next Iteration:** Add validation for .env file format on startup.

---

## [YYYY-MM-DD HH:MM] - [Brief Title of the Feature/Fix]
**Task ID / PR Reference:** [Optional PR number or Jira/Task ID]

### 1. Core Changes
* **Added:** `src/auth/token_validator.py` - Created a standalone microservice module for JWT validation.
* **Modified:** `src/api/routes.py` - Decoupled standard routing from authentication checks.
* **Deleted:** `src/utils/old_auth_helpers.py` - Removed legacy monolithic auth functions.

### 2. Rationale & Architecture
* **Why:** The API routing file was becoming monolithic and hard to test. 
* **Architecture Alignment:** By extracting the token validation into its own module, we move closer to a microservices architecture. This allows the auth service to be tested and scaled independently of the main API routes.

### 3. Recommendations & Next Steps
* **Technical Debt:** The database connection strings in `routes.py` still need to be abstracted into a dedicated database module.
* **Next Iteration:** I recommend creating a `db_manager` microservice in the next session to handle connection pooling.

---