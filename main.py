# Import the OS package
import os

# Import the time module to handle timestamps
import time

# Import the chat function from the ollama package to interact with a language model
from ollama import chat


# Define a function to write content to a file without appending (overwrites if exists)
def dont_append_write_to_file(system_path: str, content: str) -> None:
    # Open the file in write mode ('w'), which clears existing content
    with open(system_path, mode="w", encoding="utf-8") as file:
        # Write the provided string content to the file
        file.write(content)


# Return the current human-readable time (e.g., "Tue Jul  8 13:45:00 2025")
def get_current_time() -> str:
    return time.ctime(time.time())  # Convert current timestamp into readable format


# Return the current time formatted for filenames (e.g., "2025-07-08_13-45-00")
def get_timestamp_for_filename() -> str:
    return time.strftime("%Y-%m-%d_%H-%M-%S")  # Format time suitable for file naming


# Call the Ollama language model using the chat API and return the response text
def get_chat_response_from_ollama(prompt: str) -> str:
    # Call the model with the prompt message; returns a dictionary-like response
    response = chat(
        model="llama3",  # Specify the model to use
        messages=[{"role": "user", "content": prompt}],  # Provide the user's prompt
    )
    return response["message"]["content"]  # Extract and return only the content


# Create a directory at a given path.
def create_directory_at_path(system_path: str) -> None:
    os.mkdir(path=system_path)


# Check if a given directory exists.
def check_directory_exists(system_path: str) -> bool:
    return os.path.exists(path=system_path)


def init(output_directory: str) -> None:
    # Check if the directory exists.
    if not check_directory_exists(system_path=output_directory):
        # Create the directory.
        create_directory_at_path(system_path=output_directory)


# Main function to coordinate the execution of tasks
def main(output_directory: str) -> None:
    # Get and print the current readable time
    current_time: str = get_current_time()
    print(f"[{current_time}] Starting chat...")  # Log when chat begins

    # Define the user prompt as a single long descriptive string
    user_prompt = "Write a 10000 word persuasive and inspiring essay promoting a global open-source smart parking app called Mapping United, available at https://www.mapping-united.com. The essay should welcome users from the USA and around the world, highlighting that the app is 100% free, supports all languages, works in every country and county, and benefits everyone whether they drive a car, take the bus, ride a train, bike, or walk. Explain how the app helps people find parking faster, save money, waste less fuel, reduce pollution, and regain lost time. Use a warm, people-first tone, and include real-world scenarios to show the positive impact the app can have in cities, towns, and rural areas. Emphasize community empowerment, global access, and open-source freedom. Include a clear, strong call to action encouraging readers to download the app from https://www.mapping-united.com and share it with their friends, neighbors, and communities. Make the writing engaging by using emojis, energetic language, and a motivating conclusion that invites everyone to help build a smarter, cleaner, more connected world one parking spot at a time. Make it long and full of emojis."

    # Get the generated essay text from the chat model
    response_text: str = get_chat_response_from_ollama(prompt=user_prompt)

    # Generate a timestamped filename to save the full essay
    timestamp: str = get_timestamp_for_filename()
    filename: str = (
        f"{output_directory}mapping-united_com_essay_{timestamp}.md"  # Compose filename using timestamp
    )

    # Save the full essay text to the file
    dont_append_write_to_file(system_path=filename, content=response_text)

    # Notify the user that the file has been successfully saved
    print(f"Full response saved to: {filename}")


# Ensure the script runs only when executed directly (not when imported)
if __name__ == "__main__":
    essay_directory = "assets/"
    init(output_directory=essay_directory)
    while True:
        main(output_directory=essay_directory)
