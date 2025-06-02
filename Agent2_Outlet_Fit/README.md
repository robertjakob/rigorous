# Agent2_Outlet_Fit

> **Note:** This module is currently in active development. It will help reviewers evaluate manuscripts against specific journal/conference criteria and support desk rejection decisions.

## Purpose

Agent2_Outlet_Fit is designed to:
- Evaluate manuscript fit with target journals/conferences
- Support journals/conferences in desk rejection decisions
- Enable researchers to pre-check manuscripts before submission

## Status

🚧 **In Development**
- Core functionality being implemented
- Integration with Agent1_Peer_Review in progress
- Testing and validation ongoing

## Contributing

This project is open source under the MIT License. We welcome contributions from the community to help improve the AI Peer Reviewer system. Please feel free to submit issues, pull requests, or suggestions for improvements.

## STATUS: 🚧 IN PLANNING PHASE
This tool is currently in the planning and development phase. It aims to serve two key purposes:
1. Help reviewers evaluate manuscripts against specific journal/conference criteria
2. Assist journals and conferences in desk rejection decisions by providing automated preliminary screening
3. Enable researchers to pre-check their manuscripts against target outlet requirements before submission

## GAMEPLAN: Agen2_outletfit

## 🎯 INPUTS:
- journal_query: A string representing a journal, e.g., "I want to publish at NPJ Digital Medicine" found in context folder
- manuscript_pdf: A PDF academic manuscript to be evaluated found in manuscripts folder

---

## FUNCTIONAL LAYERS & AGENT SPECIFICATIONS:


### 1. OUTLET RESEARCH AGENTS
Goal: Automatically extract journal-specific publishing criteria from online sources.

**Agents:**
- PolicyCrawlerAgent: Scrapes official submission guidelines, formatting, ethics, and referencing requirements.
- ScopeAnalyzerAgent: Analyzes the journal's aims and scope to determine topical fit.
- EditorialBehaviorAgent: Uses recent articles (titles, abstracts) to infer preferred methodologies and topics.
- LanguageStyleAgent: Learns linguistic norms (hedging, tone, formality) from past published texts.
- ImpactNoveltyAgent: Extracts what kinds of novelty or significance are expected.
- ReviewerExpectationAgent: Simulates or extracts typical reviewer priorities (optional).

---

### 2. CRITERIA SYNTHESIS AGENTS
Goal: Convert raw data into structured, weighted publishing criteria.

**Agents:**
- CriteriaGeneratorAgent: Translates scraped data into JSON/YAML schemas for validation.
- CriteriaWeightingAgent: Assigns priorities or must-have/optional tags to criteria.
- RiskHeuristicAgent: Estimates desk-rejection risk based on missing or weak components.

---

### 3. MANUSCRIPT EVALUATION AGENTS
Goal: Assess the manuscript against journal-specific requirements.

**Agents:**
- PDFParserAgent: Extracts and segments text from the manuscript PDF.
- SectionValidatorAgent: Verifies section presence, structure, and ordering.
- ScopeFitAgent: Checks if manuscript topic aligns with journal scope (via semantic similarity).
- LanguageConformityAgent: Assesses tone and style match with outlet norms.
- ReferenceStyleCheckerAgent: Verifies correct citation and formatting style.
- OverallFitSummaryAgent: Outputs a summary of compliance, risks, and improvement suggestions.

---

## 🧱 ARCHITECTURE:
Use LangChain or CrewAI to orchestrate agents.

Each agent should:
- Be modular and reusable
- Accept clearly defined input/output types
- Use tools such as:
  - Playwright, BeautifulSoup → web scraping
  - FAISS, OpenAI Embeddings → semantic matching
  - PyMuPDF or GROBID → PDF parsing
  - LLM API → reasoning and language evaluation

---

## ✅ OUTPUT:
A JSON report that includes:
- ✔️ Fulfilled requirements
- ❌ Missing elements
- 📈 Desk rejection likelihood (1-5 scale)
- ✍️ Specific suggestions to better fit the journal

---

## GOAL:
Build a multiagent pipeline that automatically reverse-engineers a target outlet's expectations and assesses a manuscript's fit. The tool serves three key purposes:

1. **For Reviewers**: Streamline the review process by automatically checking manuscripts against journal/conference criteria
2. **For Journals/Conferences**: Support faster desk rejection decisions by providing automated preliminary screening and fast feedback to authors
3. **For Researchers**: Enable pre-submission self-assessment to identify potential issues before formal submission

This comprehensive approach aims to reduce desk rejection risk, improve submission strategy, and make the peer review process faster more efficient for all stakeholders.
