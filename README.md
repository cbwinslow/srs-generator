# SRS Generator

An AI-powered Software Requirements Specification document generator that uses multiple specialized AI models to create comprehensive SRS documents.

## Features

- Web-based interface for inputting project details
- AI-powered generation of SRS sections
- Multiple specialized AI models for different aspects of requirements
- Markdown export functionality
- Docker support for easy deployment

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

## Project Structure

```
SRSGenerator/
├── backend/                 # Flask backend
│   ├── ai/                 # AI integration
│   ├── models/             # Database models
│   └── templates/          # Flask templates
├── frontend/               # Frontend assets
│   └── public/             # Static files
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── nginx/                  # Nginx configuration
├── Dockerfile             # Production Docker config
└── docker-compose.yml     # Docker composition
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
