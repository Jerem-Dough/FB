"""
Database management for workflows and posting queue
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self, db_path="data/app.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Workflows table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                descriptions TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                condition TEXT NOT NULL,
                location TEXT,
                delivery_method TEXT DEFAULT 'Door pickup',
                groups TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Queue table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workflow_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                condition TEXT NOT NULL,
                location TEXT,
                images TEXT NOT NULL,
                delivery_method TEXT DEFAULT 'Door pickup',
                groups TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                posted_at TEXT,
                error_message TEXT,
                FOREIGN KEY (workflow_id) REFERENCES workflows (id)
            )
        """)

        # Migration: Add new columns to existing tables if they don't exist
        try:
            cursor.execute("SELECT delivery_method FROM workflows LIMIT 1")
        except sqlite3.OperationalError:
            # Column doesn't exist, add it
            cursor.execute("ALTER TABLE workflows ADD COLUMN delivery_method TEXT DEFAULT 'Door pickup'")
            cursor.execute("ALTER TABLE workflows ADD COLUMN groups TEXT DEFAULT NULL")
            # Update existing rows to have default value
            cursor.execute("UPDATE workflows SET delivery_method = 'Door pickup' WHERE delivery_method IS NULL")
            print("Added delivery_method and groups columns to workflows table")

        try:
            cursor.execute("SELECT delivery_method FROM queue LIMIT 1")
        except sqlite3.OperationalError:
            # Column doesn't exist, add it
            cursor.execute("ALTER TABLE queue ADD COLUMN delivery_method TEXT DEFAULT 'Door pickup'")
            cursor.execute("ALTER TABLE queue ADD COLUMN groups TEXT DEFAULT NULL")
            # Update existing rows to have default value
            cursor.execute("UPDATE queue SET delivery_method = 'Door pickup' WHERE delivery_method IS NULL")
            print("Added delivery_method and groups columns to queue table")

        # Add boost_listing column if it doesn't exist
        try:
            cursor.execute("SELECT boost_listing FROM workflows LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE workflows ADD COLUMN boost_listing INTEGER DEFAULT 0")
            print("Added boost_listing column to workflows table")

        try:
            cursor.execute("SELECT boost_listing FROM queue LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE queue ADD COLUMN boost_listing INTEGER DEFAULT 0")
            print("Added boost_listing column to queue table")

        # Fix any NULL status values
        cursor.execute("UPDATE queue SET status = 'pending' WHERE status IS NULL")

        conn.commit()
        conn.close()
    
    # Workflow operations
    def create_workflow(self, name, title, descriptions, price, category, condition, location="", delivery_method="Door pickup", groups=None, boost_listing=False):
        """Create a new workflow template"""
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.now().isoformat()

        groups_json = json.dumps(groups) if groups else None

        try:
            cursor.execute("""
                INSERT INTO workflows (name, title, descriptions, price, category, condition, location, delivery_method, groups, boost_listing, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, title, json.dumps(descriptions), price, category, condition, location, delivery_method, groups_json, 1 if boost_listing else 0, now, now))
            conn.commit()
            workflow_id = cursor.lastrowid
            return workflow_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_workflow(self, workflow_id):
        """Get workflow by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get column info
        cursor.execute("PRAGMA table_info(workflows)")
        columns = {col[1]: col[0] for col in cursor.fetchall()}

        cursor.execute("SELECT * FROM workflows WHERE id = ?", (workflow_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            # Get indices safely
            delivery_idx = columns.get('delivery_method')
            groups_idx = columns.get('groups')
            created_idx = columns.get('created_at')
            updated_idx = columns.get('updated_at')

            # Safely parse groups
            groups = None
            try:
                if groups_idx is not None and len(row) > groups_idx and row[groups_idx]:
                    groups = json.loads(row[groups_idx])
            except (json.JSONDecodeError, TypeError):
                groups = None

            # Get boost_listing
            boost_idx = columns.get('boost_listing')
            boost_listing = bool(row[boost_idx]) if boost_idx is not None and len(row) > boost_idx and row[boost_idx] is not None else False

            return {
                'id': row[0],
                'name': row[1],
                'title': row[2],
                'descriptions': json.loads(row[3]),
                'price': row[4],
                'category': row[5],
                'condition': row[6],
                'location': row[7],
                'delivery_method': (row[delivery_idx] if delivery_idx is not None and len(row) > delivery_idx and row[delivery_idx] else 'Door pickup'),
                'groups': groups,
                'boost_listing': boost_listing,
                'created_at': (row[created_idx] if created_idx is not None and len(row) > created_idx else None),
                'updated_at': (row[updated_idx] if updated_idx is not None and len(row) > updated_idx else None)
            }
        return None
    
    def get_all_workflows(self):
        """Get all workflows"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get column info
        cursor.execute("PRAGMA table_info(workflows)")
        columns = {col[1]: col[0] for col in cursor.fetchall()}

        cursor.execute("SELECT * FROM workflows ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        conn.close()

        # Get indices safely
        delivery_idx = columns.get('delivery_method')
        groups_idx = columns.get('groups')
        created_idx = columns.get('created_at')
        updated_idx = columns.get('updated_at')

        # Get boost_listing index
        boost_idx = columns.get('boost_listing')

        workflows = []
        for row in rows:
            # Safely parse groups
            groups = None
            try:
                if groups_idx is not None and len(row) > groups_idx and row[groups_idx]:
                    groups = json.loads(row[groups_idx])
            except (json.JSONDecodeError, TypeError):
                groups = None

            # Get boost_listing
            boost_listing = bool(row[boost_idx]) if boost_idx is not None and len(row) > boost_idx and row[boost_idx] is not None else False

            workflows.append({
                'id': row[0],
                'name': row[1],
                'title': row[2],
                'descriptions': json.loads(row[3]),
                'price': row[4],
                'category': row[5],
                'condition': row[6],
                'location': row[7],
                'delivery_method': (row[delivery_idx] if delivery_idx is not None and len(row) > delivery_idx and row[delivery_idx] else 'Door pickup'),
                'groups': groups,
                'boost_listing': boost_listing,
                'created_at': (row[created_idx] if created_idx is not None and len(row) > created_idx else None),
                'updated_at': (row[updated_idx] if updated_idx is not None and len(row) > updated_idx else None)
            })
        return workflows
    
    def update_workflow(self, workflow_id, name, title, descriptions, price, category, condition, location="", delivery_method="Door pickup", groups=None, boost_listing=False):
        """Update an existing workflow"""
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.now().isoformat()

        groups_json = json.dumps(groups) if groups else None

        cursor.execute("""
            UPDATE workflows
            SET name=?, title=?, descriptions=?, price=?, category=?, condition=?, location=?, delivery_method=?, groups=?, boost_listing=?, updated_at=?
            WHERE id=?
        """, (name, title, json.dumps(descriptions), price, category, condition, location, delivery_method, groups_json, 1 if boost_listing else 0, now, workflow_id))
        conn.commit()
        conn.close()
    
    def delete_workflow(self, workflow_id):
        """Delete a workflow"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM workflows WHERE id = ?", (workflow_id,))
        conn.commit()
        conn.close()
    
    # Queue operations
    def add_to_queue(self, workflow_id, title, description, price, category, condition, location, images, delivery_method="Door pickup", groups=None, boost_listing=False):
        """Add a listing to the posting queue"""
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.now().isoformat()

        groups_json = json.dumps(groups) if groups else None

        cursor.execute("""
            INSERT INTO queue (workflow_id, title, description, price, category, condition, location, images, delivery_method, groups, boost_listing, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (workflow_id, title, description, price, category, condition, location, json.dumps(images), delivery_method, groups_json, 1 if boost_listing else 0, now))
        conn.commit()
        queue_id = cursor.lastrowid
        conn.close()
        return queue_id
    
    def get_queue_items(self, status=None):
        """Get queue items, optionally filtered by status"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get column names to properly map indices
        if status:
            cursor.execute("SELECT * FROM queue WHERE status = ? ORDER BY created_at ASC", (status,))
        else:
            cursor.execute("SELECT * FROM queue ORDER BY created_at ASC")

        rows = cursor.fetchall()

        # Get column info
        cursor.execute("PRAGMA table_info(queue)")
        columns = {col[1]: col[0] for col in cursor.fetchall()}

        conn.close()

        items = []
        for row in rows:
            # Get indices safely
            delivery_idx = columns.get('delivery_method')
            groups_idx = columns.get('groups')
            boost_idx = columns.get('boost_listing')
            status_idx = columns.get('status')
            created_idx = columns.get('created_at')
            posted_idx = columns.get('posted_at')
            error_idx = columns.get('error_message')

            # Safely parse groups
            groups = None
            try:
                if groups_idx is not None and len(row) > groups_idx and row[groups_idx]:
                    groups = json.loads(row[groups_idx])
            except (json.JSONDecodeError, TypeError):
                groups = None

            # Get boost_listing
            boost_listing = bool(row[boost_idx]) if boost_idx is not None and len(row) > boost_idx and row[boost_idx] is not None else False

            items.append({
                'id': row[0],
                'workflow_id': row[1],
                'title': row[2],
                'description': row[3],
                'price': row[4],
                'category': row[5],
                'condition': row[6],
                'location': row[7],
                'images': json.loads(row[8]),
                'delivery_method': (row[delivery_idx] if delivery_idx is not None and len(row) > delivery_idx and row[delivery_idx] else 'Door pickup'),
                'groups': groups,
                'boost_listing': boost_listing,
                'status': (row[status_idx] if status_idx is not None and len(row) > status_idx and row[status_idx] else 'pending'),
                'created_at': (row[created_idx] if created_idx is not None and len(row) > created_idx else None),
                'posted_at': (row[posted_idx] if posted_idx is not None and len(row) > posted_idx else None),
                'error_message': (row[error_idx] if error_idx is not None and len(row) > error_idx else None)
            })
        return items
    
    def update_queue_status(self, queue_id, status, error_message=None):
        """Update queue item status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status == 'posted':
            posted_at = datetime.now().isoformat()
            cursor.execute("""
                UPDATE queue SET status=?, posted_at=?, error_message=? WHERE id=?
            """, (status, posted_at, error_message, queue_id))
        else:
            cursor.execute("""
                UPDATE queue SET status=?, error_message=? WHERE id=?
            """, (status, error_message, queue_id))
        
        conn.commit()
        conn.close()
    
    def delete_queue_item(self, queue_id):
        """Delete a queue item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM queue WHERE id = ?", (queue_id,))
        conn.commit()
        conn.close()
    
    def clear_completed_queue(self):
        """Clear all completed/failed items from queue"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM queue WHERE status IN ('posted', 'failed')")
        conn.commit()
        conn.close()
