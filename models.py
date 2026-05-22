from db import get_conn, init_db
from datetime import datetime


def ensure_db():
    init_db()


def add_child(name: str, age: int = None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO children (name, age) VALUES (?, ?)', (name, age))
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return cid


def list_children():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, age, balance FROM children ORDER BY name')
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_task(child_id: int, title: str, description: str = '', amount: float = 0.0, due_date: str = None, recurring: int = 0):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO tasks (child_id, title, description, amount, due_date, recurring) VALUES (?, ?, ?, ?, ?, ?)',
        (child_id, title, description, amount, due_date, recurring)
    )
    conn.commit()
    tid = cur.lastrowid
    conn.close()
    return tid


def list_tasks(child_id: int = None, include_done: bool = False):
    conn = get_conn()
    cur = conn.cursor()
    q = 'SELECT * FROM tasks'
    params = []
    where = []
    if child_id is not None:
        where.append('child_id = ?')
        params.append(child_id)
    if not include_done:
        where.append('done = 0')
    if where:
        q += ' WHERE ' + ' AND '.join(where)
    q += ' ORDER BY due_date IS NULL, due_date'
    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_task_done(task_id: int, confirmed_by_parent: bool = True):
    # mark task done and create transaction; adjust child's balance
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cur.fetchone()
    if not task:
        conn.close()
        raise ValueError('Task not found')

    if task['done']:
        conn.close()
        return False

    amount = float(task['amount'] or 0)
    child_id = task['child_id']
    ts = datetime.utcnow().isoformat()

    # update task
    cur.execute('UPDATE tasks SET done = 1 WHERE id = ?', (task_id,))

    # add transaction if parent confirmed
    if confirmed_by_parent and amount != 0:
        cur.execute('INSERT INTO transactions (child_id, task_id, amount, timestamp, note) VALUES (?, ?, ?, ?, ?)',
                    (child_id, task_id, amount, ts, f'Payout for task {task_id}'))
        # update child's balance
        cur.execute('UPDATE children SET balance = balance + ? WHERE id = ?', (amount, child_id))

    conn.commit()
    conn.close()
    return True


def list_transactions(child_id: int = None):
    conn = get_conn()
    cur = conn.cursor()
    q = 'SELECT * FROM transactions'
    params = []
    if child_id is not None:
        q += ' WHERE child_id = ?'
        params.append(child_id)
    q += ' ORDER BY timestamp DESC'
    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


if __name__ == '__main__':
    ensure_db()
