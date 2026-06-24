import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

PLAYLIST_ID = "PL3S5BTe0yy93_EoPufvRFCtMGxjNmmvPj"
URL = f"https://www.youtube.com/feeds/videos.xml?playlist_id={PLAYLIST_ID}"

try:
    # משיכת הנתונים מיוטיוב בחינם לחלוטין
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}
    
    # לקיחת 7 הסרטונים האחרונים
    entries = root.findall('atom:entry', ns)[:7]
    
    # בניית קובץ ה-HTML שלנו
    html_content = """<!DOCTYPE html>
    <html dir="rtl" lang="he">
    <head>
        <meta charset="UTF-8">
        <style>
            body { margin: 0; padding: 0; font-family: inherit; background-color: transparent; }
            .lessons-list { display: flex; flex-direction: column; gap: 10px; max-height: 250px; overflow-y: auto; padding-left: 5px; }
            .lessons-list::-webkit-scrollbar { width: 6px; }
            .lessons-list::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
            .lessons-list::-webkit-scrollbar-thumb { background: #ccc; border-radius: 10px; }
            .lesson-item { display: flex; gap: 12px; align-items: center; background: #f9f9f9; border: 1px solid #eee; padding: 8px; border-radius: 6px; text-decoration: none; transition: background 0.2s ease, transform 0.2s ease; }
            .lesson-item:hover { background: #f0f0f0; transform: translateY(-2px); }
            .lesson-thumb { width: 90px; height: 50px; object-fit: cover; border-radius: 4px; flex-shrink: 0; }
            .lesson-info { display: flex; flex-direction: column; gap: 4px; }
            .lesson-title { color: #222; font-size: 0.9rem; font-weight: bold; line-height: 1.2; margin: 0; }
            .lesson-date { color: #777; font-size: 0.8rem; margin: 0; }
        </style>
    </head>
    <body>
        <div class="lessons-list">
    """

    for entry in entries:
        video_id = entry.find('yt:videoId', ns).text
        title = entry.find('atom:title', ns).text
        date_str = entry.find('atom:published', ns).text
        
        # סידור התאריך לפורמט ישראלי (יום/חודש/שנה)
        date_obj = datetime.strptime(date_str[:10], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")
        
        thumb_url = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        html_content += f'''
            <a href="{video_url}" target="_blank" class="lesson-item">
                <img src="{thumb_url}" alt="שיעור" class="lesson-thumb">
                <div class="lesson-info">
                    <p class="lesson-title">{title}</p>
                    <p class="lesson-date">{formatted_date}</p>
                </div>
            </a>
        '''

    html_content += """
        </div>
    </body>
    </html>
    """

    # שמירת הקובץ
    with open("lessons.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("Lessons updated successfully!")

except Exception as e:
    print(f"Error: {e}")
