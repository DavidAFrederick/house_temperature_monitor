# app.py
from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Sample data
    categories = ['A', 'B', 'C', 'D']
    values = [20, 35, 30, 25]

    # Create the bar graph
    plt.bar(categories, values)
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Graph Example')

    # Save the graph to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Encode the image to base64
    data = base64.b64encode(buf.read()).decode('utf-8')
    image_url = f'data:image/png;base64,{data}'

    # Render the template with the image URL
    return render_template('index.html', image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)