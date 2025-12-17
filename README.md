# SRS Generator

An AI-powered Software Requirements Specification document generator that uses multiple specialized AI models to create comprehensive SRS documents.

## Features

- 🤖 AI-powered generation of SRS sections
- 🌐 Web-based interface for inputting project details
- 📋 GitHub and Linear issue templates for standardized requests
- 📄 Markdown export functionality
- 🐳 Docker support for easy deployment
- 🔄 REST API for programmatic access
- 📊 Real-time document preview

## Documentation

- **[Usage Guide](USAGE_GUIDE.md)** - Complete guide on using the SRS Generator
- **[Template Guide](templates/README.md)** - Documentation for GitHub and Linear templates
- **[Example Template](templates/EXAMPLE_FILLED.md)** - Filled example for reference
- **[SRS Example](SRS.md)** - Sample generated SRS document

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd SRSGenerator
   ```

2. Create `.env` file from template:
   ```bash
   cp .env.example .env
   ```
   Add your OpenRouter API key to the `.env` file.

3. Build and run with Docker:
   ```bash
   docker-compose up --build
   ```

4. Access the application at `http://localhost`

### Manual Setup

1. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scriptsctivate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Add your OpenRouter API key to the `.env` file.

4. Run the development server:
   ```bash
   ./run.sh
   ```

5. Access the application at `http://localhost:5000`

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The project uses:
- Black for Python code formatting
- Flake8 for Python code linting

Format code:
```bash
black .
```

Run linting:
```bash
flake8 .
```

## Templates

The project includes templates for integration with GitHub and Linear:

### GitHub Templates

- **Issue Templates**: Located in `.github/ISSUE_TEMPLATE/`
  - `srs-generation-request.yml` - Request SRS document generation
  - `bug_report.md` - Report bugs
  - `feature_request.md` - Suggest features
- **Pull Request Template**: `.github/PULL_REQUEST_TEMPLATE.md`

### Linear Template

- Located in `templates/LINEAR_TEMPLATE.md`
- Ready to copy into Linear workspace for issue creation

### Using Templates

1. **GitHub**: Go to Issues → New Issue → Select template
2. **Linear**: Settings → Templates → Create new → Paste content from `LINEAR_TEMPLATE.md`

See `templates/README.md` for detailed documentation and `templates/EXAMPLE_FILLED.md` for a complete example.

## Project Structure

```
SRSGenerator/
├── .github/                # GitHub configuration
│   ├── ISSUE_TEMPLATE/    # Issue templates
│   ├── workflows/         # CI/CD workflows
│   └── PULL_REQUEST_TEMPLATE.md
├── backend/               # Flask backend
│   ├── ai/               # AI integration
│   ├── models/           # Database models
│   └── monitoring.py     # Metrics and monitoring
├── frontend/             # Frontend assets
│   └── public/           # Static files
├── templates/            # Project management templates
│   ├── README.md         # Template documentation
│   ├── LINEAR_TEMPLATE.md # Linear issue template
│   └── EXAMPLE_FILLED.md  # Example filled template
├── tests/                # Test suite
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── nginx/                # Nginx configuration
├── Dockerfile            # Production Docker config
└── docker-compose.yml    # Docker composition
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
