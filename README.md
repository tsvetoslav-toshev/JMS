# 💎 Jewelry Management System

A comprehensive desktop application for managing jewelry inventory, sales, and multiple shops with advanced search capabilities and professional reporting.

## 🚀 Features

### ✨ Core Functionality
- **Advanced Inventory Management** with barcode support and image handling
- **Professional Sales Tracking** with multi-shop support
- **Enhanced Search System** with tabbed interface for precise filtering
- **Comprehensive Reporting** with analytics and export capabilities
- **Multi-Shop Operations** with seamless item transfers
- **Barcode Scanning** from camera or uploaded images
- **Professional Label Printing** optimized for thermal printers
- **Data Integrity** with backup/restore and undo/redo system

### 🔍 Advanced Search Capabilities
- **Tabbed Search Interface** for inventory (4 tabs) and sales (2 tabs)
- **Smart Filtering** across all 11 data columns
- **Date Range Pickers** for time-based searches
- **Price & Weight Filters** with range selection
- **Category-Based Search** with dynamic filtering
- **Real-time Search** with instant results

### 📊 Professional Reporting
- **Dashboard Analytics** with real-time statistics
- **Excel Export** for detailed reports
- **ROI Analysis** and profit tracking
- **Sales Trends** and performance metrics
- **Low Stock Alerts** and inventory warnings

## 🛠️ Requirements

- **Python 3.8+** (Recommended: Python 3.11+)
- **Webcam** (for barcode scanning)
- **Thermal Printer** (optional, for label printing - Citizen CLP 631 recommended)
- **Windows OS** (optimized for Windows 10/11)

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/jewelry-management-system.git
cd jewelry-management-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
python main.py
```

## 📋 User Guide

### 🏪 Main Interface

The application features **7 main tabs**:

1. **📦 Add Item** - Create new inventory items
2. **📋 Inventory** - Browse and manage stock with advanced search
3. **🏪 Shop Loading** - Transfer items between warehouse and shops
4. **💰 Sales** - Process sales with barcode scanning
5. **📊 Reports** - Analytics and reporting dashboard
6. **🗄️ Database** - Data management and backups
7. **📘 Help** - Complete user guide and shortcuts

### 🔍 Enhanced Search System

#### Inventory Search (4 Tabs):
- **General Search**: Search across all fields simultaneously
- **Price & Weight**: Filter by price ranges and weight specifications
- **Date Range**: Search by creation/modification dates
- **Category Filter**: Browse by categories, metals, and stones

#### Sales Search (2 Tabs):
- **General Search**: Search sales records by item details
- **Date Filter**: Filter sales by date ranges with quick presets

### 📦 Item Management

#### Adding Items:
1. Select category, metal, and stone from dropdowns
2. Enter prices (automatically converts EUR to BGN)
3. Specify weight and quantity
4. Upload product image (optional)
5. Generate barcode label
6. Print professional label for thermal printer

#### Inventory Operations:
- **Bulk Selection**: Ctrl+Click for multiple items
- **Mass Operations**: Edit prices, move to shops, delete
- **Smart Filtering**: Combine multiple filters for precise results
- **Visual Indicators**: Low stock items highlighted in red

### 🏪 Shop Management

#### Transferring Items:
1. Select target shop from dropdown
2. Scan barcode or enter manually
3. Specify quantity to transfer
4. System validates stock availability
5. Automatic inventory updates

#### Shop Operations:
- View items in each shop
- Return items to warehouse
- Process direct sales from shops
- Track shop-specific performance

### 💰 Sales Processing

#### Single Sale:
1. Select shop for sale
2. Scan item barcode
3. Sale processes automatically
4. Receipt generation (optional)

#### Sales Analytics:
- Filter by date ranges (today, week, month, year, custom)
- Shop-specific sales tracking
- Profit margin analysis
- Best-selling items reports

### 📊 Reports & Analytics

#### Dashboard Metrics:
- Today's sales and monthly totals
- Warehouse value calculation
- Low stock alerts
- Average profit margins

#### Detailed Reports:
- **Sales Report**: Comprehensive sales data with Excel export
- **Inventory Report**: Stock levels and valuation
- **Profit Analysis**: Margin tracking by category
- **Performance Metrics**: ROI and trend analysis

### 🗄️ Data Management

#### Backup & Restore:
- Automatic daily backups
- Manual backup creation
- Full database restore capability
- Data integrity validation

#### Import/Export:
- Excel export for all reports
- Bulk data import capabilities
- Image backup and restore
- Database migration tools

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Tab` | Next tab |
| `Ctrl + Shift + Tab` | Previous tab |
| `Ctrl + 1-7` | Direct tab access |
| `Delete` | Delete selected items |
| `Ctrl + A` | Select all |
| `Ctrl + Click` | Multi-select |
| `Double Click` | Edit item |
| `Enter` | Confirm action |
| `Escape` | Cancel/Close |

