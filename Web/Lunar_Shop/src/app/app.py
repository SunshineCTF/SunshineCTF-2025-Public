import signal
import time
import sqlite3

from flask import*
from contextlib import contextmanager



@contextmanager
def query_timeout(seconds):
    def timeout_handler(signum, frame):
        raise TimeoutError("Query timeout")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)



app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def products():
    # we could pull dynamically the productIDs, but I'm too lazy
    return render_template("products.html")

@app.route('/product', methods=['GET'])
def display_product():
    empty_row = ("", "", "", "")
    # totally a better way to prevent people from DOS-ing this
    blacklists = [
        'blob',
        'recursive',
        '>', '<',
        'sum',
        'length',
        'hex',
        'count',
        'random',
        'min(',
        'max(',
        'case',
        'when',
        'distinct',
        'replace',
        'abs(',
        'coalesce'
    ]
    try:
        # we don't want people to cheese this, learn people LEARN ! 
        print(str(request.headers).lower())
        if 'sqlmap' in str(request.headers).lower():
            return ""
        
        
        product_id = request.args.get('product_id', '1').strip()
        
        # don't want ppl DOS-ing this or cheesing it with SQLMAP
        malicious_query = product_id.lower()
        if len(malicious_query) >= 150:
            return render_template("product.html", err_msg=f"[ Blocked by WAF for being too large. ]", product=empty_row)
        
        for keyword in blacklists:
            if keyword in malicious_query.lower() or keyword in malicious_query.replace(' ', ''):
                return render_template("product.html", err_msg=f"[ Blocked by WAF. ]", product=empty_row)

        # create a connection
        conn = sqlite3.connect("database.db")

        # cursor that allows us to send those crappy raw SQL queries
        cursor = conn.cursor()

        # no writing stuff allowed just in case (even though stacked queries are disabled.) 
        conn.execute("PRAGMA query_only = ON;")
        conn.execute("PRAGMA foreign_keys = ON;")


        cursor.execute(f"SELECT * FROM products WHERE id={product_id};")
        row = cursor.fetchone()
        if row:
            return render_template("product.html", product=row)
        else:
            # just return an error
            return render_template("product.html", err_msg="[ No product with that ID found ! ]", product=empty_row)
    except Exception as err:
        err = f"Error occured. --> {err}"
        return render_template("product.html", err_msg=f"[ {err} ]", product=empty_row)

def create_app():
    return app

if __name__ == "__main__":
    # gonna keep this on so they get descriptive error messages
    app.run(host='0.0.0.0', port=8000, debug=False)
