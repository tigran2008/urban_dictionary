################################################################################
# Attributes                                                                   #
################################################################################

WARN_IF_PLAYSOUND_IS_UNAVAILABLE = True


################################################################################
# Module Imports                                                               #
################################################################################

import requests
from http.client import HTTPException

import datetime
import tempfile


################################################################################
# Classes and Exceptions                                                       #
################################################################################

class Definition:
    def __init__(self, word: str, definition: str, example: str, author: str, permalink: str, upvotes: int, downvotes: int, audio_samples: list, written_on: datetime.datetime, raw_data: dict, index: int):
        self.word          = word
        self.definition    = definition
        self.example       = example
        self.author        = author
        self.permalink     = permalink
        self.upvotes       = upvotes
        self.downvotes     = downvotes
        self.audio_samples = audio_samples
        self.written_on    = written_on
        self.raw_data      = raw_data
        self.index         = index
    
    def todict(self):
        return {
            "word": self.word,
            "definition": self.definition,
            "example": self.example,
            "author": self.author,
            "permalink": self.permalink,
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "sample_samples": self.sample_samples,
            "written_on": self.written_on,
            "raw_data": self.raw_data,
            "index": self.index
        }


class DefinitionNotFoundError(Exception):
    def __init__(self, word):
        self.word = word

    def __str__(self):
        return 'Definition not found for word: ' + self.word


class DefinitionOutOfScopeError(Exception):
    def __init__(self, word, definition_index):
        self.word = word
        self.definition_index = definition_index

    def __str__(self):
        return 'Definition index out of scope for word: ' + self.word


################################################################################
# Functions                                                                    #
################################################################################

