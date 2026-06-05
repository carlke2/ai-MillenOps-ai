# Smart Ops AI Service: Technical Direction Document

## 1. Executive Summary & Architecture Principles

The **Smart Ops AI Service** is a single, unified stateless Python/FastAPI microservice containing many distinct AI modules. It is designed to power the AI features of the enterprise Smart Facility & Support Operations System. It acts as an independent AI engine that receives context from the core NestJS system, processes the data through rule-based baselines or ML models, and returns actionable insights, predictions, and recommendations.

**Core Architectural Principles:**
*   **Statelessness:** The AI service maintains no persistent state or direct database connections. It relies entirely on the payload provided in each request.
*   **Decoupled Source of Truth:** NestJS and its PostgreSQL database remain the single source of truth. The AI service does not mutate data directly; it advises NestJS.
*   **Auditable & Transparent:** Every AI response includes a `confidence` score, an `explanation` of the reasoning, the `modelVersion` used, and a clear `recommendation`.
*   **Safety First:** AI outputs require human confirmation for critical actions (e.g., booking creation, room release, ticket assignment) unless explicitly overridden by strict automation rules configured in NestJS.
*   **Confidence Thresholds:** Automated actions or strong recommendations are only permitted if the model's `confidence` score exceeds a module-specific threshold (e.g., 0.85).
*   **Service-to-Service Security:** All communication between NestJS and the AI service must be secured via API keys or internal service tokens.
*   **Shadow Mode Deployment:** New ML models will initially run in "shadow mode," generating predictions for audit in `AiInsight` without triggering real-world actions.
*   **Graceful Degradation:** The system always falls back to rule-based logic if ML inference is unavailable, ensuring continuous operation.

---

## 2. System Integration & Data Flow

### 2.1 The Integration Flow (NestJS ↔ FastAPI)

1.  **Trigger Event (NestJS):** An event occurs in the system (e.g., a user submits a ticket, a visitor arrives, a booking is near its end).
2.  **Context Gathering (NestJS):** NestJS queries PostgreSQL/Redis to gather all necessary context for the AI decision (e.g., user history, room availability, ticket details).
3.  **Request Construction (NestJS):** NestJS formats the context into a predefined JSON payload and enqueues a job via BullMQ to the `AI_INFERENCE_QUEUE` or makes a direct synchronous HTTP call to the FastAPI service depending on the urgency (e.g., Chatbot is sync, Forecasting is async).
4.  **AI Inference (FastAPI):**
    *   FastAPI receives the payload via the specific endpoint.
    *   The payload is validated using Pydantic models.
    *   The relevant module processes the data (using rule-based logic or a loaded ML model).
    *   An standard output payload is constructed containing the result, confidence, explanation, and model version.
5.  **Response Handling (NestJS):**
    *   NestJS receives the FastAPI response.
    *   NestJS logs the complete interaction (request, response, timing) into the `AiInsight` table.
    *   NestJS applies its own business logic to the recommendation (e.g., checking confidence thresholds).
    *   If confidence is high, NestJS may apply the recommendation automatically (if rules allow) or present it to a human user for confirmation via the frontend.
6.  **Feedback Loop (Optional/Future):** When a user confirms or corrects an AI recommendation, NestJS logs this feedback to improve future ML models.

### 2.2 Standard Payloads

**Standard AI Output Payload (FastAPI → NestJS):**
```json
{
  "success": true,
  "capability": "ticket-classification",
  "correlationId": "uuid-from-nestjs-request",
  "recommendation": { ... }, // Module-specific structure
  "confidence": 0.85,        // 0.0 to 1.0
  "explanation": "Matched based on historical data of similar issues.",
  "modelVersion": "rule_v1.0" // e.g., "rule_v1.0", "ml_xgb_v2.1"
}
```

---

## 3. Module Deep Dives

### 1. Ticket Categorization AI (`app/modules/tickets/classification`)
*   **Purpose:** Automatically assign categories and subcategories to newly submitted IT or Facility support tickets based on the title and description.
*   **Input payload:** `{ "ticketId": "uuid", "title": "string", "description": "string", "submitterRole": "string" }`
*   **Output payload:** `{ "category": "string", "subCategory": "string" }` (inside standard payload)
*   **Endpoint:** `POST /v1/tickets/classify`
*   **Rule-based baseline:** Keyword matching (e.g., if description contains "wifi" -> "IT/Network").
*   **Future ML approach:** Start with rules, then implement TF-IDF + Logistic Regression, and later advance to fine-tuned or zero-shot LLMs as needed.
*   **Data needed:** Historical tickets with their resolved categories.
*   **NestJS role:** Send ticket creation event; store classification in DB if confidence > threshold, else flag for review.
*   **FastAPI role:** Parse text, apply keywords/model, return category.
*   **Stored in AiInsight:** Original text, suggested category, confidence, explanation (e.g., matched keywords).
*   **Human confirmation:** Required if confidence < 0.70. Submitter or support agent can manually change it.
*   **Testing:** Provide a test set of 100 historical tickets; measure accuracy against actual human-assigned categories.

