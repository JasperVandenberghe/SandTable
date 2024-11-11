from flask import Flask, render_template, request, jsonify
import constants

mainController = None

class WebServer:

    app = Flask(__name__)
    #mainController = None

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/program/state', methods=["POST"])
    def setProgramState():
        global mainController
        
        state = request.json['state']
        
        if state == 'PAUSE':
            mainController.pauseProgram()
        elif state == 'RESUME':
            mainController.resumeProgram()
        elif state == 'QUIT':
            mainController.quitProgram()
        else:
            return('', 422)
        
        return('', 204)
        
    @app.route('/light/brightness', methods=["POST"])
    def setBrightness():
        global mainController
        
        brightness = int(request.json['brightness'])
        
        if brightness is None or brightness < 1 or brightness > 255:
            print('Received invalid brightness ', brightness)
            return ('', 422)
          
        mainController.setBrightness(brightness)
        return('', 204)        
        
    @app.route('/light/color', methods=["POST"])
    def setColor():
        global mainController
        
        color = request.json['color']        
        enumColor = None
        
        if color == 'WHITE':
            enumColor = constants.Color.WHITE
        elif color == 'RAINBOW':
            enumColor = constants.Color.RAINBOW
        
        if enumColor is None:
            return('', 422)
            
        mainController.setColor(enumColor)
        return('', 204)
        
    def __init__(self, controller):
        global mainController
        
        mainController = controller
        print('Main controller: ')
        print(mainController)
        
    def startServer(self):
        print('Starting server')
        self.app.run(debug=False, use_reloader=False, port=5000, host='0.0.0.0')
        
if __name__ == '__main__':
    webServer = WebServer()
    webServer.startServer()
