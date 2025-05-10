from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from database import create_connection
from config import Config
from inference_sdk import InferenceHTTPClient

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Roboflow Inference Client for Alzheimer's (keeping original variable names)
ROBOFLOW_CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="79dhzfFvs8UNcpV3EWLU"
)
ROBOFLOW_MODEL_ID = "alzheimer-s-disease-detection-ud5st/1"

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def predict_condition(image_path):
    """Predict using Roboflow API (keeping original function name)"""
    try:
        result = ROBOFLOW_CLIENT.infer(image_path, model_id=ROBOFLOW_MODEL_ID)
        
        if not isinstance(result, dict):
            raise ValueError("Invalid API response format")
        
        # Handle Roboflow classification response
        if "predictions" in result and len(result["predictions"]) > 0:
            prediction = result["predictions"][0]
            return {
                'condition': prediction["class"],
                'confidence': float(prediction["confidence"]),
                'all_predictions': {p["class"]: float(p["confidence"]) for p in result["predictions"]}
            }
        elif "top" in result:
            return {
                'condition': result["top"],
                'confidence': float(result.get("confidence", 0)),
                'all_predictions': {result["top"]: float(result.get("confidence", 0))}
            }
        else:
            raise ValueError("No valid prediction in API response")
            
    except Exception as e:
        raise ValueError(f"API prediction failed: {str(e)}")

# Authentication routes (unchanged)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                
                if user and check_password_hash(user['password'], password):
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    flash('Login successful!', 'success')
                    return redirect(url_for('account'))
                else:
                    flash('Invalid username or password', 'danger')
            except Exception as e:
                flash('Database error occurred', 'danger')
            finally:
                conn.close()
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        full_name = request.form['full_name']
        age = request.form['age']
        gender = request.form['gender']
        diabetes_type = request.form['diabetes_type']
        diagnosis_date = request.form['diagnosis_date']
        
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, email, password, full_name, age, gender, diabetes_type, diagnosis_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (username, email, password, full_name, age, gender, diabetes_type, diagnosis_date))
                conn.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                flash('Username or email already exists', 'danger')
            finally:
                conn.close()
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# Main routes (keeping original template names)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
def account():
    if 'user_id' not in session:
        flash('Please login to access this page', 'warning')
        return redirect(url_for('login'))
    
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
            user = cursor.fetchone()
            
            cursor.execute("""
                SELECT * FROM predictions 
                WHERE user_id = %s 
                ORDER BY prediction_date DESC 
                LIMIT 5
            """, (session['user_id'],))
            recent_predictions = cursor.fetchall()
            
            for pred in recent_predictions:
                pred['image_url'] = url_for('static', filename=pred['image_path'])
            
            return render_template('account.html', user=user, predictions=recent_predictions)
        except Exception as e:
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    
    return redirect(url_for('index'))

@app.route('/retinopathy', methods=['GET', 'POST'])
def retinopathy():
    if 'user_id' not in session:
        flash('Please login to access this page', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_dir = os.path.join(app.static_folder, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Create unique filename to prevent collisions
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            filepath = os.path.join(upload_dir, unique_filename)
            
            try:
                file.save(filepath)
                prediction = predict_condition(filepath)
                
                # Use forward slashes for web paths
                db_image_path = f'uploads/{unique_filename}'
                static_image_url = f'uploads/{unique_filename}'  # Relative to static folder
                
                conn = create_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO predictions 
                            (user_id, image_path, condition_detected, confidence)
                            VALUES (%s, %s, %s, %s)
                        """, (session['user_id'], db_image_path,
                              prediction['condition'], prediction['confidence']))
                        conn.commit()
                    except Exception as e:
                        print(f"Database error: {e}")
                        flash('Error saving prediction to database', 'danger')
                    finally:
                        conn.close()
                
                return render_template('retinopathy.html',
                    prediction=prediction,
                    image_url=static_image_url)  # This should match how history displays images
                
            except Exception as e:
                flash(f'Error processing image: {str(e)}', 'danger')
                print(f"Error: {str(e)}")
                if os.path.exists(filepath):
                    os.remove(filepath)
    
    return render_template('retinopathy.html')

if __name__ == '__main__':
    app.secret_key = app.config['SECRET_KEY']
    app.run(debug=True)