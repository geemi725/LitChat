## Setting up the environment: luckily we only have to do the following once!
1)  First things first. It is easier if install Anaconda and VSCode in your computer. Check these videos: 

- [Install Anaconda](https://www.youtube.com/watch?v=RFeIn2ywxG4) 
- [Install VSCode](https://www.youtube.com/watch?v=B-s71n0dHUk)

2) Once you have installed Anaconda, you can create a conda environment and then install all the project related software in it. To create the environment, do `conda create --name litchat` from your terminal. Here "litchat" is the name of your environment. It can be any name you want.

3) Next you have to activate the environment and install the packages. To activate do: `conda activate litchat`. 

4) To install packages, you have to first go to the LitChat directory and do: `conda install --yes --file requirements.txt`.

5) Next, you have to add the created conda environment as a jupyter kernal so that your jupyter notebooks can work in this environment. Do the following:
- `pip install ipykernel`
- `python -m ipykernel install --user --name litchat --display-name "litchat"`

6) Hang on tight we're almost there. Make sure to install the mistral large langauge model using Ollama. Do: `ollama pull mistral`. For more details [check the Ollama GitHub repo!](https://github.com/ollama/ollama)

## How to use the project

**There are two approaches:** 
1) If you want to get yourself familiarized with what we are doing, you can use the `example_notebook.ipynb`. Simply open it and play with it.

2) Run the `create_dataset.py` script. First, you have to setup the arguments in this file. This script runs the entire pipeline of data extraction for your papers based on the questions/queries. 

Something to keep in mind is that, if you're using the same PDF files, again and again, to make the code run faster, you can create vector databases once with `create_db = True`. From the next time onwards set it to `False` and provide a `vect_dir` path. This will tell the code to read from the already vectorized PDFs instead of creating vector databases every time. 