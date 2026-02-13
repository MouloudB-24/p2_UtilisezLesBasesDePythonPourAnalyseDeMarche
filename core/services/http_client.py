import requests


class HttpClient:
    """
    Generic Http client
    """
    def __init__(self, timeout: int=10):
        self.timeout = timeout
        self.session = requests.Session()
        
    def get(self, url: str="") -> str:
        """
        Perfoms a GET request
        
        :param url: full url 
        :return: content of the response in text
        """
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        return response.text
    
    def close(self):
        """
        Close session
        """
        self.session.close()
    

if __name__ == "__main__":
    res = requests.get('https://example.com/invalid')
    res.raise_for_status()