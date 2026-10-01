# MediaStreamX - Polyglot Media & Streaming Microservices

## Overview
MediaStreamX is a deployable prototype of a Netflix-like media platform. It contains eight independent services implemented in four languages:

| Service | Language | Port | Main responsibility |
|---|---|---:|---|
| catalog-service | JavaScript | 8101 | Media catalogue and search |
| streaming-service | JavaScript | 8102 | Playback session creation |
| auth-service | Python | 8103 | Login and token validation |
| recommendation-service | Python | 8104 | Simple content recommendations |
| watchlist-service | Java | 8105 | Add/list/remove saved media |
| history-service | Java | 8106 | Record and read watch history |
| subscription-service | C# | 8107 | Subscription plans and status |
| notification-service | C# | 8108 | User notifications |

The prototype uses in-memory storage so it can be started immediately without a database. The service boundaries, HTTP APIs, configuration files, tests, Dockerfiles, Compose file and Jenkins pipeline are included so the project can be used as a base for a larger deployment.

## Folder structure
The layout intentionally follows the supplied VS Code project style: an `analyzer` folder, a `sample_microservices` folder containing services and one central `config` folder, a `scripts` folder, a `tests` folder, and root deployment/documentation files.

```text
media_streaming_microservices/
├── analyzer/
├── sample_microservices/
│   ├── config/
│   ├── catalog-service/
│   ├── streaming-service/
│   ├── auth-service/
│   ├── recommendation-service/
│   ├── watchlist-service/
│   ├── history-service/
│   ├── subscription-service/
│   └── notification-service/
├── scripts/
├── tests/
├── .gitignore
├── docker-compose.yml
├── Jenkinsfile
├── requirements.txt
├── Setup.py
└── README.md
```

## Requirements
Install Docker Desktop or Docker Engine with Docker Compose. For local development, install Node.js 20+, Python 3.12+, Java 17+, Maven 3.9+, and .NET 8 SDK. The supplied Dockerfiles are the recommended way to run the complete system because they pin the major runtime versions.

## Start the complete platform
```bash
docker compose up --build
```

The eight services are then available on ports 8101-8108. Health endpoints are available at `/health` on every service.

## Stop the platform
```bash
docker compose down
```

## Run the automated tests
```bash
python scripts/run_all_tests.py
```

The script runs the language-specific test suites and then runs the repository integration smoke test. A normal development machine with the listed language toolchains can run it without changing source code.

## API examples
Login:
```bash
curl -X POST http://localhost:8103/login -H "Content-Type: application/json" -d '{"email":"demo@example.com","password":"demo123"}'
```

List media:
```bash
curl http://localhost:8101/movies
```

Start playback:
```bash
curl -X POST http://localhost:8102/stream/start -H "Content-Type: application/json" -d '{"userId":"u1","mediaId":"m1"}'
```

Add to watchlist:
```bash
curl -X POST http://localhost:8105/watchlist -H "Content-Type: application/json" -d '{"userId":"u1","mediaId":"m1"}'
```

Subscribe:
```bash
curl -X POST http://localhost:8107/subscribe -H "Content-Type: application/json" -d '{"userId":"u1","plan":"premium"}'
```

## Important prototype note
The application is intentionally self-contained and does not require a database, Kubernetes, cloud account, CDN or external identity provider. Data is kept in memory and is reset when a service restarts. This makes the project deployable immediately for demonstration and testing. A production system would normally replace these stores with durable databases, object storage, a CDN, a real authentication provider and a message broker.

## Configuration
All service configuration files are placed in `sample_microservices/config`, as requested. JavaScript configuration is JavaScript, Python configuration is Python, Java configuration is Java properties, and C# configuration is JSON. Each service's Dockerfile copies only the configuration file it needs into the service container.

## Testing approach
Every service contains a unit test file and an integration test file. Unit tests exercise service logic without opening a network socket. Integration tests start the actual HTTP server on an ephemeral local port and send HTTP requests to it. The root `tests/integration_smoke_test.py` checks the deployed Docker Compose endpoints when the platform is running.

## CI/CD
`Jenkinsfile` installs the required toolchains through the Jenkins agent image, runs the four language test suites, builds all Docker images, starts the Compose stack, executes the smoke test and tears the stack down in the post stage.

## Images
The `docs/architecture.svg` file is the architecture image. It is deliberately generated as an SVG so it stays readable in documentation and source control.
