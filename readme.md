# Build a e-commerce site for selling ice creams

## Customer requirements
- Products list page (Done)
- Products detail page (Done)
- Cart management (add to cart, update quantity and remove from cart)
- Buy option with payment gateway like stripe / razorpay
- Delivery address management 
- Customer registration (Done)
- Customer login (Done)
- Order history and its status
- Customer can make enquiries with regards to products (Done)

## Admin requirements
- Option to create/update/delete ice cream products with details (pricing , etc)
- View Customers
- View customer orders
- Update order status
- View customer cart details

## User Roles
- Admin (can create/update/delete products, manage customers, orders, etc)
- Customer (can register, login, view products, add to cart, checkout, view order status, etc)

## Database
- Products (Done)
- Users (Done)
- Profiles (Done)
- Adresses (Done)
- Orders (Done)
- OrderItems (Done)
- Transactions (Done)
- Carts (Done)
- Enquiry (Done)

### Products
- id (primary key)
- userId (foreign key to Users table)
- slug (string, unique)
- name (string, unique)
- description (string)
- price (float)
- image_url (file)
- Brand (string)
- Category (string)

### Carts
- id (primary key)
- userId (foreign key to Users table)
- productId (foreign key to Products table)
- quantity (integer)
- price (float)
- createdAt
- updatedAt

### Orders
- id
- userId (foreign key to Users table)
- currency (INR)
- receipt (unique string)
- payment_status (default 'pending')
- amount_paid (float)
- amount_due (float)
- total (float)
- status (string)
- createdAt
- updatedAt

### OrderItems
- id (primary key)
- userId (foreign key to Users table)
- orderId (foreign key to Orders table)
- productId (foreign key to Products table)
- price
- quantity

### Transactions
- id
- orderId (foreign key to Orders table)
- amount (float)
- status (string)
- paymentMethod (string)
- paymentId (string)
- createdAt
- updatedAt

### Users
- id
- status
- paymentMethod
- paymentId
- createdAt
- updatedAt

### Profiles
- phone_number
- date_of_birth

### Address
- userId (foreign key to Users table)
- building_no
- street_address_1
- Street_address_2
- area
- City
- PIN

### Enquiry
- id
- userId (foreign key to Users table)
- productId (foreign key to Products table)
- first_name
- last_name
- email
- phone
- message (string)
- createdAt
- updatedAt

## Relationships
- One-to-many between Users and Orders (one user can have multiple orders)
- One-to-many between Users and Carts (one user can have multiple carts)
- One-to-many between Orders and OrderItems (one order can have multiple order items)
- Many-to-many between Products and Carts (one product can be in multiple carts)
- Many-to-many between Products and Orders (one product can be in multiple orders)
- One-to-one between Transactions and Orders (one transaction can be for one orders)
- One-to-many between Users and Enquiry (one user can have multiple enquiries)
- Many-to-many between Products and Enquiry (one product can have multiple enquiries)
- One-to-One between Users and Profile (One user can have one profile)
- One-to-many between Users and Addresses (One User can have multiple address)