### 2. Priority Suggestion AI (`app/modules/tickets/priority`)
*   **Purpose:** Determine the urgency of a ticket based on sentiment, keywords (e.g., "urgent", "broken", "VIP"), and submitter profile.
*   **Input payload:** `{ "ticketId": "uuid", "title": "string", "description": "string", "submitterRole": "string", "category": "string" }`
*   **Output payload:** `{ "priority": "LOW|MEDIUM|HIGH|CRITICAL", "slaRecommended": "string" }`
*   **Endpoint:** `POST /v1/tickets/priority`
*   **Rule-based baseline:** High priority if submitted by CEO or contains "fire/flood". Medium if "broken". Low otherwise.
*   **Future ML approach:** NLP sentiment analysis + Random Forest using submitter role and category as features.
*   **Data needed:** Historical tickets with priority levels and SLA breach history.
*   **NestJS role:** Apply recommended priority if above threshold; trigger SLA workflows based on result.
*   **FastAPI role:** Evaluate urgency signals.
*   **Stored in AiInsight:** Factors contributing to priority (e.g., "VIP submitter detected").
*   **Human confirmation:** PM/Support can override.
*   **Testing:** Validate against known critical incidents to ensure no false negatives on "CRITICAL".

### 3. Intelligent Routing AI (`app/modules/tickets/routing`)
*   **Purpose:** Suggest the best technician or support group to handle a ticket based on workload, skills, and past resolution history.
*   **Input payload:** `{ "ticketId": "uuid", "category": "string", "priority": "string", "availableTechs": [{"id": "uuid", "skills": [], "currentLoad": 3}] }`
*   **Output payload:** `{ "suggestedAssigneeId": "uuid", "alternativeAssigneeIds": ["uuid"] }`
*   **Endpoint:** `POST /v1/tickets/route`
*   **Rule-based baseline:** Round-robin assignment among technicians who possess the required skill for the category and have load < max.
*   **Future ML approach:** Collaborative filtering or reinforcement learning based on time-to-resolve per technician for specific categories.
*   **Data needed:** Technician skill matrices, historical ticket assignment and resolution times.
*   **NestJS role:** Fetch active technicians and their current load; present recommendation to PM or auto-assign if allowed.
*   **FastAPI role:** Score technicians based on fit and availability.
*   **Stored in AiInsight:** Why a tech was chosen (e.g., "Lowest current load + matching skill").
*   **Human confirmation:** PM must confirm assignment unless automation rules specifically permit auto-routing for low-priority issues.
*   **Testing:** Scenario testing: verify it doesn't assign to overloaded techs or those without the right skills.

### 4. Room Recommendation AI (`app/modules/rooms/recommendation`)
*   **Purpose:** Suggest the optimal meeting room based on capacity, requested equipment, proximity, and schedule availability.
*   **Input payload:** `{ "attendeeCount": int, "durationMins": int, "requiredEquipment": ["string"], "preferredFloor": int, "availableRooms": [{"id": "uuid", "capacity": int, "equipment": [], "floor": int}] }`
*   **Output payload:** `{ "recommendedRoomIds": ["uuid"], "matchScores": {"roomId": float} }`
*   **Endpoint:** `POST /v1/rooms/recommend`
*   **Rule-based baseline:** Filter out unavailable/under-capacity rooms, sort by capacity (closest to requested without being under) and equipment match.
*   **Future ML approach:** Learning user preferences over time (e.g., CEO always prefers Boardroom A even if B is closer).
*   **Data needed:** Room details, historical booking preferences per user.
*   **NestJS role:** Provide only currently available rooms to FastAPI; present recommendations in UI.
*   **FastAPI role:** Calculate fitness score for each room.
*   **Stored in AiInsight:** Recommendation criteria (e.g., "Best capacity match, 100% equipment match").
*   **Human confirmation:** User must select the room to finalize booking.
*   **Testing:** Ensure rooms missing required equipment score zero. Ensure capacity limits are strictly respected.

