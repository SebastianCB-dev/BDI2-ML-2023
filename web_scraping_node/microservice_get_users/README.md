# Instagram User Scraper Microservice

A robust Node.js microservice built with TypeScript that automatically scrapes Instagram following lists and stores user data in a PostgreSQL database. This service runs continuously, updating user information every 3 minutes.

## 🎯 Purpose

This microservice is designed to automatically collect and maintain an up-to-date database of Instagram users from your following list. It's particularly useful for:

- Social media analytics and monitoring
- Building follower databases for marketing purposes
- Tracking changes in user profiles over time
- Data collection for machine learning projects

## 🏗️ Architecture

The microservice follows a clean architecture pattern with the following components:

- **ScraperGetUsers**: Main scraping logic using Puppeteer
- **Database**: PostgreSQL connection and data operations
- **Logger**: Winston-based logging system
- **Environment Validation**: Ensures all required environment variables are set

## 🚀 Features

- **Automated Scraping**: Continuously scrapes Instagram following lists every 3 minutes
- **Intelligent Updates**: Only updates user records when full names change
- **Duplicate Prevention**: Prevents duplicate entries in the database
- **Headless Operation**: Runs in headless mode in production for optimal performance
- **Comprehensive Logging**: Detailed logging with Winston for monitoring and debugging
- **Docker Support**: Containerized for easy deployment
- **TypeScript**: Fully typed for better code quality and maintainability
- **Environment-based Configuration**: Different settings for development and production

## 📋 Prerequisites

- Node.js 18+ or Node.js 20.9.0 (as specified in Dockerfile)
- PostgreSQL database
- Valid Instagram account credentials
- pnpm package manager

## 📦 Dependencies

### Production Dependencies

- **puppeteer** (v21.3.8): Web scraping and browser automation
- **pg** (v8.11.3): PostgreSQL client for Node.js
- **winston** (v3.11.0): Logging library for comprehensive logging
- **dotenv** (v16.3.1): Environment variable management
- **colors** (v1.4.0): Console output coloring for better readability
- **module-alias** (v2.2.3): Module path aliasing for cleaner imports

### Development Dependencies

- **typescript** (v5.2.2): TypeScript compiler
- **@types/pg** (v8.10.7): TypeScript definitions for PostgreSQL
- **ts-standard** (v12.0.2): TypeScript linting with JavaScript Standard Style

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd microservice_get_users
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Set up environment variables**
   ```bash
   cp sample.env .env
   ```

4. **Configure environment variables** in `.env`:
   ```env
   # Global variables
   ENVIRONMENT=development  # or production
   
   # Instagram credentials
   INSTAGRAM_USERNAME=your_instagram_username
   INSTAGRAM_PASSWORD=your_instagram_password
   
   # PostgreSQL connection
   POSTGRES_URL=postgresql://username:password@localhost:5432/database_name
   ```

5. **Set up the database**
   - Create a PostgreSQL database
   - Run the SQL script located at `src/DB/scripts/get_users_script.sql`

## 🗄️ Database Schema

The service creates a `users` table with the following structure:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    fullname VARCHAR(255),
    user_status user_status NOT NULL DEFAULT 'PENDING',
    registration_date TIMESTAMP DEFAULT NOW()
);
```

### User Status Enum
```sql
CREATE TYPE user_status AS ENUM ('PENDING', 'REVIEWED');
```

### Indexes
- `idx_users_username`: Index on username for faster queries

## 🚀 Usage

### Development Mode

```bash
# Build TypeScript
pnpm run build

# Start the service
pnpm start

# Or run both commands together
pnpm run typescript && node dist/bootstrap.js
```

### Production Mode with Docker

```bash
# Build the Docker image
docker build -t instagram-scraper .

# Run the container
docker run -d \
  --name instagram-scraper \
  -e ENVIRONMENT=production \
  -e INSTAGRAM_USERNAME=your_username \
  -e INSTAGRAM_PASSWORD=your_password \
  -e POSTGRES_URL=your_postgres_url \
  instagram-scraper
