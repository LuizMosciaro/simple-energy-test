import os
import requests
from typing import Optional
from bs4 import BeautifulSoup

class Informations:
    def __init__(self,url:str,payload:Optional[dict],headers:Optional[dict],read_lines:Optional[bool]=False) -> str:
        self.url = url
        self.payload = payload
        self.headers = headers
        self.read_lines = read_lines

    def post(self):        
        with requests.Session() as session:
            response = session.get(url=self.url,headers=self.headers)
            if response.status_code == 200:
                root = BeautifulSoup(response.content,'lxml')
                csrf_token = root.body.input['value']
                self.payload.update({'csrf':csrf_token})
                result = session.post(url=self.url,headers=self.headers,data=self.payload)
                links = BeautifulSoup(result.content,'lxml').body.find_all("a")
                for link in links:
                    download_path = link['href']
                    print(f"Arquivo salvo em: {os.path.join(os.path.dirname(__file__),download_path)}")
                    file = session.post(url=self.url+f"{download_path}",headers=self.headers,data=self.payload)
                    with open(download_path,'wb') as new_file:
                        new_file.write(file.content)      

            else:
                print(f"Status: [{response.status_code}]\nContent:\n",response.content.decode('utf-8'))


if __name__=="__main__":
    URL = "https://simpleenergy.com.br/teste/"
    DATA = {"codigo":str(input("Informe o numero do codigo:\n"))}
    HEADER = {
        "content-type":"application/x-www-form-urlencoded",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    }
    Informations(url=URL,headers=HEADER,payload=DATA,read_lines=True).post()

