from flask import Flask, render_template_string, url_for  # Added url_for here

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <title>My Tasks</title>
    
    <link rel="icon" type="image/png" href="{{ url_for('static', filename='icon.png') }}">
    <link rel="apple-touch-icon" href="{{ url_for('static', filename='icon.png') }}">
    
    <style>
        /* Your existing CSS here... */
    </style>
</head>
...
"""


<body>
    <div class="container">
        <h1>My Tasks</h1>
        <div class="input-group">
            <input type="text" id="todo-input" placeholder="What needs doing?">
            <button id="add-btn">Add</button>
        </div>
        <div id="todo-list"></div>
    </div>

    <script>
        const input = document.getElementById('todo-input');
        const btn = document.getElementById('add-btn');
        const list = document.getElementById('todo-list');

        let todos = JSON.parse(localStorage.getItem('my_tasks')) || [];

        function render() {
            list.innerHTML = '';
            todos.forEach((todo, index) => {
                const div = document.createElement('div');
                div.className = `todo-item ${todo.done ? 'completed' : ''}`;
                div.innerText = todo.text;
                
                let holdTimer;

                // 1. START HOLD (3 seconds)
                div.addEventListener('touchstart', (e) => {
                    holdTimer = setTimeout(() => {
                        // Success! Held for 3s
                        if(confirm('Delete this task?')) {
                            todos.splice(index, 1);
                            save();
                        }
                    }, 3000); // 3000ms = 3 seconds
                });

                // 2. CANCEL HOLD (If finger is lifted early)
                div.addEventListener('touchend', () => {
                    clearTimeout(holdTimer);
                });

                // 3. SINGLE CLICK (Toggle Strikeout)
                div.onclick = () => {
                    todos[index].done = !todos[index].done;
                    save();
                };

                list.appendChild(div);
            });
        }

        function save() {
            localStorage.setItem('my_tasks', JSON.stringify(todos));
            render();
        }

        btn.onclick = () => {
            if (input.value.trim()) {
                todos.push({ text: input.value, done: false });
                input.value = '';
                save();
            }
        };

        render();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run()
  