def define(word: str, index = 0):
    """Fetch a definition from Urban Dictionary.

    Args:
        word (str): The word to define.
        index (int | None, optional): The index of the definition to fetch. Defaults to 0. If None, returns all definitions.

    Raises:
        DefinitionNotFoundError: If the definition is not found.
        DefinitionOutOfScopeError: If the definition index is out of scope.
        HTTPException: If the HTTP request fails (e.g. non-200 response).

    Returns:
        Definition: The definition.
        list[Definition]: The list of definitions.
    """

    url = 'http://api.urbandictionary.com/v0/define?term=' + word
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        definitions = data['list']
        
        if not definitions:                        # If the definition list is empty,
            raise DefinitionNotFoundError(word)    # raise an error.

        if isinstance(index, int):      # If the definition index is an integer,
            # Check if the index is in range.
            
            if len(definitions) > index:                                     # If the definition index is within the definition list,
                definition = definitions[index]                              # save it for later use.
            else:                                                            # Otherwise,
                raise DefinitionOutOfScopeError(word, index)                 # raise an error.

            # Return the definition.
            return Definition(definition['word'],
                              definition['definition'],
                              definition['example'],
                              definition['author'],
                              definition['permalink'],
                              definition['thumbs_up'],
                              definition['thumbs_down'],
                              definition['sound_urls'],
                              datetime.datetime.strptime(definition['written_on'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                              definition,
                              index)
        elif index is None:
            return [Definition(definition['word'],
                                definition['definition'],
                                definition['example'],
                                definition['author'],
                                definition['permalink'],
                                definition['thumbs_up'],
                                definition['thumbs_down'],
                                definition['sound_urls'],
                                datetime.datetime.strptime(definition['written_on'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                definition,
                                c) for c, definition in enumerate(definitions)]
    else:
        raise HTTPException(f'Error fetching definition for word: {word} - HTTP status code: {response.status_code}')

################################################################################

try:
    from playsound import playsound
    
    class DefinitionNoSoundAvailableError(Exception):
        def __init__(self, word):
            self.word = word

        def __str__(self):
            return 'Definition has no sound available for word: ' + self.word
    
    def play_sample(word, index: int = 0, block: bool = True):
        """Play a definition's Sound sample.

        Args:
            word (str | Definition): The word to retrieve the Sound sample for.
            index (int, optional): The index of the definition to fetch. Defaults to 0. Ignored if word is a Definition object.
            block (bool, optional): Whether to block the current thread until the Sound sample finishes playing. Defaults to True.

        Raises:
            TypeError: If word is not a string or a Definition object.
            DefinitionOutOfScopeError: If the definition index is out of scope.
            DefinitionNoSoundAvailableError: If the definition has no sound available.
        """
        
        try:
            if isinstance(word, str):
                url = define(word).sample_samples[index]
            elif isinstance(word, Definition):
                url = word.sample_samples[index]
            else:
                raise TypeError('word must be a string or Definition')
        except IndexError:
            raise DefinitionOutOfScopeError(f"{word} (sample)", index)
        
        try:
            file = tempfile.NamedTemporaryFile()
            file.write(requests.get(url).content)
            file.seek(0)
            
            playsound(file.name, block=block)
            
            file.close()
        except:
            raise DefinitionNoSoundAvailableError(word)
        
except ImportError:
    if WARN_IF_PLAYSOUND_IS_UNAVAILABLE:
        print("urban: WARNING: 'playsound' module could not be found.", end = "\n" * 2)
        
        print("                 This module is required for play_sample() to work.")
        print("                 Please install it using pip3 install playsound.")
        print("                 If you do not want to see this message again, set WARN_IF_PLAYSOUND_IS_UNAVAILABLE to False in urban.py")
        
        print('\n')

################################################################################

def submit_word(word: str, definition: str, example: str, tags: list, giphy_url: str = None):
    """Submit a word to Urban Dictionary.

    Args:
        word (str): The word to submit.
        definition (str): The definition to submit.
        example (str): The example to submit.
        tags (list): The tags to submit.
        giphy_url (str, optional): The Giphy URL to submit. Defaults to None.

    Raises:
        HTTPException: If the HTTP request fails (e.g. non-200 response).
    """

    url = 'http://api.urbandictionary.com/v0/define'
    data = {
        'term': word,
        'definition': definition,
        'example': example,
        'tags': ','.join(tags),
        'giphy': giphy_url if giphy_url else ''
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise HTTPException(f'Error submitting word: {word} - HTTP status code: {response.status_code}')

__doc__ = \
""" Unofficial Urban Dictionary API wrapper.

    This module provides functions for fetching definitions from Urban Dictionary.
    It also provides functions for playing sounds from Urban Dictionary definitions.
    Since this module is unofficial, it is not guaranteed to work if the Urban Dictionary API is updated.
    
    [Functions]
        define(word, index: int | None = 0) -> Definition | list[Definition]
            Fetches a definition from Urban Dictionary.
            If index is None, returns a list of all definitions.
            If index is an integer, returns the definition at the specified index.
            If index is out of range, raises an error.
            If the definition is not found, raises an error.
        
        play_sample(word, index: int = 0, block: bool = True)
            Plays a sound from a definition's Sound samples.
            If the definition has no sound available, raises an error.
            If index is out of range, raises an error.
            If block is True, blocks until the sound is finished playing.
            If block is False, returns immediately.
            
            * Requires the playsound module.
    
    
    [Attributes]
        WARN_IF_PLAYSOUND_IS_UNAVAILABLE: If True, prints a warning if the playsound module is not found.


    [Classes]
        Definition: Represents a definition from Urban Dictionary.

        [[Methods]]
          todict() -> dict: Returns a dictionary representation of the definition.
        [[Properties]]
          word:        The name of the definition. May have different capitalization from the original search and/or include other words
          definition:  The definition of the searched word
          example:     The example section of the definition
          author:      The username of the creator of the definition
          permalink:   Permanent link to the definition
          upvotes:     The amount of "thumbs up" ratings.
          downvotes:   The amount of "thumbs down" ratings.
          sample_samples: Links to Sound samples of the word. Is used by 'play_sample()'.
          written_on:  'datetime.datetime' representation of the creation time of the definition.
          raw_data:    'dict' representation of the API's JSON response
          index:       The word's index

    
    [Exceptions]
        DefinitionNotFoundError: If the definition is not found.
        DefinitionOutOfScopeError: If the definition index is out of scope.
        DefinitionNoSoundAvailableError: If the definition has no sound available.



    The author of this package is not affiliated with Urban Dictionary.
    The author of this package is not affiliated with the author of playsound.
"""

__author__  = "Tigran Khachatryan"
__version__ = "0.2.0"
__all__     = ["define", "play_sample", "Definition", "DefinitionNotFoundError", "DefinitionOutOfScopeError", "DefinitionNoSoundAvailableError"]
