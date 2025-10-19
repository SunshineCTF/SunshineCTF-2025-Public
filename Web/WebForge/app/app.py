from flask import Flask, request, render_template_string, render_template, abort, flash, redirect, url_for
import requests
import uuid

FLAG = open("flag.txt").read()

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

def create_app():
    return app

@app.route('/robots.txt')
def robots():
    return """
User-agent: *
Disallow: /admin
Disallow: /fetch

# internal SSRF testing tool requires special auth header to be set to 'true'
""", 200, {'Content-Type': 'text/plain'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['GET', 'POST'])
def fetch():
    if request.headers.get("allow", "") != "true":
        return "403 Forbidden: missing or incorrect SSRF access header", 403

    if request.method == 'GET':
        return render_template('fetch.html')

    url = request.form.get("url")

    if not url:
        return "No URL provided", 400

    try:
        # Check if the URL is trying to access /admin without template parameter
        parsed_url = requests.utils.urlparse(url)
        if parsed_url.path.endswith('/admin') and 'template' not in parsed_url.query:
            flash("You're trying to access /admin but forgot the ?template= parameter", 'error')
            return render_template('fetch.html', result={
                'error': 'Missing template parameter',
                'success': False
            })
            
        r = requests.get(url)
        return render_template('fetch.html', result={
            'text': r.text,
            'success': True,
            'status_code': r.status_code
        })
    except Exception as e:
        return render_template('fetch.html', result={
            'error': str(e),
            'success': False
        })

@app.route('/admin', methods=['GET'])
def admin():
    if request.remote_addr != "127.0.0.1":
        abort(403)
        
    if request.method != 'GET':
        abort(405)  # Method Not Allowed

    template_input = request.args.get("template", "")
    if not template_input:
        return "Missing information in the ?template= parameter in the URL", 400

    if '.' in template_input or '_' in template_input:
        return "Nope."
    
    try:
        return render_template_string(template_input)
    except Exception as e:
        return f"Template error: {e}"

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000)
