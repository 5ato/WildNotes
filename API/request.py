from requests import Session, Response

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}


def get_response(url: str, h: dict[str, str] = {}) -> Response:
    """Get response from website

    Args:
        url (str): Url website
        h (dict[str, str], optional): headers, have default. Defaults to {}.

    Returns:
        Response: Response from website
    """
    if h: headers.update(h)
    with Session() as s:
        r = s.get(url, headers=headers)
    return r
