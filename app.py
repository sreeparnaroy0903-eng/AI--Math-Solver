from flask import Flask, request, jsonify, send_from_directory
from sympy import *
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

@app.route('/')
def serve_home():
    return send_from_directory('.', 'index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    problem_type = data.get('type')
    expression = data.get('expression')
    result = ""
    steps = []

    try:
        if problem_type == "derivative":
            expr = sympify(expression)
            deriv = diff(expr)
            steps.append("Step 1: Differentiate each term of the expression.")
            steps.append(f"Final Result: {deriv}")
            result = str(deriv)

        elif problem_type == "integration":
            expr = sympify(expression)
            integ = integrate(expr)
            steps.append("Step 1: Integrate each term individually.")
            steps.append(f"Final Result: {integ}")
            result = str(integ)

        elif problem_type == "quadratic":
            a, b, c = symbols('a b c')
            expr = Eq(a*symbols('x')**2 + b*symbols('x') + c, 0)
            sol = solve(expr, symbols('x'))
            steps.append("Step 1: Apply the quadratic formula.")
            steps.append(f"Final Result: {sol}")
            result = str(sol)

        elif problem_type == "arithmetic":
            result = str(eval(expression))
            steps.append("Step 1: Evaluate the arithmetic expression.")
            steps.append(f"Final Result: {result}")

        elif problem_type == "linear":
            x = symbols('x')
            expr = Eq(sympify(expression.split('=')[0]), sympify(expression.split('=')[1]))
            sol = solve(expr, x)
            steps.append("Step 1: Isolate variable x.")
            steps.append(f"Final Result: x = {sol}")
            result = f"x = {sol}"

        else:
            result = "Unsupported problem type."

    except Exception as e:
        result = f"Error: {str(e)}"

    return jsonify({"result": result, "steps": steps})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