```

## 📜 Available Scripts

- `pnpm run typescript`: Compile TypeScript to JavaScript
- `pnpm start`: Build and start the application
- `pnpm run build`: Build the project (alias for typescript)
- `pnpm run lint`: Run TypeScript Standard linter
- `pnpm run lint:fix`: Run linter and automatically fix issues

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ENVIRONMENT` | Runtime environment (development/production) | Yes | - |
| `INSTAGRAM_USERNAME` | Instagram account username | Yes | - |
| `INSTAGRAM_PASSWORD` | Instagram account password | Yes | - |
| `POSTGRES_URL` | PostgreSQL connection string | Yes | - |

### Browser Configuration

The service automatically configures Puppeteer based on the environment:

**Development Mode:**
- Headless: `false` (visible browser)
- Args: `['--disable-extensions', '--lang=en']`

**Production Mode:**
- Headless: `true` (no visible browser)
- Args: `['--no-sandbox', '--disable-extensions', '--lang=en', '--disable-dev-shm-usage', '--disable-gpu', '--incognito']`

## 📊 How It Works

1. **Initialization**: Validates environment variables and establishes database connection
2. **Browser Launch**: Starts Puppeteer with environment-specific configuration
3. **Instagram Login**: Authenticates using provided credentials
4. **Navigation**: Goes to user's profile and accesses following list
5. **Data Extraction**: Scrolls through the entire following list and extracts usernames and full names
6. **Database Operations**: 
   - Inserts new users
   - Updates full names of existing users if changed
   - Skips users that haven't changed
7. **Continuous Operation**: Repeats the process every 3 minutes (180,000ms)

## 📈 Logging

The service uses Winston for comprehensive logging:

- **Info Logs**: Successful operations, timing information
- **Error Logs**: Failures, exceptions, and error details
- **File Logging**: Logs are saved to the `logs/` directory
  - `combined.log`: All logs
  - `error.log`: Error logs only
  - Date-based rotation for long-term storage

## 🐳 Docker Configuration

The Dockerfile uses a multi-stage build process:

1. **Builder Stage**: 
   - Uses Node.js 20.9.0 Alpine
   - Installs dependencies and builds TypeScript

2. **Production Stage**:
   - Uses Node.js 20.9.0 Alpine
   - Installs only production dependencies
   - Copies built application
   - Runs the service

## 🔒 Security Considerations

- Keep Instagram credentials secure and never commit them to version control
- Use strong PostgreSQL passwords
- Consider using environment variable injection in production deployments
- The service runs in incognito mode in production for additional privacy
- Database connections use connection pooling for better security and performance

## 🚨 Error Handling

The service includes comprehensive error handling:

- **Environment Validation**: Exits if required environment variables are missing
- **Database Connection**: Validates connection before proceeding
- **Login Failures**: Handles Instagram authentication errors
- **Scraping Errors**: Manages DOM changes and network issues
- **Database Operations**: Handles SQL errors and connection issues

## 📋 Monitoring

Monitor the service through:

- **Log Files**: Check `logs/` directory for detailed operation logs
- **Database Records**: Monitor the `users` table for data collection progress
- **Process Status**: Ensure the service remains running continuously

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow TypeScript Standard style guidelines
4. Add appropriate tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Please ensure you comply with Instagram's Terms of Service and respect rate limits. Use responsibly and consider the privacy implications of data collection.

## 🔧 Troubleshooting

### Common Issues

1. **Instagram Login Failures**
   - Verify credentials are correct
   - Check if Instagram requires additional verification
   - Ensure account is not restricted

2. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check connection string format
   - Ensure database exists and user has proper permissions

3. **Puppeteer Issues**
   - Install missing dependencies on Linux systems
   - Check if Chrome/Chromium is available in the container
   - Verify memory limits in containerized environments

4. **Class Name Changes**
   - Instagram frequently updates their UI
   - Check `src/constants/classes.constant.ts` for current selectors
   - Update selectors if scraping fails

For additional support, check the logs in the `logs/` directory for detailed error information.
