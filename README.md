
# Inventory Tracking System - API Service

## Overview
This is a FastAPI-based backend service for tracking product inventory and stock movements. It is designed to scale from a single kiryana store to a multi-store, multi-supplier platform with audit capabilities, real-time tracking, and performance optimizations.

## Key Features
- Real-time inventory tracking  
- Multi-store support  
- Audit logging for all critical operations  
- Horizontal scalability  
- Caching for improved performance  
- Basic authentication & rate limiting  

## Design Decisions

### Database Schema
- **Products**: Core product information (e.g., name, price)  
- **Stores**: Store-specific information  
- **StockMovements**: Logs all inventory changes (stock-in, sales, manual removals)  
- **StoreInventory**: Tracks current inventory per store-product combination  
- **AuditLogs**: Records critical actions for traceability  

### Scalability Approach
#### Stage 1 – MVP (Single Store)
- Uses SQLite for local development  
- CLI or simple API interface  

#### Stage 2 – Scaling to 500+ Stores
- Transitioned to PostgreSQL for relational data handling  
- Introduced REST APIs and reporting features  
- Basic authentication and request throttling implemented  

#### Stage 3 – Enterprise Scale
- Horizontal scaling with Docker  
- Redis for caching frequent reads  
- Read/write DB separation for performance  
- Event-driven architecture for async updates  

### Caching Strategy
- Redis used for caching frequent inventory queries  
- 60-second TTL to balance freshness with performance  
- Cache invalidated automatically on write operations  

### Security
- Basic authentication for all write operations  
- Rate limiting: 10 requests/minute on selected endpoints  
- **Note**: For production use, OAuth2/JWT is recommended for enhanced security.  

## API Endpoints

### Products
- `POST /products/` – Create a new product  
- `GET /products/` – List all products (paginated)  

### Stores
- `POST /stores/` – Create a new store  
- `GET /stores/` – List all stores  

### Stock Movements
- `POST /stock-movements/` – Record a stock movement  
- `GET /stock-movements/` – Filter by store, product, or date range  

### Inventory
- `GET /inventory/{store_id}` – Current inventory for a specific store  
- `GET /products/{product_id}/inventory` – Inventory for a product across all stores  

## Evolution Rationale

### Stage 1 → Stage 2
- Replaced SQLite with PostgreSQL  
- Introduced basic auth & request throttling  
- Implemented filtering/reporting capabilities  
- Added audit logging for sensitive operations  

### Stage 2 → Stage 3
- Integrated Redis for caching  
- Deployed using Docker with multiple replicas  
- Separated reads/writes for database optimization  
- Enhanced API performance and security features  

## Assumptions
- Initial deployment targets a single store setup  
- Product pricing is consistent across all stores  
- Stock movements are atomic (no partial updates)  
- Audit logs are write-heavy, rarely read  
- Inventory queries are frequent and tolerate minor staleness (~60s)  

## Trade-offs
- **Consistency vs Performance**: Chose eventual consistency with caching for better performance  
- **Security**: Basic auth is simple but less secure than OAuth/JWT  
- **Scalability**: Horizontal scaling adds complexity but enables growth  
- **Normalization vs Denormalization**: Chose normalized schema for integrity over query performance for data integrity and easier updates.  

## Technologies Used
- **FastAPI** – API framework  
- **PostgreSQL** – Relational database  
- **Redis** – In-memory caching  
- **Docker** – Containerization  
- **SQLite** – Local storage for MVP  
