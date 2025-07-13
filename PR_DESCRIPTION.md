# 🔍 Integrate Tavily API to Enrich Company Metadata

## Overview
This PR introduces automated company research functionality that significantly enhances the resume analysis process by gathering current, real-time information about companies mentioned in candidates' work experiences. The integration adds a new workflow step that enriches the analysis with up-to-date company data, improving the quality of resume-to-job matching.

## 🎯 Problem Statement
Previously, the CV optimizer relied solely on static information from resumes and job descriptions, missing crucial context about companies in candidates' work history. This limited the system's ability to:
- Understand the relevance and scale of candidate experiences
- Provide context-aware matching based on company industry, size, and market position
- Leverage current company information for better analysis

## 🚀 Key Features

### 1. **Company Research Agent** (`src/core/agents/search_agents.py`)
- **New file** implementing web search-based company research
- Utilizes **Tavily Search API** for real-time company information retrieval
- Implements **structured output** using Pydantic models for consistent data extraction
- Includes **retry logic and error handling** for robust API interactions
- **Configurable time ranges** to prioritize recent information

### 2. **Enhanced Workflow Pipeline** (`src/core/agents/graph_builder.py`)
- **Refactored dependency injection** using `functools.partial` for cleaner node definitions
- **New workflow sequence**: Resume Parsing → **Company Research** → Job Description Parsing → Experience Analysis
- Improved **modularity and testability** of the agent workflow
- Better separation of concerns with dependency injection

### 3. **Structured Data Models** (`src/core/domain/company_search.py`)
- **New Pydantic model** `CompanySearchResponse` for structured company data
- Captures comprehensive company information:
  - Company name, description, website, location
  - Industry classification, employee count, revenue
  - Founding year and other metadata
- Provides **JSON schema generation** for AI model structured output

### 4. **Enhanced Agent State Management** (`src/core/agents/utils/state.py`)
- Added `company_info` field to store researched company information
- Maintains **type safety** with proper typing annotations
- Integrates seamlessly with existing state management

### 5. **Concurrent Processing** (`src/core/agents/utils/nodes.py`)
- New `search_company_info_node` processes all companies from resume experiences
- Implements **concurrent search** using `asyncio.gather()` for optimal performance
- Integrates with existing agent state management system

### 6. **Template Infrastructure**
- New prompt templates for company search queries and system prompts
- Templates optimize search queries for **accuracy and structured data extraction**
- **Configurable search parameters** and response formatting

## 🛠️ Technical Implementation

### API Integration
- **Tavily Search API** integration for real-time web searches
- Optimized for recent and accurate company information
- Configurable search parameters (time range, result count, content filtering)

### Performance Optimizations
- **Asynchronous processing** for concurrent company searches
- **Efficient data structures** for storing and retrieving company information
- **Rate limiting considerations** with TODO for OpenAI rate limit handling

### Code Quality Improvements
- **Removed unused code** from `experience_analyzer.py`
- **Cleaner dependency injection** pattern throughout the workflow
- **Better error handling** and logging for debugging

## 📊 Impact

### For Users
- **Richer analysis** with current company context
- **Better matching accuracy** based on industry and company scale
- **Enhanced insights** into candidate experience relevance

### For Developers
- **Improved code maintainability** with better dependency injection
- **Enhanced testing capabilities** with modular design
- **Extensible architecture** for adding more data sources

## 🔧 Configuration
- **Environment variables** for API keys and configuration
- **Configurable search parameters** (time range, result count)
- **Model selection** for different OpenAI models (gpt-3.5-turbo, gpt-4o)

## 🧪 Testing
- **Unit tests** for experience analyzer functionality
- **Mock providers** for testing without external API calls
- **Template rendering tests** with improved clarity

## 📈 Future Enhancements
- Rate limit handling for OpenAI API calls (TODO added)
- Additional company data sources integration
- Caching mechanisms for frequently searched companies
- Company information validation and accuracy scoring

## 🔒 Security & Privacy
- **Secure API key management** through environment variables
- **Data privacy** considerations for company information handling
- **Error handling** to prevent sensitive information leakage

---

**Breaking Changes**: None - This is a purely additive enhancement that doesn't modify existing functionality.

**Dependencies**: New dependency on Tavily Search API for company information retrieval.