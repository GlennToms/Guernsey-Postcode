import argparse
import asyncio
import aiohttp
import json
import string
import time


def get_url(postcode):
    """
    Send a GET request to the Guernsey Postcode API with the specified postcode.

    Args:
        postcode (str): The postcode to search for.

    Returns:
        Response object from the Guernsey Postcode API.
    """
    url = f"https://guernsey.isl-fusion.com/api/search/{postcode}"

    # Set up proxies if necessary
    # proxies = {"http": "http://localhost:8080"}

    # Send GET request to API with specified postcode
    r = requests.get(url)

    return r


def gen_postcodes():
    """
    Generate all possible Guernsey postcodes.

    Returns:
        A generator that yields one Guernsey postcode at a time.
    """
    for number_one in range(1, 11):
        for number_two in range(10):
            for first_letter in string.ascii_uppercase:
                for second_letter in string.ascii_uppercase:
                    yield f"GY{number_one} {number_two}{first_letter}{second_letter}"


def write_to_file(postcode, data):
    """
    Write the results of the Guernsey Postcode API search to a file.

    Args:
        postcode (str): The postcode used in the search.
        data (dict): The results of the API search.

    Returns:
        None
    """
    if data.get("results"):
        with open(f"{postcode}.json", "w") as outfile:
            outfile.write(json.dumps(data.get("results"), indent=4))


async def search_postcodes():
    """
    Use aiohttp to asynchronously search for all Guernsey postcodes.

    Returns:
        None
    """
    async with aiohttp.ClientSession() as session:
        url = "https://guernsey.isl-fusion.com/api/search/"

        # Keep track of how many consecutive fails we've had
        fails = 0

        for postcode in gen_postcodes():
            res = await session.get(url + postcode)

            if res.status == 200:
                write_to_file(postcode, await res.json())

                # Reset the fail counter
                fails = 0
            else:
                # Increment the fail counter
                fails += 1

                # If we've had 3 consecutive fails, stop searching
                if fails >= 3:
                    break

            print(f"Search for postcode {postcode} complete.")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Search for all Guernsey postcodes using the Guernsey Postcode API.")
    parser.add_argument(
        "-t", "--timeout", type=int, default=3, help="Number of consecutive fails to tolerate before stopping search."
    )
    args = parser.parse_args()

    # Start timer
    start_time = time.time()

    # Run postcode search
    asyncio.run(search_postcodes())

    # Calculate and print elapsed time
    elapsed_time = time.time() - start_time
    print(f"Search completed in {elapsed_time:.2f} seconds.")

# python get-all-postcodes.py -t <timeout>
