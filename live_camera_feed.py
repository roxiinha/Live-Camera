from flask import Flask, Response
import cv2

app = Flask(__name__)

def generate_frames():
    # Abra a câmera (0 para a webcam padrão)
    cap = cv2.VideoCapture(0)
    while True:
        # Capture frame a frame
        success, frame = cap.read()
        if not success:
            break
        else:
            # Codifique o frame em JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        
        # Envie o frame codificado
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
        <html>
            <body>
                <h1>Live Camera Feed</h1>
                <img src="/video_feed" width="640" height="480">
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)