import requests

def make_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果响应状态码不是200,则抛出异常
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    url = "http://192.168.3.87:8200/cdkey/?cd_key=b29005d7-0135-4436-b472-8b97d6e08df0"
    response = make_request(url)
    print("Server response:", response)

if __name__ == "__main__":
    main()
