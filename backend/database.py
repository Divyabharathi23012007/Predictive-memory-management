import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "sql.freedb.tech"),
    "user": os.getenv("DB_USER", "freedb_memos"),
    "password": os.getenv("DB_PASSWORD", "Nw2E3kDkv#6hb5U"),
    "database": os.getenv("DB_NAME", "freedb_memory_management"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

def get_connection():
    """Establish MySQL database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def initialize_database():
    """Create tables if they don't exist"""
    try:
        # Connect directly with the existing database (freedb doesn't allow CREATE DATABASE)
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Create memory_samples table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_samples (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                current_used_mb FLOAT NOT NULL,
                available_mb FLOAT NOT NULL,
                memory_usage_percent FLOAT NOT NULL,
                predicted_memory_mb FLOAT NOT NULL,
                os_decision VARCHAR(50) NOT NULL,
                INDEX idx_timestamp (timestamp)
            )
        """)

        # Create memory_alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_alerts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                alert_type VARCHAR(50) NOT NULL,
                message TEXT NOT NULL,
                memory_mb FLOAT,
                severity VARCHAR(20) NOT NULL,
                INDEX idx_timestamp (timestamp)
            )
        """)

        # Create model_metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                model_name VARCHAR(100),
                accuracy FLOAT,
                mse FLOAT,
                rmse FLOAT,
                training_samples INT,
                INDEX idx_timestamp (timestamp)
            )
        """)

        # Create process_snapshots table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS process_snapshots (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sample_id INT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                pid INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                memory_mb FLOAT NOT NULL,
                memory_percent FLOAT NOT NULL,
                rank_position TINYINT NOT NULL,
                INDEX idx_timestamp (timestamp),
                INDEX idx_sample_id (sample_id)
            )
        """)

        # Create trigger to auto-alert on high memory
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS auto_alert_high_memory
            AFTER INSERT ON memory_samples
            FOR EACH ROW
            BEGIN
              IF NEW.memory_usage_percent > 85 THEN
                INSERT INTO memory_alerts (alert_type, message, memory_mb, severity)
                VALUES (
                  'HIGH_MEMORY',
                  CONCAT('Memory at ', NEW.memory_usage_percent, '% — ', NEW.os_decision),
                  NEW.current_used_mb,
                  'CRITICAL'
                );
              END IF;
            END;
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
        return True

    except Error as e:
        print(f"Error initializing database: {e}")
        return False

def save_memory_sample(current_used, available, percent, predicted, decision):
    """Save memory reading to database, returns the new row id"""
    try:
        conn = get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        query = """
            INSERT INTO memory_samples 
            (current_used_mb, available_mb, memory_usage_percent, predicted_memory_mb, os_decision)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (current_used, available, percent, predicted, decision))
        conn.commit()
        sample_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return sample_id
    except Error as e:
        print(f"Error saving memory sample: {e}")
        return None

def save_process_snapshot(sample_id, processes):
    """Save top memory-consuming processes linked to a memory sample."""
    if not processes:
        return False
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        query = """
            INSERT INTO process_snapshots
            (sample_id, pid, name, memory_mb, memory_percent, rank_position)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        rows = [
            (sample_id, p["pid"], p["name"], p["memory_mb"], p["memory_percent"], p["rank"])
            for p in processes
        ]
        cursor.executemany(query, rows)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error saving process snapshot: {e}")
        return False

def get_top_processes(limit=5):
    """Retrieve the most recent process snapshot."""
    try:
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT ps.*
            FROM process_snapshots ps
            WHERE ps.sample_id = (
                SELECT MAX(sample_id) FROM process_snapshots
            )
            ORDER BY ps.rank_position ASC
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Error as e:
        print(f"Error retrieving top processes: {e}")
        return []

def get_memory_history(limit=100):
    """Retrieve memory history from database"""
    try:
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        query = f"""
            SELECT * FROM memory_samples 
            ORDER BY timestamp DESC 
            LIMIT {limit}
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Error as e:
        print(f"Error retrieving memory history: {e}")
        return []

def get_memory_stats(hours=1):
    """Get memory statistics for the last N hours"""
    try:
        conn = get_connection()
        if not conn:
            return {}
        cursor = conn.cursor(dictionary=True)
        query = f"""
            SELECT 
                AVG(current_used_mb) as avg_used,
                MAX(current_used_mb) as max_used,
                MIN(current_used_mb) as min_used,
                AVG(memory_usage_percent) as avg_percent,
                MAX(memory_usage_percent) as max_percent,
                COUNT(*) as sample_count
            FROM memory_samples
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL {hours} HOUR)
        """
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result if result else {}
    except Error as e:
        print(f"Error getting memory stats: {e}")
        return {}

def save_alert(alert_type, message, memory_mb=None, severity="INFO"):
    """Save alert to database"""
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        query = """
            INSERT INTO memory_alerts 
            (alert_type, message, memory_mb, severity)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (alert_type, message, memory_mb, severity))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error saving alert: {e}")
        return False

def save_model_metrics(model_name, accuracy, mse, rmse, training_samples):
    """Save ML model metrics"""
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        query = """
            INSERT INTO model_metrics 
            (model_name, accuracy, mse, rmse, training_samples)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (model_name, accuracy, mse, rmse, training_samples))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error saving model metrics: {e}")
        return False

def get_training_data(limit=500):
    """Get historical data for ML training"""
    try:
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        query = f"""
            SELECT 
                current_used_mb,
                available_mb,
                memory_usage_percent,
                predicted_memory_mb
            FROM memory_samples 
            ORDER BY timestamp DESC 
            LIMIT {limit}
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Error as e:
        print(f"Error getting training data: {e}")
        return []
