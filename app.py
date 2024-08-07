from flask import Flask, render_template, jsonify, request
from ChessEngineTest import Gamestate

app = Flask(__name__)
game = Gamestate()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    move = request.json['move']
    result = game.make_move(move)
    return jsonify(result)

@app.route('/board')
def board():
    board_state = game.get_board_state()
    return jsonify(board_state)

if __name__ == '__main__':
    app.run(debug=True)

