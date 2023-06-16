import nbclient
import nbformat
import io
import importlib
import contextlib
import sys

class Context:
    def __init__(self, src, kernel):
        self.src = src
        self.kernel = kernel

    def evaluate(self, s):
        # Evaluate expression in kernel's namespace
        result = self.kernel.execute(f"result = {s}", silent=True)
        return self.kernel.get("result")

    def execute(self, s):
        # Execute code in kernel's namespace
        self.kernel.execute(s)

    def __getattr__(self, name):
        return self.evaluate(name)

    def __getitem__(self, name):
        return self.evaluate(name)

# Paths
notebook_path = sys.argv[1]
test_module_path = sys.argv[2]

# Load the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)
# Load the test module
spec = importlib.util.spec_from_file_location("test", test_module_path)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)
client = nbclient.NotebookClient(nb, timeout=600, kernel_name='ml1-arm64', resources={'metadata': {'path': '.'}})
#print(client.kernel_name)
#print("Kernel Name: ", client.kc.kernel_info())
# client.execute()
#sys.exit(1)
# Iterate through cells and execute them one by one
with client.setup_kernel():
    for cell_index, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            # Execute the current cell

            #print(f"Executing cell {cell_index}...")
            #print(cell['source'])
            client.execute_cell(cell, cell_index)

            # Check if the first line matches the format
            lines = cell['source'].split('\n')
            if lines and lines[0].startswith("### edTest("):
                # Extract test function name
                test_name = lines[0].split('(')[1].split(')')[0].strip()
                print(f"Found test function '{test_name}'")
                # Prepare the context object
                src = cell['source']
                stdout = ''.join(output.get('text', '') for output in cell.get('outputs', []) if output['output_type'] == 'stream' and output['name'] == 'stdout')
                stderr = ''.join(output.get('text', '') for output in cell.get('outputs', []) if output['output_type'] == 'stream' and output['name'] == 'stderr')
                context = Context(src, client.kc.kernel)
                context.stdout.write(stdout)
                context.stderr.write(stderr)

                # Run the test function
                test_function = getattr(test_module, test_name, None)
                if test_function:
                    print(
                        f"Running test function '{test_name}'...with {context}"
                    )
                    test_function(context)
                else:
                    print(f"Test function '{test_name}' not found in test module.")
