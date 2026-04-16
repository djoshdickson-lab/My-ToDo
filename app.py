from flask import Flask, render_template_string, url_for
import os

app = Flask(__name__)

# We use triple quotes to wrap the entire HTML block
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <title>my todo</title>
    
    <link rel="icon" type="image/png" href="{{ url_for('static', filename='icon.png') }}">
    <link rel="apple-touch-icon" href="{{ url_for('static', filename='icon.png') }}">
    
    <style>
        body { font-family: -apple-system, sans-serif; padding: 20px; background: #f0f2f5; color: #1a1a1a; }
        .container { max-width: 500px; margin: auto; }
        h1 { text-align: center; margin-bottom: 30px; font-weight: 800; }
        
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input { flex: 1; padding: 15px; border-radius: 12px; border: 1px solid #ddd; font-size: 16px; outline: none; }
        button#add-btn { padding: 15px 20px; border-radius: 12px; background: #007bff; color: white; border: none; font-weight: bold; }
        
        .todo-item { 
            background: white; padding: 18px; margin-bottom: 10px; 
            border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.2s; touch-action: manipulation;
            user-select: none; -webkit-user-select: none;
        }
        .completed { text-decoration: line-through; color: #aaa; background: #f9f9f9; }
        
        /* Visual cue when pressing */
        .todo-item:active { background: #ffebeb; transform: scale(0.96); }
    </style>
</head>
<body>
    <div class="container">
        <h1>my todo</h1>
        <div class="input-group">
            <input type="text" id="todo-input" placeholder="Add a task..." autocomplete="off">
            <button id="add-btn">Add</button>
        </div>
        <div id="todo-list"></div>
    </div>

    <script>
        const input = document.getElementById('todo-input');
        const btn = document.getElementById('add-btn');
        const list = document.getElementById('todo-list');

        // Load data from phone storage
        let todos = JSON.parse(localStorage.getItem('my_tasks')) || [];

        function render() {
            list.innerHTML = '';
            todos.forEach((todo, index) => {
                const div = document.createElement('div');
                div.className = `todo-item ${todo.done ? 'completed' : ''}`;
                div.innerText = todo.text;
                
                let holdTimer;

                // Long Press to Delete (3 seconds)
                div.addEventListener('touchstart', () => {
                    holdTimer = setTimeout(() => {
                        if(confirm('Delete this task?')) {
                            todos.splice(index, 1);
                            save();
                        }
                    }, 3000); 
                });

                div.addEventListener('touchend', () => {
                    clearTimeout(holdTimer);
                });

                // Single Tap to Strikeout
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
    # Standard Render port logic
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
