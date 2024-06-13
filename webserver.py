from flask import Flask, render_template, request, jsonify
import constants

controller = None

class WebServer:

    app = Flask(__name__)
    mainController = None

    @app.route('/')
    def index():
        return render_template('index.html')
        
    @app.route('/light/brightness', methods=["POST"])
    def setBrightness():
        global controller
        
        brightness = int(request.json['brightness'])
        
        if brightness is None or brightness < 1 or brightness > 255:
            print('Received invalid brightness ', brightness)
            return ('', 422)
          
        controller.setBrightness(brightness)
        return('', 204)
        
        

        
    @app.route('/light/color', methods=["POST"])
    def setColor():
        global controller
        
        color = request.json['color']
        print('Received request to set color to ', color)
        
        enumColor = None
        if color == 'WHITE':
            enumColor = constants.Color.WHITE
        elif color == 'RAINBOW':
            enumColor = constants.Color.RAINBOW
        
        if enumColor is None:
            return('', 422)
            
        controller.setColor(enumColor)
        return('', 204)
        
    def __init__(self, mainController = None):
        global controller
        print('Initializing webserver')
        controller = mainController
        
    def startServer(self):
        print('Starting server')
        self.app.run(debug=False, use_reloader=False, port=5000, host='0.0.0.0')
        
        print('Server stopped')

        
if __name__ == '__main__':
    webServer = WebServer()
    webServer.startServer()
