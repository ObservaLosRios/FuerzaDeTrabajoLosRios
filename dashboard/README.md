# Labor Force Dashboard

Clean, modular dashboard for labor force analysis.

## Structure

```
src/
├── core/           # Business logic and entities
├── services/       # Data services
├── components/     # UI components
├── config/         # Configuration
└── main.js         # Application entry point
```

## Usage

```bash
npm run dev    # Development server on port 3000
npm run start  # Production server on port 8080
```

## Architecture

- **Single Responsibility**: Each class has one purpose
- **Open/Closed**: Extensible without modification
- **Dependency Inversion**: Abstractions over implementations
- **Clean Code**: Minimal comments, self-documenting code
