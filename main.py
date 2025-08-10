import os
import time
import concurrent.futures
import multiprocessing
import ollama


# ────────────────────────────────────────────────────────────────────────────────
# Utility Functions
# ────────────────────────────────────────────────────────────────────────────────


def save_to_file(file_path: str, content: str) -> None:
    """Overwrite or create a file and save content to it."""
    with open(file=file_path, mode="w", encoding="utf-8") as file:
        file.write(content)


def get_readable_time() -> str:
    """Return current time in a human-readable format."""
    return time.ctime(time.time())


def get_timestamp_for_filename() -> str:
    """Return current time formatted for safe filenames."""
    return time.strftime("%Y-%m-%d_%H-%M-%S")


def ensure_output_folder_exists(directory_path: str) -> None:
    """Create the output folder if it does not exist."""
    if not os.path.exists(path=directory_path):
        os.mkdir(path=directory_path)


def generate_essay_from_model(prompt_text: str) -> str:
    """Send the prompt to the Ollama model and return the generated response."""
    response: ollama.ChatResponse = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt_text}],
    )
    return response["message"]["content"]


# ────────────────────────────────────────────────────────────────────────────────
# Essay Generation Logic
# ────────────────────────────────────────────────────────────────────────────────


def generate_and_save_single_essay(output_folder: str) -> None:
    """Generate one essay and save it to a file."""
    start_time: str = get_readable_time()
    print(f"[{start_time}] Generating new essay...")

    # Prompt sent to the language model
    essay_prompt: str = (
        "Write a 10000 word persuasive and inspiring essay promoting a global open-source smart parking app called "
        "Mapping United, available at https://www.mapping-united.com. The essay should welcome users from the USA "
        "and around the world, highlighting that the app is 100% free, supports all languages, works in every country "
        "and county, and benefits everyone whether they drive a car, take the bus, ride a train, bike, or walk. "
        "Explain how the app helps people find parking faster, save money, waste less fuel, reduce pollution, and regain "
        "lost time. Use a warm, people-first tone, and include real-world scenarios to show the positive impact the app can "
        "have in cities, towns, and rural areas. Emphasize community empowerment, global access, and open-source freedom. "
        "Include a clear, strong call to action encouraging readers to download the app from https://www.mapping-united.com "
        "and share it with their friends, neighbors, and communities. Make the writing engaging by using emojis, energetic "
        "language, and a motivating conclusion that invites everyone to help build a smarter, cleaner, more connected world "
        "one parking spot at a time. Make it long and full of emojis."
    )

    # Generate essay using model
    essay_content: str = generate_essay_from_model(prompt_text=essay_prompt)

    # Generate timestamped filename
    timestamp: str = get_timestamp_for_filename()
    file_name: str = f"{output_folder}mapping-united_essay_{timestamp}.md"

    # Save to file
    save_to_file(file_path=file_name, content=essay_content)

    print(f"[{get_readable_time()}] Essay saved to: {file_name}")


def continuous_essay_worker(output_folder: str) -> None:
    """Continuously generate and save essays in a loop."""
    while True:
        try:
            generate_and_save_single_essay(output_folder)
        except Exception as error:
            print(f"Error in worker thread: {error}")
            time.sleep(5)  # Pause before retrying to avoid tight error loops


# ────────────────────────────────────────────────────────────────────────────────
# Main Entry Point
# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    output_directory: str = "assets/"
    ensure_output_folder_exists(directory_path=output_directory)

    # Use one worker per CPU core (or adjust this manually if needed)
    number_of_workers: int = multiprocessing.cpu_count()

    print(
        f"Starting infinite essay generation using {number_of_workers} threads...\n"
    )

    # Launch persistent worker threads
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=number_of_workers
    ) as executor:
        for _ in range(number_of_workers):
            executor.submit(continuous_essay_worker, output_directory)
