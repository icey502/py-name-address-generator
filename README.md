# py-name-address-generator
This is a quick and dirty tool that I wrote because I had a need to generate a large amount of name/address data in a manner looked semi-realistic, yet could be saved and then loaded in some different formats.

### Usage
I'm still working on making this a bit more civilized to use, but the simple way to run it is to run this:

python usergen.py <number> <output file> <format> [-v|--verbose]

Example:
python usergen.py 1000 out.ldif ldif -v

Supported formats as of this writing are csv and ldif.

### Limitations
Remember, I said "quick and dirty", and that's what this is.

In a nushell, the code takes guy or girl first names at random, then chooses a last name at random, then a random address, and creates a "user profile" from that, including username, email address, and so forth.

The "random" part is very inefficient if you are trying to generate very large sets,
you might as well just remove the random part and generate combinations of first and last names, or first-first last etc.  As it is, you cannot generate more than len(first name list) * len (last name list) combinations, but of course this is fairly easily changed.

Since addresses were not important to me, I just used two arbitrarily, although I plan to elaborate this further in the future.
