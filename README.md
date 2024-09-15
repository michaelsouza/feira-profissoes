# Math Tutor CLI with Code Interpreter

## Description

This project is a command-line application that serves as an interactive math tutor. It leverages OpenAI's GPT-4 model to solve mathematical problems step by step, providing clear and detailed explanations. The application integrates a Python code interpreter to perform calculations, allowing it to handle complex computations and visualize results when necessary.

## Features

- **Interactive Command-Line Interface**: Engages users through a rich-text interface for an enhanced experience.
- **Step-by-Step Solutions**: Breaks down math problems into understandable steps.
- **Code Execution**: Utilizes a built-in Python code interpreter for calculations.
- **Symbolic Mathematics**: Supports symbolic computations using SymPy.
- **Numerical Computations**: Handles numerical calculations with NumPy and SciPy.
- **Data Visualization**: Generates plots and graphs using Matplotlib and Seaborn.

## Installation

### Prerequisites

- **Python 3.7** or higher.
- An **OpenAI API key**. You can obtain one by signing up on the [OpenAI website](https://platform.openai.com/).

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/mathtutor-cli.git
   cd mathtutor-cli
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables**

   - Create a `.env` file in the project root directory.
   - Add your OpenAI API key to the `.env` file:

     ```
     OPENAI_API_KEY=your-openai-api-key
     ```

## Usage

Run the main script to start the application:

```bash
python math-tutor.py
```

### Example Interaction

```
╭──────────────────────────────────────── Feira das Profissões ─────────────────────────────────────────╮
│                                                                                                       │
│                                                                                                       │
│  __  __       _   _       _____      _                                       .="=.                    │
│ |  \/  | __ _| |_| |__   |_   _|   _| |_ ___  _ __                          /.-.-.\_     _            │
│ | |\/| |/ _` | __| '_ \    | || | | | __/ _ \| '__|                       ( ( o o ) )    ))           │
│ | |  | | (_| | |_| | | |   | || |_| | || (_) | |                           |/  "  \|    //            │
│ |_|  |_|\__,_|\__|_| |_|   |_| \__,_|\__\___/|_|           .-------.        \'---'/    //             │
│                                                           _|~~ ~~  |_       /`"""`\\  ((              │
│    _   _ _____ ____     ____   ___ ____  _  _           =(_|_______|_)=    / /_,_\ \\  \\             │
│   | | | |  ___/ ___|   |___ \ / _ \___ \| || |            |:::::::::|      \_\\_'__/ \  ))            │
│   | | | | |_ | |         __) | | | |__) | || |            |:::::::[]|       /`  /`~\  |//             │
│   | |_| |  _|| |___     / __/| |_| / __/|__   _|          |o=======.|      /   /       /              │
│    \___/|_|   \____|   |_____|\___/_____|  |_|            `"""""""""`  ,--`,--'\/\____/               │
│                                                                        '-- "--'                       │
│                                                                                                       │
│                                                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
Insira um problema matemático (or digite 'exit' para sair)
: Show that for any two vectors $x, y \in \mathbb{R}^n$, $| ||x|| - ||y|| | \leq ||x - y||$.
╭───────────────────────────────────────── Problema Matemático ─────────────────────────────────────────╮
│ Resolvendo:                                                                                           │
│ Show that for any two vectors $x, y \in \mathbb{R}^n$, $| ||x|| - ||y|| | \leq ||x - y||$.            │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
🚀 Calling OpenAI API ...
🚀 Calling OpenAI API ...


╭─────────────────────────────────────────── Resultado Final ───────────────────────────────────────────╮
│ Solução Completa:                                                                                     │
│ To demonstrate that for any two vectors \( x, y \in \mathbb{R}^n \), the inequality                   │
│                                                                                                       │
│ [                                                                                                     │
│ | ||x|| - ||y|| | \leq ||x - y||                                                                      │
│ \]                                                                                                    │
│                                                                                                       │
│ holds, we will utilize the properties of norms and the triangle inequality.                           │
│                                                                                                       │
│ ### Step 1: Understand the Expression                                                                 │
│                                                                                                       │
│ We begin by analyzing the expression:                                                                 │
│                                                                                                       │
│ [                                                                                                     │
│ | ||x|| - ||y|| |.                                                                                    │
│ \]                                                                                                    │
│                                                                                                       │
│ This represents the absolute difference between the norms of the vectors \( x \) and \( y \).         │
│                                                                                                       │
│ ### Step 2: Apply the Triangle Inequality                                                             │
│                                                                                                       │
│ Recall the triangle inequality, which states that for any vectors \( a \) and \( b \) in \(           │
│ \mathbb{R}^n \):                                                                                      │
│                                                                                                       │
│ [                                                                                                     │
│ ||a + b|| \leq ||a|| + ||b||.                                                                         │
│ \]                                                                                                    │
│                                                                                                       │
│ We can set \( a = x - y \) and \( b = y \). By this substitution, we can express \( ||x|| \) as       │
│ follows:                                                                                              │
│                                                                                                       │
│ [                                                                                                     │
│ ||x|| = ||(x - y) + y||.                                                                              │
│ \]                                                                                                    │
│                                                                                                       │
│ Using the triangle inequality, we obtain:                                                             │
│                                                                                                       │
│ [                                                                                                     │
│ ||x|| \leq ||x - y|| + ||y||.                                                                         │
│ \]                                                                                                    │
│                                                                                                       │
│ ### Step 3: Rearranging the Inequality                                                                │
│                                                                                                       │
│ From the previous inequality, we can rearrange it to isolate \( ||x|| - ||y|| \):                     │
│                                                                                                       │
│ [                                                                                                     │
│ ||x|| - ||y|| \leq ||x - y||.                                                                         │
│ \]                                                                                                    │
│                                                                                                       │
│ ### Step 4: Analyze the Reverse Case                                                                  │
│                                                                                                       │
│ Next, we want to consider the case for \( ||y|| - ||x|| \). We can apply the triangle inequality      │
│ again, this time setting \( a = y - x \) and \( b = x \):                                             │
│                                                                                                       │
│ [                                                                                                     │
│ ||y|| = ||(y - x) + x||.                                                                              │
│ \]                                                                                                    │
│                                                                                                       │
│ Applying the triangle inequality here gives us:                                                       │
│                                                                                                       │
│ [                                                                                                     │
│ ||y|| \leq ||y - x|| + ||x||,                                                                         │
│ \]                                                                                                    │
│                                                                                                       │
│ which can be rearranged to:                                                                           │
│                                                                                                       │
│ [                                                                                                     │
│ ||y|| - ||x|| \leq ||y - x|| = ||x - y||.                                                             │
│ \]                                                                                                    │
│                                                                                                       │
│ ### Step 5: Combine the Results                                                                       │
│                                                                                                       │
│ At this point, we have established two crucial inequalities:                                          │
│                                                                                                       │
│ 1. \( ||x|| - ||y|| \leq ||x - y|| \)                                                                 │
│ 2. \( ||y|| - ||x|| \leq ||x - y|| \)                                                                 │
│                                                                                                       │
│ ### Step 6: Conclude the Inequality                                                                   │
│                                                                                                       │
│ These two results imply that:                                                                         │
│                                                                                                       │
│ [                                                                                                     │
│ | ||x|| - ||y|| | \leq ||x - y||.                                                                     │
│ \]                                                                                                    │
│                                                                                                       │
│ Therefore, we have successfully demonstrated that                                                     │
│                                                                                                       │
│ [                                                                                                     │
│ | ||x|| - ||y|| | \leq ||x - y||                                                                      │
│ \]                                                                                                    │
│                                                                                                       │
│ holds for any vectors \( x, y \in \mathbb{R}^n \).                                                    │
│                                                                                                       │
│ ### Final Result                                                                                      │
│                                                                                                       │
│ To summarize, the proven inequality is:                                                               │
│                                                                                                       │
│ [                                                                                                     │
│ \boxed{| ||x|| - ||y|| | \leq ||x - y||}.                                                             │
│ \]                                                                                                    │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Exiting the Application

To exit the program, simply type `exit` when prompted:

```
Insira um problema matemático (or digite 'exit' para sair)
> exit
```

## Dependencies

The project relies on the following Python packages:

- **black==24.8.0**
- **ipython==8.27.0**
- **numpy==2.1.1**
- **openai==1.44.1**
- **pandas==2.2.2**
- **pydantic==2.9.1**
- **pyperclip==1.9.0**
- **python-dotenv==1.0.1**
- **rich==13.8.1**
- **scipy==1.14.1**
- **seaborn==0.13.2**
- **sympy==1.13.2**
- **tqdm==4.66.5**

These are listed in the `requirements.txt` file and can be installed using the `pip install -r requirements.txt` command.

## Project Structure

- **`main.py`**: The main script that runs the application.
- **`code_interpreter.py`**: Contains the `CodeInterpreter` class responsible for executing Python code securely.
- **`requirements.txt`**: Lists all the Python packages required to run the project.

## Contributing

Contributions are welcome! If you have ideas for improvements or encounter any issues, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- **[OpenAI](https://openai.com/)** for providing the GPT-4 API.
- **[Rich](https://github.com/Textualize/rich)** for enabling beautiful formatting in the terminal.
- **[SymPy](https://www.sympy.org/)** for symbolic mathematics capabilities.
- **[NumPy](https://numpy.org/)** and **[SciPy](https://scipy.org/)** for numerical computations.
- **[Matplotlib](https://matplotlib.org/)** and **[Seaborn](https://seaborn.pydata.org/)** for data visualization tools.

## Disclaimer

This project is for educational purposes. The accuracy of the mathematical solutions depends on the responses from the OpenAI API and the correctness of the code execution. Always double-check the results, especially for critical applications.