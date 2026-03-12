# CS408-CanvasFun
## Canvas CLI Tool

A simple Python command-line tool that allows students to interact with their Canvas account and retrieve class and assignment information.

## Features

Once running, the tool allows you to:

1. Display all current classes
2. Display information about a specific class
3. Display all grades for a specific class
4. Display upcoming assignments

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/<your-username>/<repo-name>.git
    cd <repo-name>/src
    ```

2. (Optional) Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux / macOS
    venv\Scripts\activate      # Windows
    ```

3. Install required Python packages:

    ```bash
    pip install -r ../requirements.txt
    ```

4. Copy the `.env.sample` file to `.env` and fill in your Canvas API token and base URL:

    ```bash
    cp ../.env.sample ../.env   # Linux / macOS
    copy ..\.env.sample ..\.env # Windows
    ```

   Edit `.env` to include your actual API token and Canvas URL:

    ```env
    CANVAS_API_TOKEN=your_actual_token_here
    CANVAS_BASE_URL=https://schoolnamecanvas.instructure.com
    ```
## Usage

Run the CLI tool:

   ```bash
   python main.py
   ```

Follow the prompts and enter the number corresponding to the action you want to perform. For example:

1. Display all current classes
2. Display information about a specific class
3. Display all grades for a specific class
4. Display upcoming assignments
   Enter your choice:

Continue following the prompts to view class information, grades, or upcoming assignments.

## Demo

<img src="assets/canvas_cli_demo.gif" alt="Canvas CLI Tool Demo" style="border: 3px solid #1E90FF; border-radius: 8px;" width="600">

## Contributing

This is a school project. Feel free to fork and experiment with it.

## License

This project is not licensed.