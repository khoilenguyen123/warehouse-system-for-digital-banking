-- 1. Lớp chứa dữ liệu thô đẩy từ Python vào
CREATE SCHEMA staging; 

-- 2. Lớp kho dữ liệu trung tâm (Data Warehouse)
CREATE SCHEMA dw; 

-- 3. Lớp dữ liệu phục vụ báo cáo rủi ro và kinh doanh (Data Mart)
CREATE SCHEMA mart; 

-- 4. Lớp kiểm soát chất lượng dữ liệu (Data Quality/Audit)
CREATE SCHEMA audit; 

-- Kiểm tra xem đã có đủ 4 schema chưa
SELECT schema_name FROM information_schema.schemata;
