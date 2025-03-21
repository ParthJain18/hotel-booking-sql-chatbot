from services.sql_agent.agent import query_agent
import os
from io import BytesIO
import base64
from PIL import Image

def process_query(query_text: str, history_id: str):
    result = query_agent(query_text, history_id)
    images = []
    
    temp_dir = "data/temp_figures"
    if os.path.exists(temp_dir):
        temp_files = os.listdir(temp_dir)
        
        for filename in temp_files:
            file_path = os.path.join(temp_dir, filename)
            try:
                with Image.open(file_path) as img:
                    img_buffer = BytesIO()
                    img.save(img_buffer, format=img.format or "PNG")
                    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                    
                    images.append({
                        "filename": filename,
                        "data": img_str,
                        "format": img.format or "PNG"
                    })
                
                os.remove(file_path)
            except Exception as e:
                print(f"Error processing image file {filename}: {str(e)}")
    
    return {
        "answer": result.get("answer", "Sorry, I couldn't generate an answer."),
        "sql": result.get("query", ""),
        "time_taken": result.get("time_taken", ""),
        "images": images
    }