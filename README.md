# Onction Dashboards

A FastAPI-based energy trading platform that provides dashboards for Distribution Companies (DisCos) and Generation Companies (GenCos) to manage energy trading orders, bids, and offers.

## 🚀 Features

- **Disco Dashboard**: Manage energy bids and trading operations for distribution companies
- **Genco Dashboard**: Handle energy offers and trading operations for generation companies
- **System Operator**: Centralized system management and monitoring
- **Market Data**: Real-time market data and analytics
- **User Management**: Authentication and user management with Clerk integration
- **Trade Matching**: Automated matching of buy/sell orders
- **RESTful API**: Complete REST API with FastAPI and automatic documentation

## 🏗️ Architecture

- **Backend**: FastAPI (Python 3.12+)
- **Database**: SQLite with SQLModel ORM
- **Authentication**: Clerk SDK integration
- **Process Management**: PM2 for production deployment
- **Containerization**: Docker support
- **CORS**: Cross-origin resource sharing enabled

## 📋 Prerequisites

- Python 3.12 or higher
- Node.js (for PM2 process management)
- Git

## 🛠️ Installation

### Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This script will:
- Check system prerequisites
- Create a virtual environment
- Install all dependencies
- Set up PM2 configuration
- Start the application

### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Onction-dashboards
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Install PM2 globally** (for production deployment)
   ```bash
   npm install -g pm2
   ```

## 🚀 Running the Application

### Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode with PM2

```bash
# Start with PM2
pm2 start ecosystem.config.js

# Monitor the application
pm2 monit

# View logs
pm2 logs onction-dashboard

# Stop the application
pm2 stop onction-dashboard
```

### Docker Deployment

```bash
# Build the Docker image
docker build -t onction-dashboard .

# Run the container
docker run -p 8000:8000 onction-dashboard
```

## 📚 API Documentation

Once the application is running, you can access:

- **Interactive API Documentation**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 🔗 API Endpoints

### Disco Dashboard (`/Disco-Dashboard`)
- `GET /get_bid` - Retrieve all bids for a trader
- `POST /create_bid` - Create new energy bids
- `PUT /update_bid/{id}` - Update existing bid
- `DELETE /delete_bid/{id}` - Delete a bid
- `GET /Trades/{Buyer_id}` - Get trades for a buyer

### Genco Dashboard (`/Genco-Dashboard`)
- `GET /get_offer` - Retrieve all offers for a trader
- `POST /create_offer` - Create new energy offers
- `PUT /update_offer/{id}` - Update existing offer
- `DELETE /delete_offer/{id}` - Delete an offer
- `GET /Trades/{Seller_id}` - Get trades for a seller

### System Operator (`/System-Operator`)
- System management and monitoring endpoints

### Market Data (`/Market-Data`)
- Real-time market data and analytics

### User Management (`/User`)
- User authentication and management

## 🗄️ Database Models

- **Order**: Energy trading orders (bids/offers)
- **Trades**: Completed energy trades
- **Status**: Order status (pending, matched, rejected, approved, denied)
- **OrderType**: Buy/Sell order types
- **CommonName**: Predefined company names (Gen A-D, Utility X-Z)

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=sqlite:///./database.db

# Clerk Authentication
CLERK_SECRET_KEY=your_clerk_secret_key
CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key

# Application
NODE_ENV=production
PYTHONPATH=/path/to/your/project
```

### PM2 Configuration

The `ecosystem.config.js` file contains PM2 configuration:
- Application name: `onction-dashboard`
- Memory limit: 1GB
- Auto-restart enabled
- Logging to `./logs/` directory

## 📁 Project Structure

```
Onction-dashboards/
├── app/
│   ├── db/                 # Database configuration
│   ├── modules/            # Business logic modules
│   ├── routes/             # API route handlers
│   ├── utils/              # Utility functions
│   ├── main.py             # FastAPI application entry point
│   ├── models.py           # Database models
│   └── server.py           # Server configuration
├── logs/                   # Application logs
├── venv/                   # Virtual environment
├── requirements.txt        # Python dependencies
├── ecosystem.config.js     # PM2 configuration
├── Dockerfile             # Docker configuration
├── setup.sh               # Automated setup script
└── README.md              # This file
```

## 🧪 Testing

```bash
# Run tests (if available)
python -m pytest

# Run with coverage
python -m pytest --cov=app
```

## 📝 Logging

Logs are stored in the `logs/` directory:
- `combined.log` - Combined application logs
- `err.log` - Error logs
- `out.log` - Output logs

## 🔒 Security

- Authentication handled by Clerk SDK
- CORS middleware configured
- Input validation with Pydantic models
- SQL injection protection with SQLModel

## 🚀 Deployment

### Production Checklist

1. Set up environment variables
2. Configure Clerk authentication
3. Set up proper database (consider PostgreSQL for production)
4. Configure reverse proxy (nginx)
5. Set up SSL certificates
6. Configure monitoring and alerting

### PM2 Commands

```bash
# Start application
pm2 start ecosystem.config.js

# Restart application
pm2 restart onction-dashboard

# Stop application
pm2 stop onction-dashboard

# Delete application
pm2 delete onction-dashboard

# Save PM2 configuration
pm2 save

# Setup PM2 startup script
pm2 startup
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the API documentation at `/docs`

## 🔄 Version History

- **v1.0.0** - Initial release with Disco and Genco dashboards
- Basic CRUD operations for orders and trades
- Clerk authentication integration
- PM2 deployment configuration
