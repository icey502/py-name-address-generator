# py-name-generator
This is a quick and dirty tool that I wrote because I had a need to generate a semi-large amount of name/address data in a manner looked semi-realistic, yet could be saved and then loaded in some different formats.

Did I mention "quick" and "dirty"?

### Usage
I'm still working on making this a bit more civilized to use, but the simple way to run it is as follows:

python usergen.py <number> <output file> <format> [-v|--verbose]

Example:
python usergen.py 1000 out.ldif ldif -v

### How It Works
Remember, I said "quick and dirty", and that's what this is.

In a nushell, the code takes guy or girl first names at random from a pool of existing names.  It then chooses a last name at random from yet another pool of last names, then chooses a random address, and creates a "user profile" from that.  The "profile" includes derivable data such as username, email address, and so forth.

Since addresses were not quite as important to me, I just used a few arbitrarily, although I plan to elaborate this further in the future.

There are many ways to improve on what this does, but since it suited my needs at the time, I put it up here :-)

### Limitations
Supported formats as of this writing are csv and ldif.

The program will ask you for combinations if you are attempting to generate an amount of data that is larger than the total permutations of the existing name pools within.

The "random" part is very inefficient if you are trying to generate very large sets,
you might as well just remove the random part and generate combinations of first and last names, or first-first last etc.  As it is, you cannot generate more than len(first name list) * len (last name list) combinations, but of course this is fairly easily changed.

### Improvements Possible
Unicode.

Add combinations (rather than random generation) as an option, in which the names are simply looped in combination until the count is reached.  Simple stuff.

More output formats and better decoupling of output format from execution.

Surfing names/addresses from online sources as an option.
