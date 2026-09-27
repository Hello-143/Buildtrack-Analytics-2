import json
import sys
import os

def run_notebook(notebook_path):
    print(f"--- Running Notebook: {notebook_path} ---")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Save the original stdout/stderr and working directory
    original_cwd = os.getcwd()
    notebook_dir = os.path.dirname(os.path.abspath(notebook_path))
    
    # Change CWD to the notebook directory to ensure relative paths inside the notebook work
    os.chdir(notebook_dir)
    sys.path.append(os.path.abspath('../src'))
    
    # Global environment for execution
    globals_dict = {
        '__name__': '__main__',
        '__file__': os.path.basename(notebook_path)
    }
    
    # Pre-inject Agg backend configuration for matplotlib to avoid blocking GUI loops
    try:
        import matplotlib
        matplotlib.use('Agg')
        print("Set Matplotlib backend to 'Agg'")
    except ImportError:
        pass
    
    try:
        for idx, cell in enumerate(nb.get('cells', [])):
            if cell.get('cell_type') == 'code':
                source_lines = cell.get('source', [])
                source_code = "".join(source_lines)
                if not source_code.strip():
                    continue
                
                # Execute the cell
                print(f"Executing Cell {idx}...")
                exec(source_code, globals_dict)
    except Exception as e:
        print(f"Error executing notebook {notebook_path} in cell {idx}: {e}")
        import traceback
        traceback.print_exc()
        raise e
    finally:
        # Restore CWD
        os.chdir(original_cwd)
        if os.path.abspath('../src') in sys.path:
            sys.path.remove(os.path.abspath('../src'))
    print(f"--- Finished Notebook: {notebook_path} ---\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_notebook.py <path_to_notebook.ipynb>")
        sys.exit(1)
    run_notebook(sys.argv[1])
