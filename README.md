# SpendSense

A financial management application designed to help users manage, understand, and optimize their spending habits. Built for CS 3200 — Database Design, Spring 2026 at Northeastern University.

## Team Members
- **Rashi Marvadi** 
- **Jake Lawler**  
- **Sophia One** 
- **Kashish Sethi**

## About
SpendSense provides personalized financial tools for four distinct user personas:

- **Students** — Semester budgets, tuition tracking, textbook price comparison, split expenses, and savings goals
- **Financial Analysts** — Portfolio analysis, spending trend reports, and risk/return profiling
- **System Administrators** — Category management, user administration, and data validation
- **9-5 Employees** — Expense tracking, income logging, bill management, and investment monitoring

## Prerequisites
- Docker and Docker Compose installed on your machine
- Git

## Setup & Running

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-REPO/SpendSense.git
   cd SpendSense
   ```

2. **Create the `.env` file** in the `api/` directory using the template:
   ```bash
   cp api/.env.template api/.env
   ```
   Then edit `api/.env` with your database credentials:
   ```
   SECRET_KEY=your-secret-key
   DB_USER=root
   DB_HOST=db
   DB_PORT=3306
   DB_NAME=spendsense
   MYSQL_ROOT_PASSWORD=your-password
   ```

3. **Start the containers**
   ```bash
   docker compose up -d
   ```

4. **Access the app**
   - Streamlit UI: http://localhost:8501
   - Flask API: http://localhost:4000
   - MySQL Database: Port 3200

5. **To rebuild after SQL changes**, delete the database container and volume:
   ```bash
   docker compose down -v
   docker compose up -d
   ```

## Tech Stack
- **Frontend**: Streamlit (Python)
- **Backend API**: Flask (Python)
- **Database**: MySQL 8
- **Containerization**: Docker & Docker Compose

## Demo Video
[Link to demo video — INSERT HERE]

## API Endpoints
The API is organized into 4 blueprints with 35+ routes:
- `/s/` — Student routes (semesters, expenses, textbooks, savings, etc.)
- `/a/` — Analyst routes (reports, portfolios, spending summaries, risk)
- `/ad/` — Admin routes (categories, users, logs, validation)
- `/e/` — Employee routes (expenses, income, investments, bills, insurance)