## 🗂️ Directory Structure

```
jewelry-management-system/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── jewelry.ico            # Application icon
├── jewelry.spec           # PyInstaller configuration
├── 
├── database/
│   └── models.py          # Database models and operations
├── 
├── utils/
│   ├── barcode_scanner.py # Barcode scanning functionality
│   ├── barcode.py         # Barcode generation utilities
│   ├── data_manager.py    # Data import/export operations
│   ├── database.py        # Database connection management
│   └── report_generator.py # Report generation utilities
├── 
├── data/
│   └── jewelry.db         # Main SQLite database
├── 
├── resources/
│   ├── images/            # Product images storage
│   └── barcodes/          # Generated barcode images
├── 
├── backups/               # Database backups
├── exports/               # Exported reports
├── reports/               # Generated report files
├── logs/                  # Application logs
├── fonts/                 # Custom fonts for labels
└── dlls/                  # Required DLL files
```

## 🔧 Technical Details

### Database Schema:
- **items**: Main inventory table with 11 columns
- **sales**: Sales transactions with timestamps
- **shops**: Shop management and item locations
- **categories/metals/stones**: Master data tables

### Technologies Used:
- **PyQt6**: Modern GUI framework
- **SQLite**: Embedded database
- **OpenCV**: Image processing and barcode scanning
- **Pillow**: Image manipulation
- **pandas**: Data analysis and Excel export
- **pyzbar**: Barcode decoding
- **reportlab**: PDF generation

### Performance Optimizations:
- **Lazy Loading**: Large datasets loaded on demand
- **Indexed Searches**: Database indexes for fast queries
- **Memory Management**: Efficient image handling
- **Async Operations**: Non-blocking UI updates

## 🚀 Advanced Features

### Professional Label Printing:
- Optimized for thermal printers (58mm width)
- Includes barcode, item details, and pricing
- Automatic label queue management
- Print preview functionality

### Data Integrity:
- Foreign key constraints
- Transaction rollback support
- Automatic data validation
- Concurrent access protection

### Security Features:
- Database encryption support
- Audit trail logging
- User access controls
- Secure backup encryption

## 🔄 Updates & Changelog

### Latest Version Features:
- ✅ **Enhanced Tabbed Search**: 4-tab inventory search, 2-tab sales search
- ✅ **Advanced Filtering**: Price ranges, date pickers, category filters
- ✅ **Smart Data Flow**: Warehouse ↔ Shop transfers with validation
- ✅ **Comprehensive Analytics**: Real-time dashboards and trend analysis
- ✅ **Professional Reporting**: Excel exports with detailed metrics
- ✅ **UI/UX Improvements**: Modern interface with intuitive navigation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For technical support or feature requests:
- Create an issue on GitHub
- Email: support@jewelry-management.com
- Documentation: [Wiki](https://github.com/yourusername/jewelry-management-system/wiki)

## 🎯 Roadmap

### Upcoming Features:
- [ ] **Multi-language Support**: English, German, French
- [ ] **Cloud Synchronization**: Multi-location data sync
- [ ] **Mobile Companion App**: iOS/Android barcode scanning
- [ ] **Advanced Analytics**: AI-powered insights and predictions
- [ ] **POS Integration**: Credit card and payment processing
- [ ] **Customer Management**: Client database and loyalty programs

---

**💎 Jewelry Management System** - Professional inventory and sales management solution for jewelry businesses.
