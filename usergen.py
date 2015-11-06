import csv
import random
import hashlib
import argparse
from sets import Set
# local modules
import names
import locations

# changeme: this is used as the domain for email addresses
FAKE_EMAIL_DOMAIN = "mydomain.com"
#changeme: this password is used for all users
DEFAULT_PASSWORD = "password"
# changeme: set this to True to avoid duplicate names, False otherwise
ENSURE_UNIQUENESS = True
NAME_SET = Set()
# changeme: if you use LDIF export, this is your company domain component
LDAP_DOMAIN_COMPONENT="mycompany"
# whether to write output to stdout - this is set as an optional program argument
QUIET=False

def out(message):
    if not QUIET:
        print message

def get_name():
    # randomly generate a guy or girl name
    guy_or_girl = random.randint(1, 10)
    last_name = names.random_last_name()

    if guy_or_girl % 2 == 0:
        first_name = names.random_guy_name()
    else:
        first_name = names.random_girl_name()

    return first_name, last_name

def get_random_address():
    street, city, state, country, postal = locations.random_address()
    return {"street": street, "city": city, "state": state, "country": country, "postal": postal}

def hash_user(username, password, first, last, email, initials, full_name):
    user_str = username + password + first + last + email + initials + full_name
    return hashlib.sha256(user_str.encode()).hexdigest()

def get_random_user():
    """ generates a set of data for a fake user, and returns a dict with the relevant fields. """
    # generate a random name
    first, last = get_name()
    # generate some fields based on the name
    username = "%s.%s" % (first.lower(), last.lower())
    password = DEFAULT_PASSWORD
    initials = "%s%s" % (first[0:1], last[0:1])
    full_name = "%s %s" % (first, last)
    #preferred_name = "%s" % (first)
    email = "%s.%s@%s" % (first.lower(), last.lower(), FAKE_EMAIL_DOMAIN)

    # the keys below are ldif-ish on purpose
    hash = hash_user(username, password, first, last, email, initials, full_name)

    # now get a random address
    address = get_random_address()

    # internal dict for a user
    user = {
        "username": username,
        "email": email,
        "initials": initials,
        "first": first,
        "last": last,
        "full_name": full_name,
        "password": password,
        "hash": hash,
        "address" : address
    }
    return user

def print_handler(user):
    """ This handler just prints the user object. Used for testing as needed """
    print(user)

def generate_random_users(count, user_handler):
    """ This function generates "count" random users, calling the user_handler
    function for each user. """
    global NAME_SET
    total_users = 0
    duplicates = 0

    for user_num in range(0,count):
        # generate a user
        user = get_random_user()
        # if these have to be unique, make sure they are not in the set
        if ENSURE_UNIQUENESS and user["hash"] in NAME_SET:
            out("++++ duplicate found! " + user["first"] + " " +user["last"])
            duplicates += 1
            while user["hash"] in NAME_SET:
                user = get_random_user()
            out("++++ replacing with " + user["first"] + " " +user["last"])
        NAME_SET.add(user["hash"])
        total_users += 1
        user_handler(user)
    out("total users generated: %d\nduplicates encountered: %d" % (total_users, duplicates))

def random_users_to_CSV(number, csvfile):
    """ generates random users and writes them to a CSV file """
    with open(csvfile, 'wb') as outputfile:
        writer = csv.writer(outputfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # a handler that writes each user to a csv file
        def csv_handler(user):
            if user["address"]:
                address = user["address"]
                writer.writerow([user["hash"], user["username"], user["password"], user["first"], user["last"], user["email"], user["initials"], user["full_name"], address["street"], address["city"], address["state"], address["postal"], address["country"]])
            else:
                writer.writerow([user["hash"], user["username"], user["password"], user["first"], user["last"], user["email"], user["initials"], user["full_name"]])
        generate_random_users(number, csv_handler)

def random_users_to_LDIF(number, ldiffile):
    """ generates random users and writes them to an ldif file, suitable for loading into a directory """
    with open(ldiffile, "wb") as text_file:
        def ldif_handler(user):
            # transmogrify into ldif fields
            text_file.write("dn: uid=%s,ou=People,dc=%s\n" %(user["hash"], LDAP_DOMAIN_COMPONENT))
            text_file.write("objectClass: top\n")
            text_file.write("objectClass: inetorgperson\n")
            text_file.write("objectClass: organizationalperson\n")
            text_file.write("objectClass: person\n")
            text_file.write("mail: %s\n" % user["email"])
            text_file.write("initials: %s\n" % user["initials"])
            text_file.write("givenName: %s\n" % user["first"])
            text_file.write("sn: %s\n" % user["last"])
            text_file.write("cn: %s\n" % user["full_name"])
            text_file.write("uid: %s\n" % user["hash"])
            text_file.write("userPassword: %s\n" % user["password"])
            text_file.write("description: This is the description for %s.\n" % user["full_name"])
            if user["address"]:
                address = user["address"]
                text_file.write("street: %s\n" % address["street"])
                text_file.write("st: %s\n" % address["state"])
                text_file.write("postalCode: %s\n" % address["postal"])
                text_file.write("c: %s\n" % address["country"])
                text_file.write("l: %s\n" % address["city"])
                text_file.write("postalAddress: %s %s, %s %s %s\n" % (address["street"], address["city"], address["state"], address["postal"], address["country"]))
            text_file.write("\n")
        generate_random_users(number, ldif_handler)

def run(count, form, filename):
    """ main entry point for running the program. """
    max = len(names.GUY_NAMES) * len(names.LAST_NAMES)
    do_it = True # whether to continue once you get the max-size warning below
    if count > max:
        print("Warning: You asked for %d names.  I cannot produce more than %d names.  Setting count to %d." % (count, max,max))
        print("Do you want to continue? (Y/N) [N]")
        option = raw_input()
        do_it = (option == "Y") or (option == "y")
        names_to_generate = max
    else:
        names_to_generate = count

    if do_it:
        out("starting with count:%d format:%s output file:%s" %(count, form, filename))
        if form=="csv":
            random_users_to_CSV(names_to_generate, filename)
        elif form=="ldif":
            random_users_to_LDIF(names_to_generate, filename)
    else:
        out("Done")

def main():
    """ processes the command line arguments and runs the program """
    import argparse
    global QUIET
    parser = argparse.ArgumentParser(description='This program generates user data to a csv file as a default.')
    parser.add_argument('count', metavar='count', type=int,
                   help='An integer representing the number of names to generate')
    parser.add_argument('filename', metavar='filename', type=str,
                   help='The name of the output file to use')
    parser.add_argument('format', metavar='format (csv|ldif)', type=str, nargs="?",
                       default="csv", action='store',
                       help='The format of the output file to use')
    parser.add_argument('-v', '--verbose', dest='quiet', action='store_false',
                   help='do not write anything to stout')
    args = parser.parse_args()
    if not args.count or not args.filename:
        parser.error('You must specify at least a count and an output filename.')
    QUIET = args.quiet
    run(args.count, args.format, args.filename)

if __name__ == "__main__":
    main()
