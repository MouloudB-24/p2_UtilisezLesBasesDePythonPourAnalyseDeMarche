import requests


class HttpClient:
    """
    Generic Http client
    """
    def __init__(self, timeout: int=10):
        self.timeout = timeout
        self.session = requests.Session()
        
    def get_text(self, url: str) -> str:
        """
        Perfoms a GET request and return text content
        
        :param url: full url 
        :return: content of the response in text
        """
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        return response.text
    
    def get_bytes(self, url: str)  -> bytes:
        """
        Perform GET request and return binary content
        
        :param url: full url
        :return: content of the response in byte
        """
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        return response.content
    
    def close(self):
        """
        Close session
        """
        self.session.close()
    

if __name__ == "__main__":
    res = requests.get('https://example.com/invalid')
    res.raise_for_status()