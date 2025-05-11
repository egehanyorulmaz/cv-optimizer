# CV Optimizer (Still in Progress)

A multi-agent solution to optimize resumes using AI, focusing on providing intelligent feedback while maintaining privacy and accessibility.

## Vision
CV Optimizer aims to democratize access to high-quality resume optimization using AI. We help job seekers present their best professional selves while reducing bias and improving job market accessibility.

## Key Features
- 🤖 Intelligent resume parsing and analysis
- 📊 ATS (Applicant Tracking System) optimization
- 🔒 Privacy-first approach with PII protection
- 🎯 Job description matching
- ✍️ Smart content improvement suggestions
- 🌍 Multi-format support (PDF, DOCX, TXT)
- 🔄 Career development planning

## Architecture
Built using hexagonal architecture principles with a LangGraph-based workflow, ensuring:
- Clean separation of concerns
- Pluggable AI providers
- Extensible agent system
- Comprehensive testing

This is a side project that I'm currently working on, but I intend to deliver an end-to-end product until the end of this year. For more details about the vision, visit [CV Optimizer Notion Page](https://marmalade-cilantro-afb.notion.site/CV-Optimizer-13ad4b67bf9980338f2dd35552053751).

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy the example environment file:
   ```
   cp env.example .env
   ```
5. Configure your environment variables in `.env`:
   - Add your OpenAI API key
   - Set up LangSmith for tracing (optional)
6. Run tests to verify setup:
   ```
   pytest
   ```

## LangGraph Flow

The application uses LangGraph to create a workflow that analyzes resumes and job descriptions:

1. Parse Resume → Parse Job Description → Experience Analyzer → ...

More nodes will be added as development continues.

## Development

To contribute to the project:

1. Set up the environment as described above
2. Install development dependencies if not already included
3. Follow the existing code style patterns
4. Add tests for new functionality
5. Ensure all existing tests pass

## License

[MIT License](LICENSE)