### 5. Meeting Assistant AI (`app/modules/meetings/assistant`)
*   **Purpose:** Help users plan meetings by parsing intent and suggesting the complete booking setup.
*   **Input payload:** `{ "intentText": "Schedule a client meeting next Tuesday at 11am for 5 people", "userProfile": {...} }`
*   **Output payload:** `{ "parsedIntent": { "date": "...", "time": "...", "attendees": 5 }, "actionNeeded": "needs_room" }`
*   **Endpoint:** `POST /v1/meetings/parse-intent`
*   **Rule-based baseline:** Regex for date/time/numbers.
*   **Future ML approach:** Named Entity Recognition (NER) via LLM.
*   **Data needed:** N/A (requires good NER model).
*   **NestJS role:** Send user chat text; use parsed intent to call Room Recommendation AI.
*   **FastAPI role:** Extract structured data from unstructured text.
*   **Stored in AiInsight:** Original text, extracted entities.
*   **Human confirmation:** User must review the proposed booking details before confirming.
*   **Testing:** Unit tests with various phrasings of meeting requests.

### 6. Visitor Reception AI (`app/modules/visitors/reception`)
*   **Purpose:** Process uninvited visitor details at a kiosk and extract purpose of visit.
*   **Input payload:** `{ "visitorName": "string", "company": "string", "purposeText": "string" }`
*   **Output payload:** `{ "visitCategory": "DELIVERY|INTERVIEW|CLIENT_MEETING|PERSONAL|OTHER", "urgency": "string" }`
*   **Endpoint:** `POST /v1/visitors/reception-intent`
*   **Rule-based baseline:** Keyword matching (e.g., "drop off", "package" -> DELIVERY).
*   **Future ML approach:** Text classification.
*   **Data needed:** Historical kiosk entry logs.
*   **NestJS role:** Send kiosk input; route visitor flow based on category (e.g., deliveries straight to mailroom).
*   **FastAPI role:** Classify visit purpose.
*   **Stored in AiInsight:** Extracted purpose category.
*   **Human confirmation:** Receptionist dashboard flag for "OTHER" or low confidence.
*   **Testing:** Test with common visitor inputs.

### 7. Visitor Matching AI (`app/modules/visitors/matching`)
*   **Purpose:** Match an uninvited visitor to the correct internal host based on partial names, department, or purpose.
*   **Input payload:** `{ "requestedHostName": "string", "visitorPurpose": "string", "employeeDirectory": [{"id", "name", "department", "role"}] }`
*   **Output payload:** `{ "matchedEmployeeId": "uuid", "alternatives": ["uuid"] }`
*   **Endpoint:** `POST /v1/visitors/match-host`
*   **Rule-based baseline:** Fuzzy string matching (Levenshtein distance) on names.
*   **Future ML approach:** Semantic matching based on role + purpose (e.g., "Here to fix AC" matches to Facility Manager).
*   **Data needed:** Employee directory, previous visitor logs.
*   **NestJS role:** Provide active directory list; send notification to matched host.
*   **FastAPI role:** Execute fuzzy matching and scoring.
*   **Stored in AiInsight:** Match score, matched name vs requested name.
*   **Human confirmation:** Kiosk asks visitor "Did you mean [Name]?" before notifying.
*   **Testing:** Test with misspellings of common employee names.

### 8. Meeting Reminder AI (`app/modules/meetings/reminders`)
*   **Purpose:** Determine the optimal time to send a wrap-up reminder before a meeting ends, considering if the room is booked right after.
*   **Input payload:** `{ "bookingId": "uuid", "endTime": "iso", "nextBookingStartTime": "iso|null" }`
*   **Output payload:** `{ "sendReminderAt": "iso", "reminderMessage": "string" }`
*   **Endpoint:** `POST /v1/meetings/reminder-schedule`
*   **Rule-based baseline:** If next booking is within 15 mins, remind 10 mins before end. If room is free, remind 5 mins before end.
*   **Future ML approach:** Predict likelihood of meeting overrunning based on meeting type/host history.
*   **Data needed:** Calendar schedules.
*   **NestJS role:** Schedule the notification job based on returned time.
*   **FastAPI role:** Calculate time difference and select message template.
*   **Stored in AiInsight:** Scheduled time, reason (e.g., "Back-to-back meeting detected").
*   **Human confirmation:** None (automated notifications).
*   **Testing:** Logic validation for edge cases (e.g., meeting ends at end of day).

