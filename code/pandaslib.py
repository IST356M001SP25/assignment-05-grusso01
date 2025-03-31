from datetime import datetime

def clean_currency(item: str) -> float:
    '''
    remove anything from the item that prevents it from being converted to a float
    '''    
    if isinstance(item, str):
        cleaned = ''.join(c for c in item if c.isdigit() or c == '.')
    return float(cleaned)

def extract_year_mdy(timestamp):
    '''
    use the datatime.strptime to parse the date and then extract the year
    '''
    if not isinstance(timestamp, str):
        return None
    try:
        date_obj = datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S')  # Adjust format if needed
        return date_obj.year
    except ValueError:
        return None

def clean_country_usa(item: str) ->str:
    '''
    This function should replace any combination of 'United States of America', USA' etc.
    with 'United States'
    '''
    possibilities = [
        'united states of america', 'usa', 'us', 'united states', 'u.s.'
    ]
    if isinstance(item, str):
        item_lower = item.lower().strip()
        if item_lower in possibilities:
            return 'United States'
    return item

if __name__=='__main__':
    print("""
        Add code here if you need to test your functions
        comment out the code below this like before sumbitting
        to improve your code similarity score.""")
    # print(clean_currency("$1,000"))  # Expected: 1000.0
    # print(clean_currency("10,000.01"))  # Expected: 10000.01
    # print(clean_currency("10,000,000.99"))  # Expected: 10000000.99

    # print(extract_year_mdy("12/31/2021 23:59:59"))  # Expected: 2021
    # print(extract_year_mdy("2/16/2023 19:14:37"))  # Expected: 2023
    # print(extract_year_mdy("1/1/2019 12:00:00"))  # Expected: 2019

    # print(clean_country_usa("United States of America"))  # Expected: 'United States'
    # print(clean_country_usa("USA"))  # Expected: 'United States'
    # print(clean_country_usa("U.S."))  # Expected: 'United States'
    # print(clean_country_usa("Canada"))  # Expected: 'Canada'

