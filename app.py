# Ryan Bachman
# University of Advancing Technology
# MS587, Databases and Web Development
# Summer 2024, Grad 1
# Assignment 3.1 - Your eBook and Audiobook Web Application with Flask


from flask import Flask, render_template
from book_database import get_books, get_specific_book, get_book_details, db_session, Book, BookDetails
from pathlib import Path
import pyttsx3


app = Flask(__name__)


def get_headers(response): # Get the headers from the response of the website.
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'


@app.route('/')  # Display the home page so the user can start interacting with the website.
def main():
    """Entry point; the view for the main page"""
    return render_template('index.html')


@app.route('/second') # View the page showing
def reading_page():
    """Views for the book details that a user can pick to read from the database."""
    try:  # Attempt to do the following, otherwise...
        books = get_books()  # Run the get_books function from the book_database.py file to get all of the book content to display.
        return render_template('Reading.html', books=books)
    except Exception as e:  # Print out the exception page with a message.
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


@app.route('/second/<book_id>')
def ereader_page(book_id):
    """Views for the book details that a user can pick to read from the database."""
    try:  # Attempt to do the following, otherwise...
        books = get_specific_book(book_id)  # Take book_id as an argument to only output the specific book name and text the user chose.
        book_details = get_book_details(book_id)

        return render_template('eReader.html', books=books, book_details=book_details)
    except Exception as e:  # Print out the exception page with a message.
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


@app.route('/download/<book_id>')
def download_book(book_id):
    try:  # Attempt to do the following, otherwise...
        # Get the book name and text from the specific book_id that the user chose.
        book_name = str(db_session.query(Book).filter_by(book_id=book_id).first().book_name)
        book_text = str(db_session.query(BookDetails).filter_by(book_id=book_id).first().book_text)

        # Set the download path to the users downloads folder.
        downloads_path = str(Path.home() / 'Downloads')

        # Write the book name and text to the users download folder with their book name as the file name.
        f = open(downloads_path + "/" + book_name + ".txt", "w")
        f.write(book_name)
        f.write("\n\n")
        f.write(book_text)
        f.close()
    except Exception as e:  # Print out the exception page with a message.
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

    return render_template('download.html')


@app.route('/audiobook/<book_id>')
def audio_start(book_id):
    try:  # Attempt to do the following, otherwise...
        # Get the book name and text from the specific book_id that the user chose.
        book_name = str(db_session.query(Book).filter_by(book_id=book_id).first().book_name)
        book_text = str(db_session.query(BookDetails).filter_by(book_id=book_id).first().book_text)

        # Read the books name and books text using text to speech so the user can hear instead of reading.
        text_to_speech(book_name, "Female")
        text_to_speech(book_text, "Female")
    except Exception as e:  # Print out the exception page with a message.
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

    return render_template('audiobook.html')


@app.route('/downloadmp3/<book_id>')
def audio_download(book_id):
    try:  # Attempt to do the following, otherwise...
        # Get the book name and text from the specific book_id that the user chose.
        book_name = str(db_session.query(Book).filter_by(book_id=book_id).first().book_name)
        book_text = str(db_session.query(BookDetails).filter_by(book_id=book_id).first().book_text)

        # Call the text_to_speech_mp3 function to download the book with the name and text and set a female voice.
        text_to_speech_mp3(book_name, book_text, "Female")
    except Exception as e:  # Print out the exception page with a message.
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

    return render_template('downloadmp3.html')


@app.route('/third')  # Set up the references page to see the resources I used for this assignment.
def reference_page():
    """Views for the city details"""
    return render_template('References.html')


def text_to_speech(text, gender):  # Create the function that will be handling the text to speech for the audiobook.
    """
    Function to convert text to speech
    :param text: text
    :param gender: gender
    :return: None
    """
    voice_dict = {'Male': 0, 'Female': 1}  # Set the parameters for the male and female voice.
    code = voice_dict[gender]  # Set the gender based on the function argument.

    engine = pyttsx3.init()  # Initiate the text to speech engine.

    # Setting up voice rate
    engine.setProperty('rate', 160)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 0.8)

    # Change voices: 0 for male and 1 for female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)

    engine.say(text)  # Output the text to speech to the user.
    engine.runAndWait()


def text_to_speech_mp3(title, text, gender):  # Create the function that will be handling the text to speech mp3 download for the audiobook.
    """
    Function to convert text to speech
    :param title: title
    :param text: text
    :param gender: gender
    :return: None
    """
    voice_dict = {'Male': 0, 'Female': 1}  # Set the parameters for the male and female voice.
    code = voice_dict[gender]  # Set the gender based on the function argument.
    downloads_path = str(Path.home() / 'Downloads')  # Set the path to download the file to the user's downloads folder.

    engine = pyttsx3.init()  # Initiate the text to speech engine.

    # Setting up voice rate
    engine.setProperty('rate', 160)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 0.8)

    # Change voices: 0 for male and 1 for female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)

    engine.save_to_file(text, downloads_path + "/" + title + ".mp3")  # Output the text to and MP3 file the user can open.
    engine.runAndWait()


if __name__ == '__main__':  # Main function.
    app.run()