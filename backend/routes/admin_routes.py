from flask import Blueprint, jsonify, request, Response
from utils.db import get_db_connection
import psycopg2
import psycopg2.extras
import io
import csv

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/users', methods=['GET'])
def list_users():
    """
    Return list of users with created_at and last_login.
    Supports filters, pagination, and CSV export.
    Query params:
      - role: 'patient' (default), 'admin', or 'all'
      - search: substring for username (case-insensitive)
      - page: 1-based page number (default 1)
      - page_size: items per page (default 20, max 100)
      - export: 'csv' to download CSV (ignores pagination)
    """
    role = request.args.get('role', 'patient').lower()
    search = request.args.get('search', '').strip()
    export = request.args.get('export') == 'csv'

    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
    except ValueError:
        page, page_size = 1, 20
    page = max(page, 1)
    page_size = max(1, min(page_size, 100))

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Ensure last_login column exists; if not, try to add it once.
        try:
            cursor.execute("SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='last_login'")
            has_col = cursor.fetchone()
            if not has_col:
                cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMPTZ NULL")
                conn.commit()
        except Exception:
            conn.rollback()

        # Build WHERE clause
        where_clauses = []
        params = []
        if role in ('patient', 'admin'):
            where_clauses.append("user_type = %s")
            params.append(role)
        # role == 'all' means no filter on user_type
        if search:
            where_clauses.append("username ILIKE %s")
            params.append(f"%{search}%")
        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        # Count total
        count_sql = f"SELECT COUNT(*) FROM users {where_sql}"
        cursor.execute(count_sql, tuple(params))
        total = int(cursor.fetchone()['count'])

        # If CSV export, fetch all filtered rows
        if export:
            data_sql = f"""
                SELECT username, user_type, created_at, last_login
                FROM users
                {where_sql}
                ORDER BY created_at DESC
            """
            cursor.execute(data_sql, tuple(params))
            rows = cursor.fetchall()

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['username', 'user_type', 'created_at', 'last_login'])
            for r in rows:
                writer.writerow([
                    r.get('username'),
                    r.get('user_type'),
                    r.get('created_at'),
                    r.get('last_login')
                ])
            csv_data = output.getvalue()
            output.close()
            return Response(
                csv_data,
                mimetype='text/csv',
                headers={'Content-Disposition': 'attachment; filename=users.csv'}
            )

        # Paginated data
        offset = (page - 1) * page_size
        data_sql = f"""
            SELECT username, user_type, created_at, last_login
            FROM users
            {where_sql}
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(data_sql, tuple(params + [page_size, offset]))
        users = cursor.fetchall()

        return jsonify({
            'users': users,
            'total': total,
            'page': page,
            'page_size': page_size
        }), 200

    except psycopg2.Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()