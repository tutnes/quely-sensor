# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from bookshelf import get_model, storage
from flask import current_app
from gcloud import pubsub
import psq
import requests


# [START get_books_queue]
def get_visitors_queue():
    client = pubsub.Client(
        project=current_app.config['PROJECT_ID'])

    # Create a queue specifically for processing books and pass in the
    # Flask application context. This ensures that tasks will have access
    # to any extensions / configuration specified to the app, such as
    # models.
    return psq.Queue(
        client, 'books', extra_context=current_app.app_context)
# [END get_books_queue]


# Denne bør først sjekke om Mac adressen finnes i listen, 
# hvis ja, så kan den oppdatere med "last seen" hvis ikke kan den slå opp mac adressen i brukerdatabasen
# og mac adresse database
def process_visitor(book_id):
    """
    Handles an individual Bookshelf message by looking it up in the
    model, querying the Google Books API, and updating the book in the model
    with the info found in the Books API.
    """

    model = get_model()

    book = model.read(book_id)

    if not book:
        logging.warn("Could not find book with id {}".format(book_id))
        return

    if 'title' not in book:
        logging.warn("Can't process book id {} without a title."
                     .format(book_id))
        return

    logging.info("Looking up book with title {}".format(book[
                                                        'title']))

    new_book_data = query_books_api(book['title'])

    if not new_book_data:
        return

    book['title'] = new_book_data.get('title')
    book['author'] = ', '.join(new_book_data.get('authors', []))
    book['publishedDate'] = new_book_data.get('publishedDate')
    book['description'] = new_book_data.get('description')

    # If the new book data has thumbnail images and there isn't currently a
    # thumbnail for the book, then copy the image to cloud storage and update
    # the book data.
    if not book.get('imageUrl') and 'imageLinks' in new_book_data:
        new_img_src = new_book_data['imageLinks']['smallThumbnail']
        book['imageUrl'] = download_and_upload_image(
            new_img_src,
            "{}.jpg".format(book['title']))

    model.update(book, book_id)
# [END process_book]


# Denne kan skrives om til å slå opp Mac adresse
# Så kan det skrives en annen som slår opp i eksisterende brukere
def query_mac_addr(mac):
    """
    Queries the Mac address from a db an sees if it can find it
    Checks the three first bytes 00:00:00 against 
    the dataset from:
    https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf
    Example: Mac beginning with 00:03:93 would return Apple
    """
    return "Apple"


def query_visitor_db(mac):
    """
    Queries the existing visitor DB to see whether the Mac address and visitor is already present.
    If it is present it will update the Last seen time to current time
    If it is not there it will write to the db and get the lookup of the mac producer from query_mac_addr
    """
    r = requests.get('https://www.googleapis.com/books/v1/volumes', params={
        'q': title
    })

    try:
        data = r.json()['items'][0]['volumeInfo']
        return data

    except KeyError:
        logging.info("No book found for title {}".format(title))
        return None

    except ValueError:
        logging.info("Unexpected response from books API: {}".format(r))
        return None



