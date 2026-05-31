# Cloud-Based Secure Web Application (DevSecOps)

A secure, scalable and highly available web application deployed on AWS with DevSecOps practices.

## Project Overview
A Flask-based Todo/Notes application built with full DevSecOps implementation including AWS Cloud infrastructure, security hardening, CI/CD pipeline, and monitoring.

## Tech Stack
- **Backend:** Python Flask
- **Database:** MySQL (AWS RDS)
- **Server:** Ubuntu (AWS EC2)
- **Web Server:** Nginx + Gunicorn
- **Container:** Docker
- **CI/CD:** GitHub Actions
- **Monitoring:** AWS CloudWatch
- **Storage:** AWS S3

## Architecture
- VPC with Public and Private Subnets
- EC2 Instance in Public Subnet
- RDS MySQL in Private Subnet
- Application Load Balancer
- S3 for backups
- CloudWatch for monitoring

## Security Features
- Password hashing with bcrypt
- HTTPS/SSL with AWS ACM
- JWT-based sessions
- SQL Injection prevention (ORM)
- XSS protection (CSP headers)
- Rate limiting (Nginx)
- SSH hardening + Fail2ban
- UFW Firewall
- Security headers

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/fathimafarzeena960-cell/my-capstone-project.git
cd my-capstone-project
```

### 2. Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set environment variables
```bash
export DATABASE_URL='mysql+pymysql://admin:password@your-rds-endpoint:3306/tododb'
export SECRET_KEY='your-secret-key'
```

### 4. Run the application
```bash
gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
```

## Live Demo
- **URL:** http://3.107.76.113
- **Load Balancer:** (your ALB DNS)

## Author
Farzeena