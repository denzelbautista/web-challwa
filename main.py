# main.py
from flask import Flask, request, jsonify
from database import init_app, db
from models import User

app = Flask(__name__)
init_app(app)

def fibo(n):
    if n == 0 or n == 1:
        return n
    else: 
        return fibo(n-1) + fibo(n-2)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')

    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'})

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])



    


if __name__ == '__main__':
    app.run(debug=True)

"""
@app.route('/fibonacci/<number>',methods=['GET'])
def get_nth_fibonacci(number):

    num = int(number)

    def fibo(n):
        if n == 0 or n == 1:
            return n
        else: 
            return fibo(n-1) + fibo(n-2)
         
    result = fibo(num)
        
    return jsonify({f'fibo for {num} is :':result})
"""