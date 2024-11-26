import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox


# Function to scrape words from the webpage
def scrape_words(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails
        soup = BeautifulSoup(response.text, 'html.parser')
        word_div = soup.find('div', id='listado-palabras')

        if word_div:
            words = [a.text.strip() for a in word_div.find_all('a')]
            return words
        else:
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []


# Function to save words to a text file
def save_to_txt(words, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("\n".join(words))
        print(f"Words saved to {filename}")
    except Exception as e:
        print(f"Error: {e}")


# Function to process two text files and create a third with the given rules
def process_files(file1, file2, detach1, detach2, output_filename):
    try:
        # Read files
        with open(file1, 'r', encoding='utf-8') as f1:
            words1 = [line.strip() for line in f1.readlines()]
        with open(file2, 'r', encoding='utf-8') as f2:
            words2 = [line.strip() for line in f2.readlines()]

        # Process words
        result = []
        for word1 in words1:
            prefix = word1[:detach1]
            suffix1 = word1[detach1:]
            for word2 in words2:
                suffix2 = word2[-detach2:]
                root2 = word2[:-detach2]
                result.append(f"{prefix} - {suffix1} + {root2} - {suffix2}")

        # Save to output file
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(result))
        print(f"Processed words saved to {output_filename}")
    except Exception as e:
        print(f"Error: {e}")


# GUI Implementation
def gui():
    def generate_url():
        """Generate the URL based on user input."""
        base_url = "https://www.parolecon.it/search.php?"
        params = {
            "i": entry_inizia.get(),
            "f": entry_finisce.get(),
            "ms": entry_con_lettere.get(),
            "mns": entry_senza_lettere.get(),
            "m": entry_con_sequenza.get(),
            "mn": entry_senza_sequenza.get(),
            "fnl": entry_num_lettere_da.get(),
            "fnl2": entry_num_lettere_a.get(),
            "d": "50",  # Always included
        }

        # Construct the query string
        query_string = "&".join([f"{key}={value}" for key, value in params.items() if value])
        full_url = base_url + query_string

        # Show the generated URL
        url_entry.delete(0, tk.END)
        url_entry.insert(0, full_url)

    def scrape_url():
        url = url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        words = scrape_words(url)
        if words:
            filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if filename:
                save_to_txt(words, filename)
                messagebox.showinfo("Success", f"Words scraped and saved to {filename}")
        else:
            messagebox.showwarning("No Words Found", "No words were found on the webpage.")

    def process_mode():
        file1 = filedialog.askopenfilename(title="Select First TXT File", filetypes=[("Text files", "*.txt")])
        if not file1:
            return
        detach1 = simpledialog.askinteger("Input", "Detach how many characters from the beginning of each word in TXT 1?")
        if detach1 is None:
            return

        file2 = filedialog.askopenfilename(title="Select Second TXT File", filetypes=[("Text files", "*.txt")])
        if not file2:
            return
        detach2 = simpledialog.askinteger("Input", "Detach how many characters from the end of each word in TXT 2?")
        if detach2 is None:
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not output_file:
            return

        process_files(file1, file2, detach1, detach2, output_file)
        messagebox.showinfo("Success", f"Processed words saved to {output_file}")

    # GUI window
    root = tk.Tk()
    root.title("Word Scraper and Processor")

    # URL Builder Section
    tk.Label(root, text="Costruttore URL").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(root, text="Inizia con (i)").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_inizia = tk.Entry(root, width=30)
    entry_inizia.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Finisce con (f)").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_finisce = tk.Entry(root, width=30)
    entry_finisce.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Con lettere (ms)").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_con_lettere = tk.Entry(root, width=30)
    entry_con_lettere.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="Senza lettere (mns)").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entry_senza_lettere = tk.Entry(root, width=30)
    entry_senza_lettere.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(root, text="Con sequenza (m)").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    entry_con_sequenza = tk.Entry(root, width=30)
    entry_con_sequenza.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(root, text="Senza sequenza (mn)").grid(row=6, column=0, sticky="w", padx=10, pady=5)
    entry_senza_sequenza = tk.Entry(root, width=30)
    entry_senza_sequenza.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(root, text="Numero lettere DA (fnl)").grid(row=7, column=0, sticky="w", padx=10, pady=5)
    entry_num_lettere_da = tk.Entry(root, width=30)
    entry_num_lettere_da.insert(0, "6")  # Default value
    entry_num_lettere_da.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(root, text="Numero lettere A (fnl2)").grid(row=8, column=0, sticky="w", padx=10, pady=5)
    entry_num_lettere_a = tk.Entry(root, width=30)
    entry_num_lettere_a.insert(0, "6")  # Default value
    entry_num_lettere_a.grid(row=8, column=1, padx=10, pady=5)

    tk.Button(root, text="Genera URL", command=generate_url, bg="blue", fg="white").grid(row=9, column=0, columnspan=2, pady=10)

    # URL Scraper Section
    tk.Label(root, text="Enter URL for Scraping:").grid(row=10, column=0, columnspan=2, pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=11, column=0, columnspan=2, padx=10, pady=5)
    tk.Button(root, text="Scrape and Save Words", command=scrape_url, bg="green", fg="white").grid(row=12, column=0, columnspan=2, pady=10)

    # File Processor Section
    tk.Label(root, text="Process Two Text Files:").grid(row=13, column=0, columnspan=2, pady=10)
    tk.Button(root, text="Process Files", command=process_mode, bg="orange", fg="white").grid(row=14, column=0, columnspan=2, pady=10)

    root.mainloop()


if __name__ == "__main__":
    gui()