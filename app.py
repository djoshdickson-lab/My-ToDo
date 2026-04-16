from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <title>My Tasks</title>
    <style>
        body { font-family: -apple-system, sans-serif; padding: 20px; background: #f0f2f5; }
        .container { max-width: 500px; margin: auto; }
        h1 { text-align: center; color: #1a1a1a; }
        
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input { flex: 1; padding: 15px; border-radius: 12px; border: 1px solid #ddd; font-size: 16px; }
        button#add-btn { padding: 15px 20px; border-radius: 12px; background: #007bff; color: white; border: none; font-weight: bold; }
        
        .todo-item { 
            background: white; padding: 18px; margin-bottom: 10px; 
            border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex; justify-content: space-between; align-items: center;
            transition: transform 0.1s; touch-action: manipulation;
        }
        .completed { text-decoration: line-through; color: #aaa; background: #f9f9f9; }
    </style>
</head>
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

        // 1. Load data from phone storage on startup
        let todos = JSON.parse(localStorage.getItem('my_tasks')) || [];

        function render() {
            list.innerHTML = '';
            todos.forEach((todo, index) => {
                const div = document.createElement('div');
                div.className = `todo-item ${todo.done ? 'completed' : ''}`;
                div.innerText = todo.text;
                
                // Single Tap to Strike out
                div.onclick = () => {
                    todos[index].done = !todos[index].done;
                    save();
                };

                // Double Tap to Delete
                let lastTap = 0;
                div.addEventListener('touchend', (e) => {
                    let now = new Date().getTime();
                    if (now - lastTap < 300) {
                        todos.splice(index, 1);
                        save();
                    }
                    lastTap = now;
                });

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

        render(); // Initial draw
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run()
  
