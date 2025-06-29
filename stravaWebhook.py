from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

STRAVA_VERIFY_TOKEN = os.environ.get("STRAVA_VERIFY_TOKEN")
STRAVA_ACCESS_TOKEN = os.environ.get("STRAVA_ACCESS_TOKEN")
TRAININGPEAKS_UPLOAD_URL = "https://api.trainingpeaks.com/file/upload"
TRAININGPEAKS_AUTH = (os.environ.get("TP_USERNAME"), os.environ.get("TP_PASSWORD"))

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # if request.method == 'GET':
    #     if request.args.get('hub.verify_token') == STRAVA_VERIFY_TOKEN:
    #         return jsonify({'hub.challenge': request.args.get('hub.challenge')})
    #     return "Verification failed", 403

    # if request.method == 'POST':
    #     data = request.get_json()
    #     if data['object_type'] == 'activity' and data['aspect_type'] == 'create':
    #         activity_id = data['object_id']
    #         download_and_upload_fit(activity_id)
    #     return '', 200
    if request.method == 'GET':
        print('Webhook received')
        return '',204

def download_and_upload_fit(activity_id):
    headers = {'Authorization': f'Bearer {STRAVA_ACCESS_TOKEN}'}
    export_url = f"https://www.strava.com/api/v3/activities/{activity_id}/export_original"
    r = requests.get(export_url, headers=headers)
    
    if r.status_code == 200:
        with open('activity.fit', 'wb') as f:
            f.write(r.content)
        with open('activity.fit', 'rb') as f:
            response = requests.post(TRAININGPEAKS_UPLOAD_URL, files={'file': f}, auth=TRAININGPEAKS_AUTH)
            print("TrainingPeaks upload status:", response.status_code)
    else:
        print("Could not download FIT file:", r.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50001)
