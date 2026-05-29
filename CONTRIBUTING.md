# Contributing to AgriSmartRwanda

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Development Process

1. Fork the repo and create your branch from `main`
2. If you've added code, add tests
3. If you've changed APIs, update documentation
4. Ensure tests pass
5. Make sure code follows style guidelines
6. Issue a pull request!

## Coding Style

### Python
- Follow PEP 8
- Use Black for formatting
- Max line length: 88 characters

### JavaScript/React
- Use ESLint and Prettier
- Use functional components
- Add comments for complex logic

## Setup Development Environment

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm start
```

### Docker
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Testing

### Backend
```bash
pytest
pytest --cov=api
```

### Frontend
```bash
npm test
```

## Reporting Bugs

Include:
- OS and Python/Node version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

## License

By contributing, you agree your contributions will be licensed under the MIT License.