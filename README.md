run4.py is the working version

run it as follows:

`python run4.py s1-exa2-solution.ipynb test2.py` to see a succesful file

and the following to see the output on a skeleton file, which will fail:

`python run4.py s1-exa2-challenge.ipynb test2.py`

The system output from the script is -1 if any test fails, or 0 if all tests pass.

Read the code. After mucking around too much with notebook client communicating with 0mq i decided to go with simple `exec`, in-process. This is not as secure as the 0mq approach, but it is much simpler and easier to debug. The code is not very long.

You might want to suppress a lot of the prints. I left them in for debugging purposes.

I followed the `None` returning spec in `ed-testing.pdf`, but have not implemented the dictionary return yet. I dont know id the TA's use it.