### 9. No-Show Prediction AI (`app/modules/bookings/no_show`)
*   **Purpose:** Predict the likelihood that a booked meeting will be a no-show (ghost meeting) to optimize room utilization.
*   **Input payload:** `{ "bookingId": "uuid", "hostId": "uuid", "attendeeCount": int, "isRecurring": boolean, "timeSinceBooking": int }`
*   **Output payload:** `{ "noShowProbability": float }`
*   **Endpoint:** `POST /v1/bookings/predict-no-show`
*   **Rule-based baseline:** Probability increases if recurring + small attendee count + booked far in advance.
*   **Future ML approach:** Logistic Regression based on host's historical no-show rate.
*   **Data needed:** Historical booking completion vs no-show data.
*   **NestJS role:** If probability > threshold, trigger a "Please confirm your meeting" notification to the host 1 hour before.
*   **FastAPI role:** Calculate probability score.
*   **Stored in AiInsight:** No-show probability and primary contributing factors.
*   **Human confirmation:** Requires host to explicitly cancel or confirm; AI does not cancel.
*   **Testing:** Evaluate prediction accuracy against a holdout dataset.

### 10. Smart Room Release AI (`app/modules/rooms/release`)
*   **Purpose:** Analyze sensor data (if available) or check-in status to recommend releasing a booked room if it appears empty.
*   **Input payload:** `{ "bookingId": "uuid", "minutesSinceStart": int, "sensorActivityLevel": float }`
*   **Output payload:** `{ "shouldRelease": boolean, "reason": "string" }`
*   **Endpoint:** `POST /v1/rooms/evaluate-release`
*   **Rule-based baseline:** Release if minutesSinceStart > 15 AND no manual check-in AND sensorActivityLevel == 0.
*   **Future ML approach:** Time-series analysis of sensor data to distinguish between an empty room and a quiet meeting.
*   **Data needed:** Real-time sensor data, check-in status.
*   **NestJS role:** Execute room release if recommendation is true AND system policies allow auto-release.
*   **FastAPI role:** Evaluate release conditions.
*   **Stored in AiInsight:** Reason for release recommendation.
*   **Human confirmation:** Only allowed without confirmation if strict "15-minute no-show auto-release" policy is active in NestJS.
*   **Testing:** Simulate sensor data streams.

### 11. Facility Usage Forecasting AI (`app/modules/facilities/forecasting`)
*   **Purpose:** Predict future facility usage (room occupancy, visitor traffic) to help with resource planning (e.g., cleaning schedules).
*   **Input payload:** `{ "historicalUsageData": [...], "targetDate": "iso" }`
*   **Output payload:** `{ "predictedOccupancyRate": float, "predictedVisitorCount": int, "peakHours": ["string"] }`
*   **Endpoint:** `POST /v1/facilities/forecast`
*   **Rule-based baseline:** Moving average of the same day-of-week over the past 4 weeks.
*   **Future ML approach:** ARIMA or Prophet models considering seasonality, holidays, and company events.
*   **Data needed:** Long-term historical usage data, calendar of company holidays.
*   **NestJS role:** Send daily batch job to generate forecast; display on Admin Dashboard.
*   **FastAPI role:** Run time-series forecasting.
*   **Stored in AiInsight:** Forecasted values for audit against actuals later.
*   **Human confirmation:** Informational only.
*   **Testing:** Backtesting against historical data.

### 12. Admin Operations Intelligence AI (`app/modules/admin/operations_insights`)
*   **Purpose:** Generate natural language summaries of system health and operational metrics for the admin dashboard.
*   **Input payload:** `{ "metrics": {"openTickets": 50, "slaBreaches": 2, "roomUtilization": 0.8} }`
*   **Output payload:** `{ "summaryText": "string", "keyInsights": ["string"], "actionableAlerts": ["string"] }`
*   **Endpoint:** `POST /v1/admin/insights`
*   **Rule-based baseline:** Template-based generation (e.g., "Room utilization is high at 80%.").
*   **Future ML approach:** LLM-generated summaries highlighting anomalous patterns not immediately obvious in raw data.
*   **Data needed:** Aggregated daily/weekly metrics.
*   **NestJS role:** Collect metrics and request summary for dashboard load.
*   **FastAPI role:** Generate human-readable insights.
*   **Stored in AiInsight:** Generated summary text.
*   **Human confirmation:** Informational only.
*   **Testing:** Verify output matches input metrics accurately (no hallucinations).

### 13. User Help Chatbot AI (`app/modules/helpdesk/chatbot`)
*   **Purpose:** Answer basic "how-to" questions and triage system issues for end-users.
*   **Input payload:** `{ "userMessage": "string", "conversationHistory": [...] }`
*   **Output payload:** `{ "replyText": "string", "intent": "SUPPORT_TICKET|INFO|GREETING", "escalate": boolean }`
*   **Endpoint:** `POST /v1/helpdesk/chat`
*   **Rule-based baseline:** FAQ keyword matching (e.g., "book" + "room" -> return link to booking guide).
*   **Future ML approach:** RAG (Retrieval-Augmented Generation) using company documentation and an LLM.
*   **Data needed:** FAQ documents, system usage guides.
*   **NestJS role:** Manage chat sessions; if escalate=true, open ticket creation modal.
*   **FastAPI role:** Generate response based on knowledge base.
*   **Stored in AiInsight:** User query, provided answer, escalation status.
*   **Human confirmation:** If intent=SUPPORT_TICKET, user must fill out ticket form to confirm.
*   **Testing:** Evaluate against a test set of common user questions.

