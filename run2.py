import nbclient
import nbformat
import importlib
import io
import traceback
import sys

class Context:
    def __init__(self, client, src):
        self.client = client
        self.src = src
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()

    def evaluate(self, s):
        code = f"{s}"
        print("execing", code)
        reply = self.client.execute(code)
        for output in reply['outputs']:
            if 'data' in output and 'text/plain' in output['data']:
                return output['data']['text/plain']

    def execute(self, s):
        self.client.execute(s, silent=True)

    def __getattr__(self, name):
        return self.evaluate(name)

    def __getitem__(self, name):
        return self.evaluate(name)

class CustomNotebookClient(nbclient.NotebookClient):
    def __init__(self, nb, test_module, **kw):
        super().__init__(nb, **kw)
        self.test_module = test_module

    def on_cell_complete(self, cell, cell_index):
        # Check if the first line matches the format
        lines = cell['source'].split('\n')
        print(f"Cell {cell_index} {lines[0]}. Checking for test function...")
        if lines and lines[0].startswith("### edTest("):
            # Extract test function name
            test_name = lines[0].split('(')[1].split(')')[0].strip()

            # Prepare the context object
            context = Context(self, cell['source'])
            stdout = ''.join(output.get('text', '') for output in cell.get('outputs', []) if output['output_type'] == 'stream' and output['name'] == 'stdout')
            stderr = ''.join(output.get('text', '') for output in cell.get('outputs', []) if output['output_type'] == 'stream' and output['name'] == 'stderr')
            context.stdout.write(stdout)
            context.stderr.write(stderr)
            # Run the test function
            test_function = getattr(self.test_module, test_name, None)
            if test_function:
                print(f"Running test function '{test_name}'...")
                try:
                    returnval = test_function(context)
                    if returnval==None:
                        print(f"Test function '{test_name}' returned None. SUCCESS")
                    else:
                        print(f"Test function '{test_name}' returned {returnval}. FAILURE")
                except:
                    print(f"Test function '{test_name}' failed with exception:")
                    print("".join(traceback.format_exception(*sys.exc_info())))
            else:
                print(f"Test function '{test_name}' not found in test module.")


# Paths
notebook_path = 's1-exa2-solution.ipynb'
test_module_path = 'test2.py'

# Load the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Load the test module
spec = importlib.util.spec_from_file_location("test", test_module_path)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

# Create a CustomNotebookClient and execute the notebook
client = CustomNotebookClient(nb, test_module, kernel_name='ml1-arm64')
client.execute()
