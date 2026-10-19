# Updated to v1.68.1 (2026-10-12)

## What's New

(2026-09-04)

### Fixed

- **Genericized example names in tests, docs, and examples.** Fixture people and companies now use fictional names throughout. Behavior is unchanged.

## Google Workspace Integration

Claudia connects to your full Google Workspace: Gmail, Calendar, Drive, Docs, Sheets, Tasks, and more through one server.

**Quick setup:** Run `npx get-claudia google` to configure it interactively. It will generate a one-click URL to enable all required APIs at once.

Or see the Google Integration Setup section in CLAUDE.md for manual configuration. If you enable new APIs later, remember to re-authenticate (delete ~/.workspace-mcp/token.json and restart Claude Code).

## Your Complete Skill Set

### Proactive (auto-activate)
- **onboarding** - Guide new users through a conversational discovery flow to create a personalized Claudia setup
- **structure-generator** - Create personalized folder structures and files based on user archetype and workflow needs
- **memory-manager** - Handle cross-session persistence using MCP tools from the claudia-memory server, with fallback to markdown files. Activates at session start to load context and session end to save learnings. Use when memory tools respond, fail, or are unavailable.
- **agent-dispatcher** - Detects when to delegate tasks to specialized agents with two-tier dispatch
- **judgment-awareness** - Load and apply user-defined judgment rules from context/judgment.yaml to inform priority conflicts, escalation decisions, surfacing, and delegation
- **commitment-detector** - Automatically detect promises and commitments in conversation and offer to track them
- **pattern-recognizer** - Notice trends, recurring themes, and patterns across conversations and surface them when relevant. Activates when the same topic, frustration, or behavior appears across 3+ interactions.
- **relationship-tracker** - Surface relevant context when people are mentioned and track relationship health with velocity-based reconnection suggestions
- **risk-surfacer** - Proactively identify and surface potential problems using velocity-based relationship trends and commitment risk detection
- **capability-suggester** - Notice repeated user behaviors and suggest new commands, workflows, structure, or integrations to streamline work. Also detects when the user's setup has outgrown its current structure and suggests targeted upgrades.
- **hire-agent** - Suggests new agents based on repeated task patterns
- **vault-awareness** - Manage Obsidian vault projection with syncing, bidirectional edits, canvas generation, and vault-to-memory import

### Contextual (natural language or /command)
- **/client-health** - Health check across active client engagements showing status, deliverables, and concerns
- **/financial-snapshot** - Quick view of revenue, expenses, invoicing, and cash flow with key metrics
- **/growth-check** - Periodic reflection on development, skills, learning, and progress toward goals
- **/databases** - View all Claudia memory databases, switch between them, manage isolation
- **/brain-monitor** - Terminal dashboard for real-time memory stats and activity
- **/diagnose** - Check memory system health and troubleshoot connectivity issues. Use when memory commands aren't working, at session start if something seems wrong, or when user asks about memory status.
- **/inbox-check** - Lightweight inbox triage across all configured email accounts with two-tier fetch and judgment. Use when user asks about their email.
- **/meeting-prep** - One-page briefing before a call or meeting with person context, open items, and talking points. Use when user is preparing for a meeting or call.
- **/capture-meeting** - Process meeting notes or transcript to extract decisions, commitments, insights, and relationship updates. Use when user shares notes from a call or meeting.
- **/summarize-doc** - Create an executive summary of any document at the appropriate level of detail
- **/memory-audit** - Show everything Claudia knows with provenance tracing and entity counts
- **/brain** - Launch the 3D Brain Visualizer showing entities, relationships, and memories as an interactive graph
- **/fix-duplicates** - Find and merge duplicate entities in the memory system
- **/memory-health** - Check memory system health and data quality with stats and recommendations
- **/file-document** - Store a document, email, or text for future reference with entity linking and provenance
- **/new-person** - Create a relationship tracking file for a person with contact info, history, and communication preferences. Use when user mentions someone important who doesn't have a file yet.
- **/new-workspace** - Create a workspace skeleton for a new project, client, or venture with populated templates and dashboard. Use when starting a new engagement or project.
- **/connector-discovery** - Help users connect external tools in a gentle, non-technical way with plain language guidance
- **/research** - Deep research on a topic with web sources, memory integration, and stored findings. Also handles quick context-aware lookups when current information would improve the conversation.
- **/what-am-i-missing** - Surface risks, blind spots, overlooked items, and accountability across commitments and relationships
- **/map-connections** - Scan context files to extract entities and relationships into the memory system
- **/weekly-review** - Guided weekly reflection across all relationships, commitments, and projects with pattern analysis. Use at end of week for structured reflection.
- **/meditate** - End-of-session reflection generating persistent learnings about user preferences, communication patterns, and cross-session insights. Also extracts judgment rules from decisions made during the session.
- **/pipeline-review** - Review active pipeline, opportunities, capacity, and stalled items needing attention
- **/deep-context** - Full-context deep analysis using memory_deep_context compound tool (single call replaces 6-8 sequential calls) for comprehensive synthesis

### Explicit (/command only)
- **/feedback** - Send feedback, ideas, or bug reports about Claudia via GitHub Discussions
- **/build-team** - Propose a personalized team of specialized agents based on the user profile and real work, validated by an independent Checker, applied on approval with rollback.
- **/morning-brief** - Daily digest organized by urgency: overdue commitments, upcoming deadlines, reconnection suggestions, and recent changes. Activates at the start of the day or when user asks about their agenda.
- **/draft-reply** - Draft an email response with tone matching the relationship context. Shows draft for approval before sending.
- **/follow-up-draft** - Create a post-meeting thank-you or follow-up email with key points and next steps. Use after a meeting capture when next steps need communicating.
- **/ingest-sources** - Process multiple source documents with Extract-Then-Aggregate discipline. Use when user shares multiple transcripts, emails, or documents for batch processing.

## Memory System
Memory operations use MCP tools from the claudia-memory daemon (memory_recall, memory_remember, memory_about, etc.).
The daemon provides ~33 tools for semantic search, pattern detection, and relationship tracking.
See the memory-manager skill for the full tool reference.

---
_Surface this update in your first greeting, then delete this file._
