# urban_dictionary
Unofficial Urban Dictionary API wrapper.

## Installation
This module is not available as a package (for now), because I am not very familiar with them.


To use this module, you can simply create a `modules` folder in your project, then copy the `urban.py` file into your folder. You'll be able to import it from your main file like this:
```py
import modules.urban as urban
```


## Examples

```py
"""Script to get the amount of definitions for "Hello" in Urban Dictionary"""

import urban

definitions = urban.define('hello', index=None)
def_amount = len(definitions)

print("The word 'hello' has {} definitions in Urban Dictionary.".format(def_amount))
```

```py
"""Script to play the audio file for 'hello' using the Urban Dictionary API"""

import urban

hello = urban.define('hello')
urban.play_tts(hello)
```

```py
"""Script to ask the user for a word and define it"""

import urban

word = input("Search for a definition in Urban Dictionary: ")
definition = urban.define(word)

print(definition.word)
print(definition.definition)
print(definition.example)
print(f"👍 {definition.upvotes} | 👎 {definition.downvotes}", end = "\n" * 2)

print(definition.permalink)
```


## Usage

This module provides functions for fetching definitions from Urban Dictionary.
It also provides functions for playing sounds from Urban Dictionary definitions.
Since this module is unofficial, it is not guaranteed to work if the Urban Dictionary API is updated.

### Functions

#### `define(word: str, index: int | None = 0)` <sub>`-> Definition | list[Definition]`</sub>
- Fetches a definition from Urban Dictionary.
  * If `index` is `None`, returns a list of all definitions.
  * If `index` is an integer, returns the definition at the specified index.
  * If `index` is out of range, raises an error.
  * If the definition is not found, raises an error.
        
#### `play_sample(word, index: int = 0, block: bool = True)` <sub>`-> None`</sub>
- Plays a sound from a definition's audio samples.
  * If the definition has no sound available, raises an error.
  * If `index` is out of range, raises an error.
  * If `block` is `True`, blocks until the sound is finished playing.
  * If `block` is `False`, returns immediately.
<sub>Requires the playsound module.</sub>
    
    
### Attributes

`WARN_IF_PLAYSOUND_IS_UNAVAILABLE`: If True, prints a warning if the playsound module is not found.


### Classes

`Definition`: Represents a definition from Urban Dictionary.
- Methods
  * `todict()` <sub>`-> dict`</sub>: Returns a dictionary representation of the definition.
- Properties
  * `word`: The name of the definition. May have different capitalization from the original search and/or include other words
  * `definition`: The definition of the searched word
  * `example`: The example section of the definition
  * `author`: The username of the creator of the definition
  * `permalink`: Permanent link to the definition
  * `upvotes`: The amount of "thumbs up" ratings.
  * `downvotes`: The amount of "thumbs down" ratings.
  * `audio_samples`: Links to audio samples of the word. Is used by `play_audio()`.
  * `written_on`: `datetime.datetime` representation of the creation time of the definition.
  * `raw_data`: `dict` representation of the API's JSON response
  * `index`: The word's index

    
### Exceptions

- `DefinitionNotFoundError`:         If the definition is not found.
- `DefinitionOutOfScopeError`:       If the definition index is out of scope.
- `DefinitionNoSoundAvailableError`: If the definition has no sound available.

----------------------------------------------------------------------------------------

<sub>

The author of this package is not affiliated with Urban Dictionary.

The author of this package is not affiliated with the author of playsound.

</sub>