### 14. Anomaly Detection AI (`app/modules/anomalies/detection`)
*   **Purpose:** Identify unusual patterns in system usage (e.g., a sudden spike in login failures, or a single user booking 20 rooms in a day).
*   **Input payload:** `{ "recentActivityLogs": [...] }`
*   **Output payload:** `{ "anomaliesDetected": [{"type": "string", "severity": "string", "details": "string"}] }`
*   **Endpoint:** `POST /v1/anomalies/detect`
*   **Rule-based baseline:** Static thresholds (e.g., >5 failed logins/min = anomaly).
*   **Future ML approach:** Isolation Forest or Autoencoders on activity log streams.
*   **Data needed:** ActivityLog data stream.
*   **NestJS role:** Send logs periodically; generate Admin Alerts if anomalies found.
*   **FastAPI role:** Detect statistical outliers.
*   **Stored in AiInsight:** Detected anomalies and their severity.
*   **Human confirmation:** Admin reviews alerts.
*   **Testing:** Inject synthetic anomalies into test data and verify detection.

### 15. Workforce Insight AI (`app/modules/workforce/insight`)
*   **Purpose:** Analyze support team workload and ticket resolution times to identify burnout risks or training needs.
*   **Input payload:** `{ "technicianStats": [{"id", "ticketsClosed", "avgResolutionTime", "openTickets", "slaBreachRate"}] }`
*   **Output payload:** `{ "insights": [{"technicianId": "uuid", "riskLevel": "HIGH|LOW", "observation": "string"}] }`
*   **Endpoint:** `POST /v1/workforce/analyze`
*   **Rule-based baseline:** Flag High risk if openTickets > threshold OR slaBreachRate > threshold.
*   **Future ML approach:** Clustering technicians to identify outliers in performance vs load.
*   **Data needed:** Aggregated support performance data.
*   **NestJS role:** Request analysis for PM dashboard.
*   **FastAPI role:** Generate risk assessments based on stats.
*   **Stored in AiInsight:** Risk assessments.
*   **Human confirmation:** PM uses data for management decisions; AI takes no direct action.
*   **Testing:** Validate flags against known high-load scenarios.

---

## 4. Execution & Testing Strategy

### 4.1 Safety First Execution
The AI service adheres strictly to the "advise, don't mutate" principle. All destructive or state-changing actions (creating bookings, releasing rooms, assigning tickets) require explicit human confirmation via the NestJS frontend UI unless the system administrator has explicitly configured a bypassing "Automation Rule" in NestJS for a specific, high-confidence AI recommendation.

### 4.2 Data Privacy
*   **No HR/Payroll Data:** The AI service never receives PII beyond what is strictly necessary (e.g., names for visitor matching).
*   **No Persistent Data:** The AI service drops the payload immediately after generating a response.

### 4.3 Testing Before Deployment
1.  **Unit Testing & Golden Dataset:** Each FastAPI module will have PyTest coverage validating logic against mocked JSON payloads. Additionally, a "golden dataset" of verified inputs and expected outputs must be maintained to test ML models against regressions.
2.  **Integration Testing:** NestJS E2E tests will spin up the FastAPI service in a Docker container to verify the HTTP/Queue integration and ensure NestJS correctly handles the standard AI payload structure.
3.  **Shadow Mode:** For ML models, they will run in "shadow mode" first. They will receive production data and generate predictions stored in `AiInsight`, but NestJS will ignore the recommendations for automated actions. PMs can review the accuracy in the dashboard before enabling active use.
4.  **Fallback Verification:** Tests must explicitly break the FastAPI service (e.g., shut it down) and verify that NestJS gracefully falls back to standard, non-AI operations without throwing 500 errors to the user.

### 4.4 Build Order Justification
1.  **FastAPI Foundation:** Necessary boilerplate (Pydantic models, error handling, logging, Docker setup).
2.  **Ticket modules (2-4):** Immediate value for support teams; data is highly structured.
3.  **Room/Meeting modules (5-11):** Core product features; higher complexity involving scheduling math.
4.  **Admin/Analytics modules (12-15):** Relies on data generated by the system; best built last when system usage is understood.
