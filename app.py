from flask import Flask, render_template, request, redirect, jsonify, session


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock database
users = {}  # {email: {username, password}}
bookings = []  # Store bookings here

# Serve HTML files (ensure they're in 'templates' folder)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            session['user'] = email
            return redirect('/')
        else:
            return "Invalid login", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        if email in users:
            return "Email already registered", 400
        users[email] = {'username': username, 'password': password}
        return redirect('/login')
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        if email in users:
            return "Reset link sent to your email (mock)", 200
        else:
            return "Email not found", 404
    return render_template('forgot_password.html')

@app.route('/booking_form.html')
def booking_form():
    return render_template('booking_form.html')

@app.route('/tickets_form.html')
def tickets_form():
    return render_template('tickets_form.html')


@app.route('/api/lock_seats', methods=['POST'])
def lock_seats():
    data = request.get_json()
    # No real locking logic for now
    return jsonify({'locked_seats': data['seats']}), 200

@app.route('/api/release_seats', methods=['POST'])
def release_seats():
    return jsonify({'status': 'released'}), 200

@app.route('/api/simulate_payment', methods=['POST'])
def simulate_payment():
    data = request.get_json()
    return jsonify({'status': 'success'}), 200

@app.route('/api/confirm_booking', methods=['POST'])
def confirm_booking():
    data = request.get_json()
    booking = {
        'movieId': data['movieId'],
        'location': data['location'],
        'showtime': data['showtime'],
        'theater': data['theater'],
        'selectedSeats': data['selectedSeats'],
        'totalCost': data['totalCost'],
        'ticket_code': f"TKT{len(bookings) + 1:04}"
    }
    bookings.append(booking)
    return jsonify({'status': 'confirmed', 'ticket_code': booking['ticket_code']}), 200

if __name__ == '__main__':
    app.run(debug=True)