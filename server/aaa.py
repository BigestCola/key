import requests

def make_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果响应状态码不是200,则抛出异常
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    url = "http://192.168.3.87:8200/cdkey/?cd_key=aa14682d-8a30-4e7d-b8ce-65b0faa80b3c"
    response = make_request(url)
    print("Server response:", response)

if __name__ == "__main__":
    main()
