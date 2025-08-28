import os
import json
import csv
import uuid
import shutil
import logging
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Enable CORS for all routes
CORS(app, origins=["*"])

# Base directory for storing data
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Model names for directory creation
MODEL_NAMES = [
    "qwen_CoT_video_image_info",
    "qwen_CoT_video_image_raw", 
    "qwen_CoT_description_info",
    "qwen_video_image_info",
    "qwen_video_image_raw",
    "qwen_description_info",
    "smol_CoT_video_image_info",
    "smol_CoT_video_image_raw",
    "smol_CoT_description_info",
    "smol_video_image_info",
    "smol_video_image_raw",
    "smol_description_info"
]

def get_model_dir(uuid_str, model_name):
    """Get the directory path for a specific UUID and model"""
    return DATA_DIR / uuid_str / model_name

def get_csv_path(uuid_str, model_name, csv_type):
    """Get the path for a specific CSV file"""
    model_dir = get_model_dir(uuid_str, model_name)
    return model_dir / f"{csv_type}.csv"

def ensure_model_dir(uuid_str, model_name):
    """Ensure the model directory exists"""
    model_dir = get_model_dir(uuid_str, model_name)
    model_dir.mkdir(parents=True, exist_ok=True)
    return model_dir

def create_sample_csv(filepath, csv_type, num_items=50):
    """Create a sample CSV file with realistic structure"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    if csv_type == "video_description":
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['product_id', 'description_key1', 'description_key2', 'description_key3'])
            for i in range(1, num_items + 1):
                writer.writerow([
                    f'P{i:04d}',
                    f'Video shows product features {i}',
                    f'Duration: {30 + i % 60} seconds',
                    f'Quality: {"HD" if i % 3 == 0 else "Standard"}'
                ])
    
    elif csv_type == "product_info":
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['product_id', 'brand', 'price', 'spec', 'category'])
            categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
            brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']
            for i in range(1, num_items + 1):
                writer.writerow([
                    f'P{i:04d}',
                    brands[i % len(brands)],
                    f'${(i * 10) % 500 + 20}',
                    f'Model-{i}-XL',
                    categories[i % len(categories)]
                ])
    
    elif csv_type == "judgement":
        import random
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['product_id', 'product_name', 'category', 'video_url', 'thumbnail_url', 
                           'ground_truth_image_url', 'label', 'reason'])
            
            labels = ['Yes', 'N/A', 'No']
            categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
            
            for i in range(1, num_items + 1):
                label = random.choice(labels)
                reasons = {
                    'Yes': f'Product clearly matches criteria {i}',
                    'N/A': f'Product information insufficient for determination {i}',
                    'No': f'Product does not meet the required standards {i}'
                }
                
                writer.writerow([
                    f'P{i:04d}',
                    f'Sample Product {i}',
                    categories[i % len(categories)],
                    f'http://example.com/video{i}.mp4',
                    f'http://example.com/thumb{i}.jpg',
                    f'http://example.com/gt{i}.jpg',
                    label,
                    reasons[label]
                ])

@app.route('/pull_data', methods=['POST'])
def pull_data():
    """Pull data endpoint - simulates data collection"""
    try:
        data = request.get_json()
        uuid_str = data.get('uuid')
        days_back = data.get('days_back')
        
        if not uuid_str or not days_back:
            return jsonify({'ok': False, 'error': 'Missing uuid or days_back'}), 400
        
        if not isinstance(days_back, int) or days_back < 1:
            return jsonify({'ok': False, 'error': 'days_back must be a positive integer'}), 400
        
        # Create directories for all models
        for model_name in MODEL_NAMES:
            ensure_model_dir(uuid_str, model_name)
        
        app.logger.info(f"Data pull completed for UUID {uuid_str}, {days_back} days back")
        return jsonify({'ok': True})
        
    except Exception as e:
        app.logger.error(f"Error in pull_data: {str(e)}")
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/make_video_description', methods=['POST'])
def make_video_description():
    """Generate video descriptions"""
    try:
        data = request.get_json()
        uuid_str = data.get('uuid')
        model = data.get('model')
        
        if not uuid_str or not model:
            return jsonify({'ok': False, 'error': 'Missing uuid or model'}), 400
        
        if model not in MODEL_NAMES:
            return jsonify({'ok': False, 'error': 'Invalid model name'}), 400
        
        # Create the CSV file
        csv_path = get_csv_path(uuid_str, model, 'video_description')
        create_sample_csv(csv_path, 'video_description')
        
        app.logger.info(f"Video description CSV created for UUID {uuid_str}, model {model}")
        return jsonify({'ok': True})
        
    except Exception as e:
        app.logger.error(f"Error in make_video_description: {str(e)}")
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/make_product_info', methods=['POST'])
def make_product_info():
    """Generate product information"""
    try:
        data = request.get_json()
        uuid_str = data.get('uuid')
        model = data.get('model')
        
        if not uuid_str or not model:
            return jsonify({'ok': False, 'error': 'Missing uuid or model'}), 400
        
        if model not in MODEL_NAMES:
            return jsonify({'ok': False, 'error': 'Invalid model name'}), 400
        
        # Create the CSV file
        csv_path = get_csv_path(uuid_str, model, 'product_info')
        create_sample_csv(csv_path, 'product_info')
        
        app.logger.info(f"Product info CSV created for UUID {uuid_str}, model {model}")
        return jsonify({'ok': True})
        
    except Exception as e:
        app.logger.error(f"Error in make_product_info: {str(e)}")
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/judge', methods=['POST'])
def judge():
    """Run judgement process"""
    try:
        data = request.get_json()
        uuid_str = data.get('uuid')
        model = data.get('model')
        
        if not uuid_str or not model:
            return jsonify({'ok': False, 'error': 'Missing uuid or model'}), 400
        
        if model not in MODEL_NAMES:
            return jsonify({'ok': False, 'error': 'Invalid model name'}), 400
        
        # Create the CSV file
        csv_path = get_csv_path(uuid_str, model, 'judgement')
        create_sample_csv(csv_path, 'judgement')
        
        app.logger.info(f"Judgement CSV created for UUID {uuid_str}, model {model}")
        return jsonify({'ok': True})
        
    except Exception as e:
        app.logger.error(f"Error in judge: {str(e)}")
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get processing status for a UUID and model"""
    try:
        uuid_str = request.args.get('uuid')
        model = request.args.get('model')
        
        if not uuid_str or not model:
            return jsonify({'error': 'Missing uuid or model'}), 400
        
        if model not in MODEL_NAMES:
            return jsonify({'error': 'Invalid model name'}), 400
        
        # Check if CSV files exist
        video_desc_path = get_csv_path(uuid_str, model, 'video_description')
        product_info_path = get_csv_path(uuid_str, model, 'product_info')
        judgement_path = get_csv_path(uuid_str, model, 'judgement')
        
        status = {
            'video_description_csv': 'complete' if video_desc_path.exists() else 'pending',
            'product_info_csv': 'complete' if product_info_path.exists() else 'pending',
            'judgement_csv': 'complete' if judgement_path.exists() else 'pending'
        }
        
        return jsonify(status)
        
    except Exception as e:
        app.logger.error(f"Error in get_status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/results', methods=['GET'])
def get_results():
    """Get results from CSV files"""
    try:
        uuid_str = request.args.get('uuid')
        model = request.args.get('model')
        
        if not uuid_str or not model:
            return jsonify({'error': 'Missing uuid or model'}), 400
        
        if model not in MODEL_NAMES:
            return jsonify({'error': 'Invalid model name'}), 400
        
        # Read CSV files
        video_desc_path = get_csv_path(uuid_str, model, 'video_description')
        product_info_path = get_csv_path(uuid_str, model, 'product_info')
        judgement_path = get_csv_path(uuid_str, model, 'judgement')
        
        if not all([video_desc_path.exists(), product_info_path.exists(), judgement_path.exists()]):
            return jsonify({'error': 'Not all required CSV files exist'}), 400
        
        # Read video descriptions
        video_descriptions = {}
        with open(video_desc_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_id = row['product_id']
                video_descriptions[product_id] = {k: v for k, v in row.items() if k != 'product_id'}
        
        # Read product info
        product_infos = {}
        with open(product_info_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_id = row['product_id']
                product_infos[product_id] = {k: v for k, v in row.items() if k != 'product_id'}
        
        # Read judgement data
        items = []
        label_counts = {'Yes': 0, 'N/A': 0, 'No': 0}
        
        with open(judgement_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_id = row['product_id']
                label = row['label']
                
                item = {
                    'product_id': product_id,
                    'product_name': row['product_name'],
                    'category': row['category'],
                    'video_url': row['video_url'],
                    'thumbnail_url': row['thumbnail_url'],
                    'ground_truth_image_url': row['ground_truth_image_url'],
                    'label': label,
                    'reason': row['reason'],
                    'video_description': video_descriptions.get(product_id, {}),
                    'product_info': product_infos.get(product_id, {})
                }
                
                items.append(item)
                if label in label_counts:
                    label_counts[label] += 1
        
        result = {
            'counts': label_counts,
            'items': items
        }
        
        return jsonify(result)
        
    except Exception as e:
        app.logger.error(f"Error in get_results: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/override_label', methods=['POST'])
def override_label():
    """Override a product label in the judgement CSV"""
    try:
        data = request.get_json()
        uuid_str = data.get('uuid')
        model = data.get('model')
        product_id = data.get('product_id')
        new_label = data.get('new_label')
        
        if not all([uuid_str, model, product_id, new_label]):
            return jsonify({'ok': False, 'error': 'Missing required parameters'}), 400
        
        if model not in MODEL_NAMES:
            return jsonify({'ok': False, 'error': 'Invalid model name'}), 400
        
        if new_label not in ['Yes', 'N/A', 'No']:
            return jsonify({'ok': False, 'error': 'Invalid label'}), 400
        
        judgement_path = get_csv_path(uuid_str, model, 'judgement')
        
        if not judgement_path.exists():
            return jsonify({'ok': False, 'error': 'Judgement CSV not found'}), 400
        
        # Read existing data
        rows = []
        with open(judgement_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['product_id'] == product_id:
                    row['label'] = new_label
                rows.append(row)
        
        # Write back the updated data
        if rows:
            with open(judgement_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        
        app.logger.info(f"Label override completed for product {product_id} to {new_label}")
        return jsonify({'ok': True})
        
    except Exception as e:
        app.logger.error(f"Error in override_label: {str(e)}")
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_all():
    """Clear all data for a UUID across all models"""
    try:
        data = request.get_json()
        uuid_str = data.get('uuid')
        
        if not uuid_str:
            return jsonify({'ok': False, 'error': 'Missing uuid'}), 400
        
        # Remove the entire UUID directory
        uuid_dir = DATA_DIR / uuid_str
        if uuid_dir.exists():
            shutil.rmtree(uuid_dir)
            app.logger.info(f"Cleared all data for UUID {uuid_str}")
        
        return jsonify({'ok': True})
        
    except Exception as e:
        app.logger.error(f"Error in clear_all: {str(e)}")
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/')
def index():
    """Serve the main HTML file"""
    return app.send_static_file('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Video Review Pipeline API is running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
